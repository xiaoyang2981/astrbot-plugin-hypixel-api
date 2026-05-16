from .shared import fmt_num

async def handle(client, name):
    b = await client.get_blitz_stats(name=name)
    kd = f"{b['kills'] / b['deaths']:.2f}" if b['deaths'] else "∞"
    return (
        f"━━━━ ⚔️ 布吉岛 ━━━━\n"
        f"👤 玩家名 → {b['display_name']}\n"
        f"🪙 硬币 → {fmt_num(b['coins'])}\n"
        f"🏆 总胜场 → {fmt_num(b['wins'])}\n"
        f"🎮 总场次 → {fmt_num(b['games_played'])}\n"
        f"⚔️ 击杀 → {fmt_num(b['kills'])}\n"
        f"💀 死亡 → {fmt_num(b['deaths'])}\n"
        f"📊 K/D → {kd}\n"
        f"👥 组队胜场 → {fmt_num(b['wins_teams'])}\n"
        f"👥 组队击杀 → {fmt_num(b['kills_teams'])}\n"
        f"👤 单人胜场 → {fmt_num(b['wins_solo'])}\n"
        f"👤 单人击杀 → {fmt_num(b['kills_solo'])}\n"
        f"📦 开箱 → {fmt_num(b['chests_opened'])}\n"
        f"⏱️ 游戏时长 → {fmt_num(b['time_played'])} 分钟"
    )
