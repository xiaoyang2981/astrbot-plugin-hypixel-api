from datetime import datetime, timezone

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import *

from .hypixel_client import HypixelClient
from .renderer import PLAYER_TMPL, BEDWARS_TMPL, SKYWARS_TMPL, get_initials


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
        xp_table.append(xp_table[-1] + 5000)  # simplified star calculation
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
            logger.info("Hypixel API 客户端已初始化")
        else:
            self.client = None
            logger.warning("Hypixel API Key 未配置，请使用 /hypixel setkey <key> 设置")

    def _get_client(self, event: AstrMessageEvent) -> HypixelClient | None:
        if self.client is None:
            return None
        return self.client

    @filter.command("hypixel")
    async def hypixel(self, event: AstrMessageEvent):
        message_str = event.message_str.strip()
        parts = message_str.split(maxsplit=2)

        if len(parts) < 2:
            yield event.plain_result(
                "Hypixel 查询插件\n\n"
                "用法:\n"
                "  /hypixel player <游戏ID>  - 查看玩家基本信息\n"
                "  /hypixel bedwars <游戏ID> - 查看 BedWars 数据\n"
                "  /hypixel skywars <游戏ID> - 查看 SkyWars 数据\n"
                "  /hypixel setkey <API密钥> - 设置 API Key"
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

        if sub == "player":
            if not arg:
                yield event.plain_result("请输入玩家游戏ID: /hypixel player <ID>")
                return
            async for result in self._handle_player(event, arg):
                yield result
            return

        if sub == "bedwars":
            if not arg:
                yield event.plain_result("请输入玩家游戏ID: /hypixel bedwars <ID>")
                return
            async for result in self._handle_bedwars(event, arg):
                yield result
            return

        if sub == "skywars":
            if not arg:
                yield event.plain_result("请输入玩家游戏ID: /hypixel skywars <ID>")
                return
            async for result in self._handle_skywars(event, arg):
                yield result
            return

        yield event.plain_result(f"未知子命令: {sub}\n请使用 /hypixel 查看帮助。")

    async def _handle_player(self, event: AstrMessageEvent, name: str):
        client = self.client
        if client is None:
            yield event.plain_result("Hypixel API Key 未配置。请使用 /hypixel setkey <API密钥> 进行设置。")
            return

        try:
            info = await client.get_player_rank_info(name=name)
        except Exception as e:
            logger.error(f"获取玩家信息失败: {e}")
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
        try:
            url = await self.html_render(PLAYER_TMPL, data)
            yield event.image_result(url)
        except Exception as e:
            logger.error(f"渲染图片失败: {e}")
            yield event.plain_result("渲染图片失败，请检查 Playwright 是否正确安装。")

    async def _handle_bedwars(self, event: AstrMessageEvent, name: str):
        client = self.client
        if client is None:
            yield event.plain_result("Hypixel API Key 未配置。请使用 /hypixel setkey <API密钥> 进行设置。")
            return

        try:
            bw = await client.get_bedwars_stats(name=name)
        except Exception as e:
            logger.error(f"获取 BedWars 数据失败: {e}")
            yield event.plain_result(f"获取 BedWars 数据失败: {e}")
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
        try:
            url = await self.html_render(BEDWARS_TMPL, data)
            yield event.image_result(url)
        except Exception as e:
            logger.error(f"渲染图片失败: {e}")
            yield event.plain_result("渲染图片失败，请检查 Playwright 是否正确安装。")

    async def _handle_skywars(self, event: AstrMessageEvent, name: str):
        client = self.client
        if client is None:
            yield event.plain_result("Hypixel API Key 未配置。请使用 /hypixel setkey <API密钥> 进行设置。")
            return

        try:
            sw = await client.get_skywars_stats(name=name)
        except Exception as e:
            logger.error(f"获取 SkyWars 数据失败: {e}")
            yield event.plain_result(f"获取 SkyWars 数据失败: {e}")
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
        try:
            url = await self.html_render(SKYWARS_TMPL, data)
            yield event.image_result(url)
        except Exception as e:
            logger.error(f"渲染图片失败: {e}")
            yield event.plain_result("渲染图片失败，请检查 Playwright 是否正确安装。")

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()