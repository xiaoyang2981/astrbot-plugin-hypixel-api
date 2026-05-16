from .shared import fmt_num, calc_kdr, calc_wlr

async def handle(client, name):
    sw = await client.get_skywars_stats(name=name)
    kdr = calc_kdr(sw["kills"], sw["deaths"])
    wlr = calc_wlr(sw["wins"], sw["losses"])
    return (
        f"━━━━ 🌌 空岛战争 ━━━━\n"
        f"👤 玩家名 → {sw['display_name']}\n"
        f"✨ 等级 → Lv.{sw['level']}\n"
        f"🏆 胜场 → {fmt_num(sw['wins'])}\n"
        f"💔 败场 → {fmt_num(sw['losses'])}\n"
        f"📈 W/L → {wlr}\n"
        f"⚔️ 击杀 → {fmt_num(sw['kills'])}\n"
        f"💀 死亡 → {fmt_num(sw['deaths'])}\n"
        f"📊 K/D → {kdr}\n"
        f"💜 Souls → {fmt_num(sw['souls'])}\n"
        f"👤 Heads → {fmt_num(sw['heads'])}\n"
        f"🎮 总场次 → {fmt_num(sw['games_played'])}\n"
        f"🪙 硬币 → {fmt_num(sw['coins'])}"
    )
