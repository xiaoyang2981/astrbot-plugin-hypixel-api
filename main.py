import os
import json
import asyncio
from datetime import datetime, timezone

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import *

from .hypixel_client import HypixelClient


CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


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


@register("astrbot_plugin_hypixel_api", "AstrBot-Plugin-Dev", "Hypixel 玩家数据查询插件", "1.0.0")
class HypixelPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        config = load_config()
        api_key = config.get("api_key", "")
        if api_key:
            self.client = HypixelClient(api_key)
            logger.info("Hypixel API 客户端已初始化")
        else:
            self.client = None
            logger.warning("Hypixel API Key 未配置，请使用 /hypixel setkey <key> 设置")

    async def _get_client(self, event: AstrMessageEvent) -> HypixelClient | None:
        if self.client is None:
            yield event.plain_result("Hypixel API Key 未配置。请使用 /hypixel setkey <API密钥> 进行设置。")
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
            config = load_config()
            config["api_key"] = arg
            save_config(config)
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

        msg = (
            f"玩家: {info['display_name']}\n"
            f"UUID: {info['uuid']}\n"
            f"等级: {info.get('rank', 'NONE')} (MVP++颜色: {info.get('mvp_plus_color', 'NONE')})\n"
            f"网络等级: {level}\n"
            f"Karma: {info.get('karma', 0):,}\n"
            f"语言: {info.get('language', 'N/A')}\n"
            f"首次登录: {ts_to_str(info.get('first_login', 0))}\n"
            f"最近登录: {ts_to_str(info.get('last_login', 0))}\n"
        )
        yield event.plain_result(msg)

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

        msg = (
            f"BedWars - {bw['display_name']}\n"
            f"等级 (Exp): {bw['level']:,}\n"
            f"胜场: {bw['wins']:,}  |  败场: {bw['losses']:,}\n"
            f"W/L: {wlr}\n"
            f"总击杀: {bw['kills']:,}  总死亡: {bw['deaths']:,}\n"
            f"K/D: {kdr}\n"
            f"最终击杀: {bw['final_kills']:,}  最终死亡: {bw['final_deaths']:,}\n"
            f"FKDR: {fkdr}\n"
            f"拆床: {bw['beds_broken']:,}  丢床: {bw['beds_lost']:,}\n"
            f"游戏场次: {bw['games_played']:,}\n"
            f"连胜: {bw['winstreak']}\n"
            f"硬币: {bw['coins']:,}\n"
        )
        yield event.plain_result(msg)

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

        msg = (
            f"SkyWars - {sw['display_name']}\n"
            f"等级: {sw['level']}\n"
            f"胜场: {sw['wins']:,}  败场: {sw['losses']:,}\n"
            f"W/L: {wlr}\n"
            f"击杀: {sw['kills']:,}  死亡: {sw['deaths']:,}\n"
            f"K/D: {kdr}\n"
            f"游戏场次: {sw['games_played']:,}\n"
            f"Souls: {sw['souls']:,}\n"
            f"硬币: {sw['coins']:,}\n"
            f"Heads: {sw['heads']:,}\n"
        )
        yield event.plain_result(msg)

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()