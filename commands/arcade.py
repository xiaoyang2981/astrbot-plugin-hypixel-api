from .shared import fmt_num

async def handle(client, name):
    arc = await client.get_arcade_stats(name=name)
    msg = (
        f"━━━━ 🕹️ 街机游戏 ━━━━\n"
        f"👤 玩家名 → {arc['display_name']}\n"
        f"🏆 总胜场 → {fmt_num(arc['wins'])}\n"
        f"🔄 总回合 → {fmt_num(arc['rounds_played'])}\n"
        f"🪙 硬币 → {fmt_num(arc['coins'])}\n"
    )
    if arc["top_games"]:
        msg += "🏆 热门小游戏:\n"
        for g, w in arc["top_games"][:5]:
            msg += f"  🎮 {g} → {w} 胜\n"
    return msg
