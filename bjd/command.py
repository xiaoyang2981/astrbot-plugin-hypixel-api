def fmt_num(n: int) -> str:
    return f"{n:,}"

GAME_NAMES = {
    "bedwars": "🛏️ 起床战争", "skywars": "🌌 空岛战争",
    "blitz": "⚔️ 布吉岛 Blitz", "thebridges": "🌉 搭桥",
    "murder": "🔪 密室杀手", "arcade": "🕹️ 街机",
}

async def blitz(client, name):
    b = await client.get_blitz_stats(name=name)
    kd = f"{b['kills'] / b['deaths']:.2f}" if b['deaths'] else "∞"
    return (
        f"━━━━ ⚔️ 布吉岛 Blitz ━━━━\n"
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

async def gamestats(bjd, game: str, name: str) -> str:
    data = await bjd.get_gamestats(name, game=game)
    d = data.get("data", data)
    display = GAME_NAMES.get(game, f"🎮 {game}")
    lines = [f"━━━━ {display} ━━━━", f"👤 玩家名 → {name}"]
    for k, v in d.items():
        if isinstance(v, (int, float)):
            lines.append(f"  {k} → {fmt_num(int(v))}")
        elif isinstance(v, str) and v:
            lines.append(f"  {k} → {v}")
    return "\n".join(lines)
