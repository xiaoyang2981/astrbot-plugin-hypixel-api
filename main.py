from datetime import datetime, timezone

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import *

from .hypixel_client import HypixelClient
from .renderer import TEMPLATES, get_initials


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
            logger.warning("Hypixel API Key 未配置")

    async def _render(self, kind: str, data: dict) -> str | None:
        tmpl = TEMPLATES.get(kind)
        if not tmpl:
            return None
        try:
            return await self.html_render(tmpl, data)
        except Exception:
            return None

    @filter.command("hypixel")
    async def hypixel(self, event: AstrMessageEvent):
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
        async for result in handler(event, arg):
            yield result

    async def _handle_player(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            info = await self.client.get_player_rank_info(name=name)
        except Exception as e:
            yield event.plain_result(f"获取玩家信息失败: {e}")
            return

        level = calc_star_from_exp(info.get("network_level", 0))
        data = {
            "initials": get_initials(info["display_name"]),
            "display_name": info["display_name"],
            "rank_display": info.get("rank", "NONE"),
            "level": level,
            "uuid": info["uuid"],
            "language": info.get("language", "N/A"),
            "karma": f"{info.get('karma', 0):,}",
            "rank": info.get("rank", "NONE"),
            "first_login": ts_to_str(info.get("first_login", 0)),
            "last_login": ts_to_str(info.get("last_login", 0)),
        }
        url = await self._render("player", data)
        if url:
            yield event.image_result(url)
        else:
            yield event.plain_result(
                f"=== 玩家信息 ==={SEP}"
                f"玩家: {info['display_name']}  Lv.{level}{SEP}"
                f"UUID: {info['uuid']}{SEP}"
                f"Rank: {info.get('rank', 'NONE')}  Karma: {info.get('karma', 0):,}{SEP}"
                f"语言: {info.get('language', 'N/A')}{SEP}"
                f"首次登录: {ts_to_str(info.get('first_login', 0))}{SEP}"
                f"最近活跃: {ts_to_str(info.get('last_login', 0))}"
            )

    async def _handle_bedwars(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            bw = await self.client.get_bedwars_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取起床战争数据失败: {e}")
            return

        fkdr = calc_fkdr(bw["final_kills"], bw["final_deaths"])
        kdr = calc_kdr(bw["kills"], bw["deaths"])
        wlr = calc_wlr(bw["wins"], bw["losses"])
        data = {
            "display_name": bw["display_name"],
            "level": f"{bw['level']:,}",
            "wins": f"{bw['wins']:,}",
            "losses": f"{bw['losses']:,}",
            "final_kills": f"{bw['final_kills']:,}",
            "final_deaths": f"{bw['final_deaths']:,}",
            "fkdr": fkdr,
            "kdr": kdr,
            "wlr": wlr,
            "beds_broken": f"{bw['beds_broken']:,}",
            "beds_lost": f"{bw['beds_lost']:,}",
            "winstreak": str(bw["winstreak"]),
            "games_played": f"{bw['games_played']:,}",
        }
        url = await self._render("bedwars", data)
        if url:
            yield event.image_result(url)
        else:
            yield event.plain_result(
                f"=== 起床战争 [{bw['display_name']}] ==={SEP}"
                f"等级: {bw['level']:,}  硬币: {bw['coins']:,}{SEP}"
                f"胜场: {bw['wins']:,}  败场: {bw['losses']:,}  W/L: {wlr}{SEP}"
                f"击杀: {bw['kills']:,}  死亡: {bw['deaths']:,}  K/D: {kdr}{SEP}"
                f"最终击杀: {bw['final_kills']:,}  最终死亡: {bw['final_deaths']:,}  FKDR: {fkdr}{SEP}"
                f"拆床: {bw['beds_broken']:,}  丢床: {bw['beds_lost']:,}{SEP}"
                f"连胜: {bw['winstreak']}  总场次: {bw['games_played']:,}"
            )

    async def _handle_skywars(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            sw = await self.client.get_skywars_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取空岛战争数据失败: {e}")
            return

        kdr = calc_kdr(sw["kills"], sw["deaths"])
        wlr = calc_wlr(sw["wins"], sw["losses"])
        data = {
            "display_name": sw["display_name"],
            "level": sw["level"],
            "wins": f"{sw['wins']:,}",
            "losses": f"{sw['losses']:,}",
            "kills": f"{sw['kills']:,}",
            "deaths": f"{sw['deaths']:,}",
            "kdr": kdr,
            "wlr": wlr,
            "souls": f"{sw['souls']:,}",
            "games_played": f"{sw['games_played']:,}",
            "heads": f"{sw['heads']:,}",
        }
        url = await self._render("skywars", data)
        if url:
            yield event.image_result(url)
        else:
            yield event.plain_result(
                f"=== 空岛战争 [{sw['display_name']}] ==={SEP}"
                f"等级: {sw['level']}  硬币: {sw['coins']:,}{SEP}"
                f"胜场: {sw['wins']:,}  败场: {sw['losses']:,}  W/L: {wlr}{SEP}"
                f"击杀: {sw['kills']:,}  死亡: {sw['deaths']:,}  K/D: {kdr}{SEP}"
                f"Souls: {sw['souls']:,}  Heads: {sw['heads']:,}{SEP}"
                f"总场次: {sw['games_played']:,}"
            )

    async def _handle_arcade(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            arc = await self.client.get_arcade_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取街机数据失败: {e}")
            return

        data = {
            "display_name": arc["display_name"],
            "wins": f"{arc['wins']:,}",
            "rounds_played": f"{arc['rounds_played']:,}",
            "coins": f"{arc['coins']:,}",
            "top_games": arc["top_games"],
        }
        url = await self._render("arcade", data)
        if url:
            yield event.image_result(url)
        else:
            msg = f"=== 街机游戏 [{arc['display_name']}] ==={SEP}"
            msg += f"总胜场: {arc['wins']:,}  总回合: {arc['rounds_played']:,}  硬币: {arc['coins']:,}{SEP}"
            if arc["top_games"]:
                msg += "热门小游戏:\n"
                for gname, gwins in arc["top_games"][:5]:
                    msg += f"  {gname}: {gwins} 胜\n"
            yield event.plain_result(msg)

    async def _handle_zombies(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            z = await self.client.get_zombies_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取丧尸末日数据失败: {e}")
            return

        maps_list = list(z["maps"].items())
        data = {
            "display_name": z["display_name"],
            "wins": f"{z['wins']:,}",
            "losses": f"{z['losses']:,}",
            "kills": f"{z['kills']:,}",
            "deaths": f"{z['deaths']:,}",
            "headshots": f"{z['headshots']:,}",
            "games_played": f"{z['games_played']:,}",
            "doors_opened": f"{z['doors_opened']:,}",
            "chests_looted": f"{z['chests_looted']:,}",
            "rounds_survived": f"{z['rounds_survived']:,}",
            "best_round": str(z["best_round"]),
            "maps": maps_list,
        }
        url = await self._render("zombies", data)
        if url:
            yield event.image_result(url)
        else:
            kdr = calc_kdr(z["kills"], z["deaths"])
            wlr = calc_wlr(z["wins"], z["losses"])
            msg = f"=== 丧尸末日 [{z['display_name']}] ==={SEP}"
            msg += f"场次: {z['games_played']:,}  胜场: {z['wins']:,}  败场: {z['losses']:,}{SEP}"
            msg += f"击杀: {z['kills']:,}  死亡: {z['deaths']:,}  K/D: {kdr}  W/L: {wlr}{SEP}"
            msg += f"爆头: {z['headshots']:,}  开门: {z['doors_opened']:,}  开箱: {z['chests_looted']:,}{SEP}"
            msg += f"总生存回合: {z['rounds_survived']:,}  最佳回合: {z['best_round']}{SEP}"
            msg += "地图记录:\n"
            for mname, mround in z["maps"].items():
                msg += f"  {mname}: 最佳 {mround} 回合\n"
            yield event.plain_result(msg)

    async def _handle_party(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            p = await self.client.get_party_games_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取小游戏派对数据失败: {e}")
            return

        data = {
            "display_name": p["display_name"],
            "round_wins": f"{p['round_wins']:,}",
            "total_rounds": f"{p['total_rounds']:,}",
            "mini_games": p["mini_games"],
        }
        url = await self._render("party", data)
        if url:
            yield event.image_result(url)
        else:
            msg = f"=== 小游戏派对 [{p['display_name']}] ==={SEP}"
            msg += f"回合胜场: {p['round_wins']:,}  总回合: {p['total_rounds']:,}{SEP}"
            if p["mini_games"]:
                msg += "各小游戏胜场:\n"
                for gname, gwins in p["mini_games"]:
                    msg += f"  {gname}: {gwins}\n"
            yield event.plain_result(msg)

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()
