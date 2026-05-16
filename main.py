from datetime import datetime, timezone

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import *

from .hypixel_client import HypixelClient
from .renderer import TEMPLATES


def calc_fkdr(final_kills: int, final_deaths: int) -> str:
    if final_deaths == 0:
        return f"{final_kills:.2f}"
    return f"{final_kills / final_deaths:.2f}"

def calc_kdr(kills: int, deaths: int) -> str:
    if deaths == 0:
        return f"{kills:.2f}"
    return f"{kills / deaths:.2f}"

def calc_wlr(wins: int, losses: int) -> str:
    if losses == 0:
        return f"{wins:.2f}"
    return f"{wins / losses:.2f}"

def ts_to_str(ts: int) -> str:
    if ts == 0:
        return "N/A"
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def calc_star_from_exp(exp: int) -> int:
    if exp <= 0:
        return 1
    xp_table = [0]
    for i in range(1, 10001):
        xp_table.append(xp_table[-1] + 5000)
    level = 0
    for i, xp in enumerate(xp_table):
        if exp < xp:
            level = i
            break
        level = i
    return level

def fmt_num(n: int) -> str:
    return f"{n:,}"


SEP = "\n" + "=" * 36 + "\n"


@register("astrbot_plugin_hypixel_api", "bi_xiaoyang2", "Hypixel 玩家数据查询插件", "1.0.0")
class HypixelPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        api_key = self.config.get("api_key", "")
        if api_key:
            self.client = HypixelClient(api_key)
            logger.info("Hypixel API 客户端已初始化")
        else:
            self.client = None
            logger.warning("Hypixel API Key 未配置，请在插件配置页中填写")

    def _is_banned(self, event: AstrMessageEvent) -> bool:
        group_id = event.get_group_id()
        user_id = event.get_sender_id()
        ban_groups = self.config.get("ban_groups", [])
        ban_users = self.config.get("ban_users", [])
        if group_id and str(group_id) in [str(x) for x in ban_groups]:
            logger.info(f"群组 {group_id} 在黑名单中，已拦截")
            return True
        if user_id and str(user_id) in [str(x) for x in ban_users]:
            logger.info(f"用户 {user_id} 在黑名单中，已拦截")
            return True
        return False

    def _get_render_mode(self) -> str:
        mode = self.config.get("render_mode", "auto")
        return mode if mode in ("auto", "text") else "auto"

    async def _output(self, event: AstrMessageEvent, kind: str, text_fb: str, data: dict):
        mode = self._get_render_mode()
        if mode == "text":
            yield event.plain_result(text_fb)
            return

        tmpl = TEMPLATES.get(kind)
        if tmpl:
            try:
                url = await self.html_render(tmpl, data, options={"scale": "css", "type": "png"})
                yield event.image_result(url)
                return
            except Exception as e:
                logger.info(f"HTML 渲染失败，尝试 T2I 降级: {e}")

        try:
            url = await self.text_to_image(text_fb)
            yield event.image_result(url)
        except Exception as e:
            logger.info(f"T2I 渲染失败，降级为纯文本: {e}")
            yield event.plain_result(text_fb)

    @filter.command("hypixel")
    async def hypixel(self, event: AstrMessageEvent):
        if self._is_banned(event):
            return

        message_str = event.message_str.strip()
        parts = message_str.split(maxsplit=2)

        if len(parts) < 2:
            yield event.plain_result(
                "Hypixel 数据查询插件\n\n"
                "用法:\n"
                "  /hypixel player <ID>   - 玩家基本信息\n"
                "  /hypixel bedwars <ID>  - 起床战争数据\n"
                "  /hypixel skywars <ID>  - 空岛战争数据\n"
                "  /hypixel arcade <ID>   - 街机游戏总览\n"
                "  /hypixel zombies <ID>  - 丧尸末日数据\n"
                "  /hypixel party <ID>    - 小游戏派对数据\n"
                "  /hypixel setkey <key>  - 设置 API Key"
            )
            return

        sub = parts[1]
        arg = parts[2] if len(parts) > 2 else ""

        if sub == "setkey":
            if not arg:
                yield event.plain_result("请输入 API 密钥: /hypixel setkey <key>")
                return
            self.config["api_key"] = arg
            self.config.save_config()
            self.client = HypixelClient(arg)
            logger.info(f"Hypixel API Key 已更新（由 {event.get_sender_id()} 设置）")
            yield event.plain_result("Hypixel API Key 已设置并保存!")
            return

        handlers = {
            "player": self._handle_player,
            "bedwars": self._handle_bedwars,
            "skywars": self._handle_skywars,
            "arcade": self._handle_arcade,
            "zombies": self._handle_zombies,
            "party": self._handle_party,
        }
        handler = handlers.get(sub)
        if not handler:
            yield event.plain_result(f"未知子命令: {sub}\n请使用 /hypixel 查看帮助。")
            return
        if not arg:
            yield event.plain_result(f"请输入玩家游戏ID: /hypixel {sub} <ID>")
            return

        sender = event.get_sender_name()
        uid = event.get_sender_id()
        gid = event.get_group_id()
        ctx = f"用户 {sender}({uid})"
        if gid:
            ctx += f" 在群 {gid}"
        logger.info(f"查询 {sub} {arg} — {ctx}")

        async for result in handler(event, arg):
            yield result

    async def _handle_player(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            info = await self.client.get_player_rank_info(name=name)
        except Exception as e:
            logger.info(f"查询玩家 {name} 失败: {e}")
            yield event.plain_result(f"获取玩家信息失败: {e}")
            return

        level = calc_star_from_exp(info.get("network_level", 0))
        data = {
            "initials": (info["display_name"][:2] if info["display_name"] else "?").upper(),
            "display_name": info["display_name"],
            "rank_display": info.get("rank", "NONE"),
            "level": level,
            "uuid": info["uuid"],
            "language": info.get("language", "N/A"),
            "karma": fmt_num(info.get("karma", 0)),
            "rank": info.get("rank", "NONE"),
            "first_login": ts_to_str(info.get("first_login", 0)),
            "last_login": ts_to_str(info.get("last_login", 0)),
        }
        text_fb = (
            f"玩家信息: {info['display_name']} Lv.{level}{SEP}"
            f"UUID: {info['uuid']}  Rank: {info.get('rank', 'NONE')}{SEP}"
            f"Karma: {fmt_num(info.get('karma', 0))}  语言: {info.get('language', 'N/A')}{SEP}"
            f"首次登录: {ts_to_str(info.get('first_login', 0))}{SEP}"
            f"最近活跃: {ts_to_str(info.get('last_login', 0))}"
        )
        async for result in self._output(event, "player", text_fb, data):
            yield result

    async def _handle_bedwars(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            bw = await self.client.get_bedwars_stats(name=name)
        except Exception as e:
            logger.info(f"查询起床战争 {name} 失败: {e}")
            yield event.plain_result(f"获取起床战争数据失败: {e}")
            return

        fkdr = calc_fkdr(bw["final_kills"], bw["final_deaths"])
        kdr = calc_kdr(bw["kills"], bw["deaths"])
        wlr = calc_wlr(bw["wins"], bw["losses"])
        data = {
            "display_name": bw["display_name"],
            "level": fmt_num(bw["level"]),
            "wins": fmt_num(bw["wins"]),
            "losses": fmt_num(bw["losses"]),
            "final_kills": fmt_num(bw["final_kills"]),
            "final_deaths": fmt_num(bw["final_deaths"]),
            "fkdr": fkdr, "kdr": kdr, "wlr": wlr,
            "beds_broken": fmt_num(bw["beds_broken"]),
            "beds_lost": fmt_num(bw["beds_lost"]),
            "winstreak": str(bw["winstreak"]),
            "games_played": fmt_num(bw["games_played"]),
        }
        text_fb = (
            f"起床战争 [{bw['display_name']}]{SEP}"
            f"等级: {fmt_num(bw['level'])}  硬币: {fmt_num(bw['coins'])}{SEP}"
            f"胜场: {fmt_num(bw['wins'])}  败场: {fmt_num(bw['losses'])}  W/L: {wlr}{SEP}"
            f"击杀: {fmt_num(bw['kills'])}  死亡: {fmt_num(bw['deaths'])}  K/D: {kdr}{SEP}"
            f"最终击杀: {fmt_num(bw['final_kills'])}  最终死亡: {fmt_num(bw['final_deaths'])}  FKDR: {fkdr}{SEP}"
            f"拆床: {fmt_num(bw['beds_broken'])}  丢床: {fmt_num(bw['beds_lost'])}{SEP}"
            f"连胜: {bw['winstreak']}  总场次: {fmt_num(bw['games_played'])}"
        )
        async for result in self._output(event, "bedwars", text_fb, data):
            yield result

    async def _handle_skywars(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            sw = await self.client.get_skywars_stats(name=name)
        except Exception as e:
            logger.info(f"查询空岛战争 {name} 失败: {e}")
            yield event.plain_result(f"获取空岛战争数据失败: {e}")
            return

        kdr = calc_kdr(sw["kills"], sw["deaths"])
        wlr = calc_wlr(sw["wins"], sw["losses"])
        data = {
            "display_name": sw["display_name"],
            "level": sw["level"],
            "wins": fmt_num(sw["wins"]),
            "losses": fmt_num(sw["losses"]),
            "kills": fmt_num(sw["kills"]),
            "deaths": fmt_num(sw["deaths"]),
            "kdr": kdr, "wlr": wlr,
            "souls": fmt_num(sw["souls"]),
            "games_played": fmt_num(sw["games_played"]),
            "heads": fmt_num(sw["heads"]),
        }
        text_fb = (
            f"空岛战争 [{sw['display_name']}]  Lv.{sw['level']}{SEP}"
            f"胜场: {fmt_num(sw['wins'])}  败场: {fmt_num(sw['losses'])}  W/L: {wlr}{SEP}"
            f"击杀: {fmt_num(sw['kills'])}  死亡: {fmt_num(sw['deaths'])}  K/D: {kdr}{SEP}"
            f"Souls: {fmt_num(sw['souls'])}  Heads: {fmt_num(sw['heads'])}{SEP}"
            f"总场次: {fmt_num(sw['games_played'])}  硬币: {fmt_num(sw['coins'])}"
        )
        async for result in self._output(event, "skywars", text_fb, data):
            yield result

    async def _handle_arcade(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            arc = await self.client.get_arcade_stats(name=name)
        except Exception as e:
            logger.info(f"查询街机游戏 {name} 失败: {e}")
            yield event.plain_result(f"获取街机数据失败: {e}")
            return

        data = {
            "display_name": arc["display_name"],
            "wins": fmt_num(arc["wins"]),
            "rounds_played": fmt_num(arc["rounds_played"]),
            "coins": fmt_num(arc["coins"]),
            "top_games": arc["top_games"],
        }
        text_fb = f"街机游戏 [{arc['display_name']}]{SEP}总胜场: {fmt_num(arc['wins'])}  总回合: {fmt_num(arc['rounds_played'])}  硬币: {fmt_num(arc['coins'])}"
        if arc["top_games"]:
            text_fb += "\n热门小游戏:\n" + "\n".join(f"  {g}: {w}胜" for g, w in arc["top_games"][:5])
        async for result in self._output(event, "arcade", text_fb, data):
            yield result

    async def _handle_zombies(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            z = await self.client.get_zombies_stats(name=name)
        except Exception as e:
            logger.info(f"查询丧尸末日 {name} 失败: {e}")
            yield event.plain_result(f"获取丧尸末日数据失败: {e}")
            return

        maps_list = list(z["maps"].items())
        kdr = calc_kdr(z["kills"], z["deaths"])
        wlr = calc_wlr(z["wins"], z["losses"])
        data = {
            "display_name": z["display_name"],
            "wins": fmt_num(z["wins"]), "losses": fmt_num(z["losses"]),
            "kills": fmt_num(z["kills"]), "deaths": fmt_num(z["deaths"]),
            "headshots": fmt_num(z["headshots"]),
            "games_played": fmt_num(z["games_played"]),
            "doors_opened": fmt_num(z["doors_opened"]),
            "chests_looted": fmt_num(z["chests_looted"]),
            "rounds_survived": fmt_num(z["rounds_survived"]),
            "best_round": str(z["best_round"]),
            "maps": maps_list,
        }
        text_fb = (
            f"丧尸末日 [{z['display_name']}]{SEP}"
            f"场次: {fmt_num(z['games_played'])}  胜场: {fmt_num(z['wins'])}  败场: {fmt_num(z['losses'])}{SEP}"
            f"击杀: {fmt_num(z['kills'])}  死亡: {fmt_num(z['deaths'])}  K/D: {kdr}  W/L: {wlr}{SEP}"
            f"爆头: {fmt_num(z['headshots'])}  开门: {fmt_num(z['doors_opened'])}  开箱: {fmt_num(z['chests_looted'])}{SEP}"
            f"总生存回合: {fmt_num(z['rounds_survived'])}  最佳回合: {z['best_round']}"
        )
        if z["maps"]:
            text_fb += "\n地图记录:\n" + "\n".join(f"  {m}: 最佳 {r} 回合" for m, r in z["maps"].items())
        async for result in self._output(event, "zombies", text_fb, data):
            yield result

    async def _handle_party(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            p = await self.client.get_party_games_stats(name=name)
        except Exception as e:
            logger.info(f"查询小游戏派对 {name} 失败: {e}")
            yield event.plain_result(f"获取小游戏派对数据失败: {e}")
            return

        data = {
            "display_name": p["display_name"],
            "round_wins": fmt_num(p["round_wins"]),
            "total_rounds": fmt_num(p["total_rounds"]),
            "mini_games": p["mini_games"],
        }
        text_fb = f"小游戏派对 [{p['display_name']}]{SEP}回合胜场: {fmt_num(p['round_wins'])}  总回合: {fmt_num(p['total_rounds'])}"
        if p["mini_games"]:
            text_fb += "\n各小游戏胜场:\n" + "\n".join(f"  {g}: {w}" for g, w in p["mini_games"])
        async for result in self._output(event, "party", text_fb, data):
            yield result

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()
