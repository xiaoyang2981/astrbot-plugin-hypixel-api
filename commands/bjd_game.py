from .shared import fmt_num

GAME_NAMES = {
    "bedwars": "🛏️ 起床战争",
    "skywars": "🌌 空岛战争",
    "blitz": "⚔️ 布吉岛 Blitz",
    "thebridges": "🌉 搭桥",
    "murder": "🔪 密室杀手",
    "arcade": "🕹️ 街机",
}

async def handle(bjd, game: str, name: str) -> str:
    data = await bjd.get_gamestats(name, game=game)
    display = GAME_NAMES.get(game, f"🎮 {game}")
    d = data.get("data", data)
    lines = [f"━━━━ {display} ━━━━", f"👤 玩家名 → {name}"]
    for k, v in d.items():
        if isinstance(v, (int, float)):
            lines.append(f"  {k} → {fmt_num(int(v))}")
        elif isinstance(v, str) and v:
            lines.append(f"  {k} → {v}")
    return "\n".join(lines)
