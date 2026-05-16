from .shared import fmt_num, calc_network_level, ts_to_str

async def handle(client, name):
    info = await client.get_player_rank_info(name=name)
    level = calc_network_level(info.get("network_level", 0))
    return (
        f"━━━━ 🔍 玩家信息 ━━━━\n"
        f"👤 玩家名 → {info['display_name']}\n"
        f"✨ 等级 → Lv.{level}\n"
        f"🆔 UUID → {info['uuid']}\n"
        f"⭐ Rank → {info.get('rank', 'NONE')}\n"
        f"💎 人品 → {fmt_num(info.get('karma', 0))}\n"
        f"🌐 语言 → {info.get('language', 'N/A')}\n"
        f"🕐 首次登录 → {ts_to_str(info.get('first_login', 0))}\n"
        f"🕐 最近活跃 → {ts_to_str(info.get('last_login', 0))}"
    )
