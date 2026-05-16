from .shared import fmt_num, calc_kdr, calc_wlr

async def handle(client, name):
    z = await client.get_zombies_stats(name=name)
    kdr = calc_kdr(z["kills"], z["deaths"])
    wlr = calc_wlr(z["wins"], z["losses"])
    msg = (
        f"━━━━ 🧟 丧尸末日 ━━━━\n"
        f"👤 玩家名 → {z['display_name']}\n"
        f"🎮 场次 → {fmt_num(z['games_played'])}\n"
        f"🏆 胜场 → {fmt_num(z['wins'])}\n"
        f"💔 败场 → {fmt_num(z['losses'])}\n"
        f"📈 W/L → {wlr}\n"
        f"⚔️ 击杀 → {fmt_num(z['kills'])}\n"
        f"💀 死亡 → {fmt_num(z['deaths'])}\n"
        f"📊 K/D → {kdr}\n"
        f"🎯 爆头 → {fmt_num(z['headshots'])}\n"
        f"🚪 开门 → {fmt_num(z['doors_opened'])}\n"
        f"📦 开箱 → {fmt_num(z['chests_looted'])}\n"
        f"🔄 生存回合 → {fmt_num(z['rounds_survived'])}\n"
        f"🏅 最佳回合 → {z['best_round']}\n"
    )
    if z["maps"]:
        msg += "🗺️ 地图记录:\n"
        for m, r in z["maps"].items():
            msg += f"  📍 {m} → 最佳 {r} 回合\n"
    return msg
