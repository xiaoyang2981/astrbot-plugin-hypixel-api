from .shared import fmt_num, calc_fkdr, calc_kdr, calc_wlr

async def handle(client, name):
    bw = await client.get_bedwars_stats(name=name)
    fkdr = calc_fkdr(bw["final_kills"], bw["final_deaths"])
    kdr = calc_kdr(bw["kills"], bw["deaths"])
    wlr = calc_wlr(bw["wins"], bw["losses"])
    return (
        f"━━━━ 🛏️ 起床战争 ━━━━\n"
        f"👤 玩家名 → {bw['display_name']}\n"
        f"📊 等级 → {fmt_num(bw['level'])}\n"
        f"🏆 胜场 → {fmt_num(bw['wins'])}\n"
        f"💔 败场 → {fmt_num(bw['losses'])}\n"
        f"📈 W/L → {wlr}\n"
        f"⚔️ 击杀 → {fmt_num(bw['kills'])}\n"
        f"💀 死亡 → {fmt_num(bw['deaths'])}\n"
        f"📊 K/D → {kdr}\n"
        f"🔥 最终击杀 → {fmt_num(bw['final_kills'])}\n"
        f"💀 最终死亡 → {fmt_num(bw['final_deaths'])}\n"
        f"📈 FKDR → {fkdr}\n"
        f"🛏️ 拆床 → {fmt_num(bw['beds_broken'])}\n"
        f"💤 丢床 → {fmt_num(bw['beds_lost'])}\n"
        f"🔥 连胜 → {bw['winstreak']}\n"
        f"🎮 总场次 → {fmt_num(bw['games_played'])}\n"
        f"🪙 硬币 → {fmt_num(bw['coins'])}"
    )
