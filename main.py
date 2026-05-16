from datetime import datetime, timezone

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import *

from .hypixel_client import HypixelClient


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


@register("astrbot_plugin_hypixel_api", "bi_xiaoyang2", "Hypixel 玩家数据查询插件", "1.0.0")
class HypixelPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        api_key = self.config.get("api_key", "")
        if api_key:
            self.client = HypixelClient(api_key)
        else:
            self.client = None

    async def _img_or_text(self, event: AstrMessageEvent, text: str):
        try:
            url = await self.text_to_image(text)
            yield event.image_result(url)
        except Exception:
            yield event.plain_result(text)

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
        text = (
            "━━━━ 玩家信息 ━━━━\n\n"
            f"  {info['display_name']}  —  Lv.{level}\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"  UUID   │ {info['uuid']}\n"
            f"  Rank   │ {info.get('rank', 'NONE')}\n"
            f"  Karma  │ {info.get('karma', 0):,}\n"
            f"  语言    │ {info.get('language', 'N/A')}\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"  首次登录  {ts_to_str(info.get('first_login', 0))}\n"
            f"  最近活跃  {ts_to_str(info.get('last_login', 0))}"
        )
        async for result in self._img_or_text(event, text):
            yield result

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
        text = (
            "━━━━ 起床战争 ━━━━\n\n"
            f"  {bw['display_name']}\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"  等级    │ {bw['level']:,}          硬币  │ {bw['coins']:,}\n"
            f"  胜场    │ {bw['wins']:,}          败场  │ {bw['losses']:,}\n"
            f"  W/L    │ {wlr}\n\n"
            f"  击杀    │ {bw['kills']:,}          死亡  │ {bw['deaths']:,}\n"
            f"  K/D    │ {kdr}\n\n"
            f"  最终击杀 │ {bw['final_kills']:,}        最终死亡 │ {bw['final_deaths']:,}\n"
            f"  FKDR   │ {fkdr}\n\n"
            f"  拆床    │ {bw['beds_broken']:,}          丢床  │ {bw['beds_lost']:,}\n"
            f"  连胜    │ {bw['winstreak']}\n"
            f"  总场次  │ {bw['games_played']:,}"
        )
        async for result in self._img_or_text(event, text):
            yield result

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
        text = (
            "━━━━ 空岛战争 ━━━━\n\n"
            f"  {sw['display_name']}  —  Lv.{sw['level']}\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"  胜场    │ {sw['wins']:,}          败场  │ {sw['losses']:,}\n"
            f"  W/L    │ {wlr}\n\n"
            f"  击杀    │ {sw['kills']:,}          死亡  │ {sw['deaths']:,}\n"
            f"  K/D    │ {kdr}\n\n"
            f"  Souls  │ {sw['souls']:,}          Heads │ {sw['heads']:,}\n"
            f"  总场次  │ {sw['games_played']:,}\n"
            f"  硬币    │ {sw['coins']:,}"
        )
        async for result in self._img_or_text(event, text):
            yield result

    async def _handle_arcade(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            arc = await self.client.get_arcade_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取街机数据失败: {e}")
            return

        text = (
            "━━━━ 街机游戏 ━━━━\n\n"
            f"  {arc['display_name']}\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"  总胜场  │ {arc['wins']:,}\n"
            f"  总回合  │ {arc['rounds_played']:,}\n"
            f"  硬币    │ {arc['coins']:,}\n\n"
        )
        if arc["top_games"]:
            text += "热门小游戏:\n"
            for gname, gwins in arc["top_games"][:5]:
                text += f"  └ {gname}  —  {gwins} 胜\n"
        async for result in self._img_or_text(event, text):
            yield result

    async def _handle_zombies(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            z = await self.client.get_zombies_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取丧尸末日数据失败: {e}")
            return

        kdr = calc_kdr(z["kills"], z["deaths"])
        wlr = calc_wlr(z["wins"], z["losses"])
        text = (
            "━━━━ 丧尸末日 ━━━━\n\n"
            f"  {z['display_name']}\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"  场次    │ {z['games_played']:,}\n"
            f"  胜场    │ {z['wins']:,}          败场  │ {z['losses']:,}\n"
            f"  W/L    │ {wlr}\n\n"
            f"  击杀    │ {z['kills']:,}          死亡  │ {z['deaths']:,}\n"
            f"  K/D    │ {kdr}\n"
            f"  爆头    │ {z['headshots']:,}\n\n"
            f"  开门    │ {z['doors_opened']:,}         开箱  │ {z['chests_looted']:,}\n"
            f"  生存回合 │ {z['rounds_survived']:,}        最佳  │ {z['best_round']}\n\n"
        )
        if z["maps"]:
            text += "地图记录:\n"
            for mname, mround in z["maps"].items():
                text += f"  └ {mname}  —  最佳 {mround} 回合\n"
        async for result in self._img_or_text(event, text):
            yield result

    async def _handle_party(self, event: AstrMessageEvent, name: str):
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置")
            return
        try:
            p = await self.client.get_party_games_stats(name=name)
        except Exception as e:
            yield event.plain_result(f"获取小游戏派对数据失败: {e}")
            return

        text = (
            "━━━━ 小游戏派对 ━━━━\n\n"
            f"  {p['display_name']}\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            f"  回合胜场  │ {p['round_wins']:,}\n"
            f"  总回合    │ {p['total_rounds']:,}\n\n"
        )
        if p["mini_games"]:
            text += "各小游戏胜场:\n"
            for gname, gwins in p["mini_games"]:
                text += f"  └ {gname}  —  {gwins}\n"
        async for result in self._img_or_text(event, text):
            yield result

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()
