from datetime import datetime, timezone

def fmt_num(n: int) -> str:
    return f"{n:,}"

def calc_network_level(exp: int) -> int:
    if exp <= 0: return 1
    level, need = 1, 2500
    while exp >= need:
        exp -= need; level += 1; need += 2500
    return level

def calc_fkdr(fk, fd):
    return f"{fk / fd:.2f}" if fd else f"{fk:.2f}"

def calc_kdr(k, d):
    return f"{k / d:.2f}" if d else f"{k:.2f}"

def calc_wlr(w, l):
    return f"{w / l:.2f}" if l else f"{w:.2f}"

def ts_to_str(ts: int) -> str:
    if ts == 0: return "N/A"
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


async def player(client, name):
    info = await client.get_player_rank_info(name=name)
    lv = calc_network_level(info.get("network_level", 0))
    return (
        f"━━━━ 🔍 玩家信息 ━━━━\n"
        f"👤 玩家名 → {info['display_name']}\n"
        f"✨ 等级 → Lv.{lv}\n"
        f"🆔 UUID → {info['uuid']}\n"
        f"⭐ Rank → {info.get('rank', 'NONE')}\n"
        f"💎 人品 → {fmt_num(info.get('karma', 0))}\n"
        f"🌐 语言 → {info.get('language', 'N/A')}\n"
        f"🕐 首次登录 → {ts_to_str(info.get('first_login', 0))}\n"
        f"🕐 最近活跃 → {ts_to_str(info.get('last_login', 0))}"
    )

async def bedwars(client, name):
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

async def skywars(client, name):
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

async def arcade(client, name):
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

async def zombies(client, name):
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

async def party(client, name):
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
