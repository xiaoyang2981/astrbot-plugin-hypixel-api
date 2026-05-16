from .shared import fmt_num

async def handle(client, name):
    p = await client.get_party_games_stats(name=name)
    msg = (
        f"━━━━ 🎉 小游戏派对 ━━━━\n"
        f"👤 玩家名 → {p['display_name']}\n"
        f"🏆 回合胜场 → {fmt_num(p['round_wins'])}\n"
        f"🔄 总回合 → {fmt_num(p['total_rounds'])}\n"
    )
    if p["mini_games"]:
        msg += "🎯 各小游戏胜场:\n"
        for g, w in p["mini_games"]:
            msg += f"  🎮 {g} → {w}\n"
    return msg
