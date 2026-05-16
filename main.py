import os
from datetime import datetime, timezone

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import *

from .hypixel_client import HypixelClient


TPL_DIR = os.path.join(os.path.dirname(__file__), "templates")


def calc_network_level(exp: int) -> int:
    if exp <= 0: return 1
    level, need = 1, 2500
    while exp >= need:
        exp -= need; level += 1; need += 2500
    return level

def fmt_num(n: int) -> str: return f"{n:,}"

def calc_fkdr(fk, fd): return f"{fk / fd:.2f}" if fd else f"{fk:.2f}"
def calc_kdr(k, d): return f"{k / d:.2f}" if d else f"{k:.2f}"
def calc_wlr(w, l): return f"{w / l:.2f}" if l else f"{w:.2f}"

def ts_to_str(ts: int) -> str:
    if ts == 0: return "N/A"
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


SEP = "\n" + "─" * 36 + "\n"


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

    def _is_banned(self, event: AstrMessageEvent) -> bool:
        gid, uid = event.get_group_id(), event.get_sender_id()
        bg = [str(x) for x in self.config.get("ban_groups", [])]
        bu = [str(x) for x in self.config.get("ban_users", [])]
        if gid and str(gid) in bg: return True
        if uid and str(uid) in bu: return True
        return False

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

        sub, arg = parts[1], parts[2] if len(parts) > 2 else ""

        if sub == "setkey":
            if not arg:
                yield event.plain_result("请输入 API 密钥"); return
            self.config["api_key"] = arg
            self.config.save_config()
            self.client = HypixelClient(arg)
            logger.info(f"API Key 已更新（{event.get_sender_id()}）")
            yield event.plain_result("API Key 已保存!"); return

        handlers = {
            "player": self._handle_player, "bedwars": self._handle_bedwars,
            "skywars": self._handle_skywars, "arcade": self._handle_arcade,
            "zombies": self._handle_zombies, "party": self._handle_party,
        }
        h = handlers.get(sub)
        if not h:
            yield event.plain_result(f"未知命令: {sub}"); return
        if not arg:
            yield event.plain_result(f"请输入玩家ID: /hypixel {sub} <ID>"); return

        s, u, g = event.get_sender_name(), event.get_sender_id(), event.get_group_id()
        ctx = f"用户 {s}({u})" + (f" 在群 {g}" if g else "")
        logger.info(f"查询 {sub} {arg} — {ctx}")

        async for r in h(event, arg):
            yield r

    async def _handle_player(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            info = await self.client.get_player_rank_info(name=name)
        except Exception as e:
            logger.info(f"查询玩家 {name} 失败: {e}")
            yield event.plain_result(f"获取玩家信息失败: {e}"); return
        level = calc_network_level(info.get("network_level", 0))
        yield event.plain_result(
            f"━━━━ 玩家信息 ━━━━\n\n"
            f"  {info['display_name']}  —  Lv.{level}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"  UUID   │ {info['uuid']}\n"
            f"  Rank   │ {info.get('rank', 'NONE')}\n"
            f"  Karma  │ {fmt_num(info.get('karma', 0))}\n"
            f"  语言    │ {info.get('language', 'N/A')}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"  首次登录  {ts_to_str(info.get('first_login', 0))}\n"
            f"  最近活跃  {ts_to_str(info.get('last_login', 0))}"
        )

    async def _handle_bedwars(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            bw = await self.client.get_bedwars_stats(name=name)
        except Exception as e:
            logger.info(f"起床战争 {name} 失败: {e}")
            yield event.plain_result(f"获取起床战争数据失败: {e}"); return
        fkdr = calc_fkdr(bw["final_kills"], bw["final_deaths"])
        kdr = calc_kdr(bw["kills"], bw["deaths"])
        wlr = calc_wlr(bw["wins"], bw["losses"])
        yield event.plain_result(
            f"━━━━ 起床战争 ━━━━\n\n"
            f"  {bw['display_name']}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"  等级    │ {fmt_num(bw['level'])}          硬币  │ {fmt_num(bw['coins'])}\n"
            f"  胜场    │ {fmt_num(bw['wins'])}          败场  │ {fmt_num(bw['losses'])}\n"
            f"  W/L    │ {wlr}\n\n"
            f"  击杀    │ {fmt_num(bw['kills'])}          死亡  │ {fmt_num(bw['deaths'])}\n"
            f"  K/D    │ {kdr}\n\n"
            f"  最终击杀 │ {fmt_num(bw['final_kills'])}        最终死亡 │ {fmt_num(bw['final_deaths'])}\n"
            f"  FKDR   │ {fkdr}\n\n"
            f"  拆床    │ {fmt_num(bw['beds_broken'])}          丢床  │ {fmt_num(bw['beds_lost'])}\n"
            f"  连胜    │ {bw['winstreak']}\n"
            f"  总场次  │ {fmt_num(bw['games_played'])}"
        )

    async def _handle_skywars(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            sw = await self.client.get_skywars_stats(name=name)
        except Exception as e:
            logger.info(f"空岛战争 {name} 失败: {e}")
            yield event.plain_result(f"获取空岛战争数据失败: {e}"); return
        kdr = calc_kdr(sw["kills"], sw["deaths"]); wlr = calc_wlr(sw["wins"], sw["losses"])
        yield event.plain_result(
            f"━━━━ 空岛战争 ━━━━\n\n"
            f"  {sw['display_name']}  —  Lv.{sw['level']}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"  胜场    │ {fmt_num(sw['wins'])}          败场  │ {fmt_num(sw['losses'])}\n"
            f"  W/L    │ {wlr}\n\n"
            f"  击杀    │ {fmt_num(sw['kills'])}          死亡  │ {fmt_num(sw['deaths'])}\n"
            f"  K/D    │ {kdr}\n\n"
            f"  Souls  │ {fmt_num(sw['souls'])}          Heads │ {fmt_num(sw['heads'])}\n"
            f"  总场次  │ {fmt_num(sw['games_played'])}\n"
            f"  硬币    │ {fmt_num(sw['coins'])}"
        )

    async def _handle_arcade(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            arc = await self.client.get_arcade_stats(name=name)
        except Exception as e:
            logger.info(f"街机 {name} 失败: {e}")
            yield event.plain_result(f"获取街机数据失败: {e}"); return
        msg = (
            f"━━━━ 街机游戏 ━━━━\n\n"
            f"  {arc['display_name']}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"  总胜场  │ {fmt_num(arc['wins'])}\n"
            f"  总回合  │ {fmt_num(arc['rounds_played'])}\n"
            f"  硬币    │ {fmt_num(arc['coins'])}\n\n"
        )
        if arc["top_games"]:
            msg += "热门小游戏:\n" + "\n".join(f"  └ {g}  —  {w} 胜" for g, w in arc["top_games"][:5])
        yield event.plain_result(msg)

    async def _handle_zombies(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            z = await self.client.get_zombies_stats(name=name)
        except Exception as e:
            logger.info(f"丧尸末日 {name} 失败: {e}")
            yield event.plain_result(f"获取丧尸末日数据失败: {e}"); return
        kdr = calc_kdr(z["kills"], z["deaths"]); wlr = calc_wlr(z["wins"], z["losses"])
        msg = (
            f"━━━━ 丧尸末日 ━━━━\n\n"
            f"  {z['display_name']}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"  场次    │ {fmt_num(z['games_played'])}\n"
            f"  胜场    │ {fmt_num(z['wins'])}          败场  │ {fmt_num(z['losses'])}\n"
            f"  W/L    │ {wlr}\n\n"
            f"  击杀    │ {fmt_num(z['kills'])}          死亡  │ {fmt_num(z['deaths'])}\n"
            f"  K/D    │ {kdr}\n"
            f"  爆头    │ {fmt_num(z['headshots'])}\n\n"
            f"  开门    │ {fmt_num(z['doors_opened'])}         开箱  │ {fmt_num(z['chests_looted'])}\n"
            f"  生存回合 │ {fmt_num(z['rounds_survived'])}        最佳  │ {z['best_round']}\n\n"
        )
        if z["maps"]:
            msg += "地图记录:\n" + "\n".join(f"  └ {m}  —  最佳 {r} 回合" for m, r in z["maps"].items())
        yield event.plain_result(msg)

    async def _handle_party(self, event, name):
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        try:
            p = await self.client.get_party_games_stats(name=name)
        except Exception as e:
            logger.info(f"小游戏派对 {name} 失败: {e}")
            yield event.plain_result(f"获取小游戏派对数据失败: {e}"); return
        msg = (
            f"━━━━ 小游戏派对 ━━━━\n\n"
            f"  {p['display_name']}\n\n"
            f"━━━━━━━━━━━━━━━━\n\n"
            f"  回合胜场  │ {fmt_num(p['round_wins'])}\n"
            f"  总回合    │ {fmt_num(p['total_rounds'])}\n\n"
        )
        if p["mini_games"]:
            msg += "各小游戏胜场:\n" + "\n".join(f"  └ {g}  —  {w}" for g, w in p["mini_games"])
        yield event.plain_result(msg)

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()
