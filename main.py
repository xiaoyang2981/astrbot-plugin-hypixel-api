import os
from datetime import datetime, timezone

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import *

from .hypixel_client import HypixelClient


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


def calc_network_level(exp: int) -> int:
    if exp <= 0:
        return 1
    level = 1
    need = 2500
    while exp >= need:
        exp -= need
        level += 1
        need += 2500
    return level

def calc_fkdr(fk, fd):
    return f"{fk / fd:.2f}" if fd else f"{fk:.2f}"
def calc_kdr(k, d):
    return f"{k / d:.2f}" if d else f"{k:.2f}"
def calc_wlr(w, l):
    return f"{w / l:.2f}" if l else f"{w:.2f}"

def ts_to_str(ts: int) -> str:
    if ts == 0: return "N/A"
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

def fmt_num(n: int) -> str:
    return f"{n:,}"


def load_templates():
    tpls = {}
    for name in ("player", "bedwars", "skywars", "arcade", "zombies", "party"):
        path = os.path.join(TEMPLATE_DIR, f"{name}.html")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                tpls[name] = f.read()
    return tpls


@register("astrbot_plugin_hypixel_api", "bi_xiaoyang2", "Hypixel 玩家数据查询插件", "1.0.0")
class HypixelPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self._templates: dict[str, str] = {}

    async def initialize(self):
        self._templates = load_templates()
        names = ", ".join(self._templates.keys())
        logger.info(f"已加载 HTML 模板: {names}")

        api_key = self.config.get("api_key", "")
        if api_key:
            self.client = HypixelClient(api_key)
            logger.info("Hypixel API 客户端已初始化")
        else:
            self.client = None
            logger.warning("Hypixel API Key 未配置")

    def _is_banned(self, event: AstrMessageEvent) -> bool:
        gid = event.get_group_id()
        uid = event.get_sender_id()
        bg = [str(x) for x in self.config.get("ban_groups", [])]
        bu = [str(x) for x in self.config.get("ban_users", [])]
        if gid and str(gid) in bg:
            logger.info(f"群组 {gid} 在黑名单中，已拦截"); return True
        if uid and str(uid) in bu:
            logger.info(f"用户 {uid} 在黑名单中，已拦截"); return True
        return False

    async def _render(self, kind: str, data: dict) -> str | None:
        mode = self.config.get("render_mode", "auto")
        if mode == "text":
            return None
        tmpl = self._templates.get(kind)
        if not tmpl:
            return None
        try:
            return await self.html_render(tmpl, data, options={"scale": "css", "type": "png"})
        except Exception as e:
            logger.info(f"HTML 渲染失败: {e}")
            return None

    @filter.command("hypixel")
    async def hypixel(self, event: AstrMessageEvent):
        if self._is_banned(event):
            return

        msg = event.message_str.strip()
        parts = msg.split(maxsplit=2)

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
            logger.info(f"API Key 已更新（由 {event.get_sender_id()} 设置）")
            yield event.plain_result("Hypixel API Key 已设置并保存!")
            return

        handlers = {
            "player": self._handle_player, "bedwars": self._handle_bedwars,
            "skywars": self._handle_skywars, "arcade": self._handle_arcade,
            "zombies": self._handle_zombies, "party": self._handle_party,
        }
        handler = handlers.get(sub)
        if not handler:
            yield event.plain_result(f"未知子命令: {sub}\n请使用 /hypixel 查看帮助。")
            return
        if not arg:
            yield event.plain_result(f"请输入玩家游戏ID: /hypixel {sub} <ID>")
            return

        s = event.get_sender_name()
        u = event.get_sender_id()
        g = event.get_group_id()
        ctx = f"用户 {s}({u})" + (f" 在群 {g}" if g else "")
        logger.info(f"查询 {sub} {arg} — {ctx}")

        async for result in handler(event, arg):
            yield result

    async def _output(self, event, url, text):
        if url:
            yield event.image_result(url)
        else:
            try:
                u = await self.text_to_image(text)
                yield event.image_result(u)
            except Exception:
                yield event.plain_result(text)

    async def _handle_player(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            info = await self.client.get_player_rank_info(name=name)
        except Exception as e:
            logger.info(f"查询玩家 {name} 失败: {e}")
            yield event.plain_result(f"获取玩家信息失败: {e}"); return

        level = calc_network_level(info.get("network_level", 0))
        data = dict(
            initials=(info["display_name"][:2].upper() if info["display_name"] else "?"),
            display_name=info["display_name"],
            rank_display=info.get("rank", "NONE"),
            level=level, uuid=info["uuid"], language=info.get("language", "N/A"),
            karma=fmt_num(info.get("karma", 0)), rank=info.get("rank", "NONE"),
            first_login=ts_to_str(info.get("first_login", 0)),
            last_login=ts_to_str(info.get("last_login", 0)),
        )
        fb = (f"玩家: {info['display_name']} Lv.{level}  Rank: {info.get('rank','NONE')}\n"
              f"UUID: {info['uuid']}  Karma: {fmt_num(info.get('karma',0))}  语言: {info.get('language','N/A')}\n"
              f"首次登录: {ts_to_str(info.get('first_login',0))}\n"
              f"最近活跃: {ts_to_str(info.get('last_login',0))}")
        url = await self._render("player", data)
        async for r in self._output(event, url, fb):
            yield r

    async def _handle_bedwars(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            bw = await self.client.get_bedwars_stats(name=name)
        except Exception as e:
            logger.info(f"查询起床战争 {name} 失败: {e}")
            yield event.plain_result(f"获取起床战争数据失败: {e}"); return

        fkdr = calc_fkdr(bw["final_kills"], bw["final_deaths"])
        kdr = calc_kdr(bw["kills"], bw["deaths"])
        wlr = calc_wlr(bw["wins"], bw["losses"])
        data = dict(
            display_name=bw["display_name"], level=fmt_num(bw["level"]),
            wins=fmt_num(bw["wins"]), losses=fmt_num(bw["losses"]),
            final_kills=fmt_num(bw["final_kills"]), final_deaths=fmt_num(bw["final_deaths"]),
            fkdr=fkdr, kdr=kdr, wlr=wlr,
            beds_broken=fmt_num(bw["beds_broken"]), beds_lost=fmt_num(bw["beds_lost"]),
            winstreak=str(bw["winstreak"]), games_played=fmt_num(bw["games_played"]),
        )
        fb = (f"起床战争 [{bw['display_name']}]  等级: {fmt_num(bw['level'])}  硬币: {fmt_num(bw['coins'])}\n"
              f"胜场: {fmt_num(bw['wins'])}  败场: {fmt_num(bw['losses'])}  W/L: {wlr}\n"
              f"击杀: {fmt_num(bw['kills'])}  死亡: {fmt_num(bw['deaths'])}  K/D: {kdr}\n"
              f"最终击杀: {fmt_num(bw['final_kills'])}  最终死亡: {fmt_num(bw['final_deaths'])}  FKDR: {fkdr}\n"
              f"拆床: {fmt_num(bw['beds_broken'])}  丢床: {fmt_num(bw['beds_lost'])}\n"
              f"连胜: {bw['winstreak']}  总场次: {fmt_num(bw['games_played'])}")
        url = await self._render("bedwars", data)
        async for r in self._output(event, url, fb):
            yield r

    async def _handle_skywars(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            sw = await self.client.get_skywars_stats(name=name)
        except Exception as e:
            logger.info(f"查询空岛战争 {name} 失败: {e}")
            yield event.plain_result(f"获取空岛战争数据失败: {e}"); return

        kdr = calc_kdr(sw["kills"], sw["deaths"])
        wlr = calc_wlr(sw["wins"], sw["losses"])
        data = dict(
            display_name=sw["display_name"], level=sw["level"],
            wins=fmt_num(sw["wins"]), losses=fmt_num(sw["losses"]),
            kills=fmt_num(sw["kills"]), deaths=fmt_num(sw["deaths"]),
            kdr=kdr, wlr=wlr, souls=fmt_num(sw["souls"]),
            games_played=fmt_num(sw["games_played"]), heads=fmt_num(sw["heads"]),
        )
        fb = (f"空岛战争 [{sw['display_name']}] Lv.{sw['level']}\n"
              f"胜场: {fmt_num(sw['wins'])}  败场: {fmt_num(sw['losses'])}  W/L: {wlr}\n"
              f"击杀: {fmt_num(sw['kills'])}  死亡: {fmt_num(sw['deaths'])}  K/D: {kdr}\n"
              f"Souls: {fmt_num(sw['souls'])}  Heads: {fmt_num(sw['heads'])}\n"
              f"总场次: {fmt_num(sw['games_played'])}  硬币: {fmt_num(sw['coins'])}")
        url = await self._render("skywars", data)
        async for r in self._output(event, url, fb):
            yield r

    async def _handle_arcade(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            arc = await self.client.get_arcade_stats(name=name)
        except Exception as e:
            logger.info(f"查询街机游戏 {name} 失败: {e}")
            yield event.plain_result(f"获取街机数据失败: {e}"); return

        data = dict(
            display_name=arc["display_name"],
            wins=fmt_num(arc["wins"]), rounds_played=fmt_num(arc["rounds_played"]),
            coins=fmt_num(arc["coins"]), top_games=arc["top_games"],
        )
        fb = (f"街机游戏 [{arc['display_name']}]\n"
              f"总胜场: {fmt_num(arc['wins'])}  总回合: {fmt_num(arc['rounds_played'])}  硬币: {fmt_num(arc['coins'])}")
        if arc["top_games"]:
            fb += "\n热门小游戏:\n" + "\n".join(f"  {g}: {w}胜" for g, w in arc["top_games"][:5])
        url = await self._render("arcade", data)
        async for r in self._output(event, url, fb):
            yield r

    async def _handle_zombies(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            z = await self.client.get_zombies_stats(name=name)
        except Exception as e:
            logger.info(f"查询丧尸末日 {name} 失败: {e}")
            yield event.plain_result(f"获取丧尸末日数据失败: {e}"); return

        kdr = calc_kdr(z["kills"], z["deaths"])
        wlr = calc_wlr(z["wins"], z["losses"])
        data = dict(
            display_name=z["display_name"],
            wins=fmt_num(z["wins"]), losses=fmt_num(z["losses"]),
            kills=fmt_num(z["kills"]), deaths=fmt_num(z["deaths"]),
            headshots=fmt_num(z["headshots"]),
            games_played=fmt_num(z["games_played"]),
            doors_opened=fmt_num(z["doors_opened"]), chests_looted=fmt_num(z["chests_looted"]),
            rounds_survived=fmt_num(z["rounds_survived"]), best_round=str(z["best_round"]),
            maps=list(z["maps"].items()),
        )
        fb = (f"丧尸末日 [{z['display_name']}]\n"
              f"场次: {fmt_num(z['games_played'])}  胜场: {fmt_num(z['wins'])}  败场: {fmt_num(z['losses'])}\n"
              f"击杀: {fmt_num(z['kills'])}  死亡: {fmt_num(z['deaths'])}  K/D: {kdr}\n"
              f"爆头: {fmt_num(z['headshots'])}  开门: {fmt_num(z['doors_opened'])}  开箱: {fmt_num(z['chests_looted'])}\n"
              f"总生存回合: {fmt_num(z['rounds_survived'])}  最佳回合: {z['best_round']}")
        if z["maps"]:
            fb += "\n地图记录:\n" + "\n".join(f"  {m}: 最佳 {r} 回合" for m, r in z["maps"].items())
        url = await self._render("zombies", data)
        async for r in self._output(event, url, fb):
            yield r

    async def _handle_party(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            p = await self.client.get_party_games_stats(name=name)
        except Exception as e:
            logger.info(f"查询小游戏派对 {name} 失败: {e}")
            yield event.plain_result(f"获取小游戏派对数据失败: {e}"); return

        data = dict(
            display_name=p["display_name"],
            round_wins=fmt_num(p["round_wins"]), total_rounds=fmt_num(p["total_rounds"]),
            mini_games=p["mini_games"],
        )
        fb = (f"小游戏派对 [{p['display_name']}]\n"
              f"回合胜场: {fmt_num(p['round_wins'])}  总回合: {fmt_num(p['total_rounds'])}")
        if p["mini_games"]:
            fb += "\n各小游戏胜场:\n" + "\n".join(f"  {g}: {w}" for g, w in p["mini_games"])
        url = await self._render("party", data)
        async for r in self._output(event, url, fb):
            yield r

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()
