from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.api.message_components import *

from .hypixel import HypixelClient
from .bjd import BuGLandClient

import commands.player as player_cmd
import commands.bedwars as bedwars_cmd
import commands.skywars as skywars_cmd
import commands.arcade as arcade_cmd
import commands.zombies as zombies_cmd
import commands.party as party_cmd
import commands.bjd_blitz as blitz_cmd


@register("astrbot_plugin_hypixel_api", "bi_xiaoyang2", "Hypixel + BuGLand 数据查询插件", "1.0.0")
class HypixelPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        api_key = self.config.get("api_key", "")
        self.client = HypixelClient(api_key) if api_key else None
        if self.client:
            logger.info("Hypixel API 客户端已初始化")
        else:
            logger.warning("Hypixel API Key 未配置")

        bjd_token = self.config.get("bjd_token", "")
        self.bjd = BuGLandClient(bjd_token) if bjd_token else None
        if self.bjd:
            logger.info("BuGLand API 客户端已初始化")
        else:
            logger.warning("BuGLand Token 未配置，布吉岛查询不可用")

    def _is_banned(self, event: AstrMessageEvent) -> bool:
        gid, uid = event.get_group_id(), event.get_sender_id()
        bg = [str(x) for x in self.config.get("ban_groups", [])]
        bu = [str(x) for x in self.config.get("ban_users", [])]
        return (gid and str(gid) in bg) or (uid and str(uid) in bu)

    def _log(self, event, sub, arg):
        s, u, g = event.get_sender_name(), event.get_sender_id(), event.get_group_id()
        ctx = f"用户 {s}({u})" + (f" 在群 {g}" if g else "")
        logger.info(f"查询 {sub} {arg} — {ctx}")

    @filter.command("hypixel")
    async def hypixel(self, event: AstrMessageEvent):
        if self._is_banned(event):
            return
        msg = event.message_str.strip()
        parts = msg.split(maxsplit=2)

        if len(parts) < 2:
            yield event.plain_result(
                "📊 Hypixel + BuGLand 数据查询\n\n"
                "📋 用法:\n"
                "  🔍 /hypixel player <ID>   - 玩家基本信息\n"
                "  🛏️ /hypixel bedwars <ID>  - 起床战争数据\n"
                "  🌌 /hypixel skywars <ID>  - 空岛战争数据\n"
                "  🕹️ /hypixel arcade <ID>   - 街机游戏总览\n"
                "  🧟 /hypixel zombies <ID>  - 丧尸末日数据\n"
                "  🎉 /hypixel party <ID>    - 小游戏派对数据\n"
                "  ⚔️ /hypixel blitz <ID>    - 布吉岛数据\n"
                "  🔑 /hypixel setkey <key>  - 设置 Hypixel API Key\n"
                "  🔑 /hypixel bjdkey <key>  - 设置 BuGLand Token"
            )
            return

        sub, arg = parts[1], parts[2] if len(parts) > 2 else ""

        if sub == "setkey":
            if not arg:
                yield event.plain_result("请输入 Hypixel API 密钥"); return
            self.config["api_key"] = arg
            self.config.save_config()
            self.client = HypixelClient(arg)
            logger.info(f"Hypixel API Key 已更新（{event.get_sender_id()}）")
            yield event.plain_result("Hypixel API Key 已保存!"); return

        if sub == "bjdkey":
            if not arg:
                yield event.plain_result("请输入 BuGLand Token"); return
            self.config["bjd_token"] = arg
            self.config.save_config()
            self.bjd = BuGLandClient(arg)
            logger.info(f"BuGLand Token 已更新（{event.get_sender_id()}）")
            yield event.plain_result("BuGLand Token 已保存!"); return

        HYPHANDLERS = {
            "player": player_cmd.handle,
            "bedwars": bedwars_cmd.handle,
            "skywars": skywars_cmd.handle,
            "arcade": arcade_cmd.handle,
            "zombies": zombies_cmd.handle,
            "party": party_cmd.handle,
        }
        if sub == "blitz":
            if not self.bjd:
                yield event.plain_result("BuGLand Token 未配置，请使用 /hypixel bjdkey <token> 设置")
                return
            if not arg:
                yield event.plain_result("请输入玩家ID: /hypixel blitz <ID>"); return
            self._log(event, sub, arg)
            try:
                text = await blitz_cmd.handle(self.bjd, arg)
                yield event.plain_result(text)
            except Exception as e:
                logger.info(f"布吉岛 {arg} 失败: {e}")
                yield event.plain_result(f"获取布吉岛数据失败: {e}")
            return

        h = HYPHANDLERS.get(sub)
        if not h:
            yield event.plain_result(f"未知命令: {sub}"); return
        if not self.client:
            yield event.plain_result("Hypixel API Key 未配置"); return
        if not arg:
            yield event.plain_result(f"请输入玩家ID: /hypixel {sub} <ID>"); return

        self._log(event, sub, arg)
        try:
            text = await h(self.client, arg)
            yield event.plain_result(text)
        except Exception as e:
            logger.info(f"查询 {sub} {arg} 失败: {e}")
            yield event.plain_result(f"获取数据失败: {e}")

    async def terminate(self):
        if hasattr(self, "client") and self.client:
            await self.client.close()
        if hasattr(self, "bjd") and self.bjd:
            await self.bjd.close()
