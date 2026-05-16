_GRID = "background:#161b22;border-radius:10px;padding:12px 14px;"
_LABEL = "font-size:11px;color:#8b949e;letter-spacing:.3px;"
_VAL = "font-size:15px;color:#e6edf3;font-weight:600;margin-top:2px;"
_HL = "background:#1c2128;border-radius:10px;padding:14px;display:flex;justify-content:space-around;"
_BD = "#30363d"

PLAYER_TPL = (
    '<div style="background:linear-gradient(135deg,#0d1117 0%,#161b22 50%,#0d1117 100%);'
    'border-radius:16px;border:1px solid '+_BD+';padding:24px 28px;'
    'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;'
    'color:#e6edf3;width:520px;">'
    '<div style="display:flex;align-items:center;gap:16px;padding-bottom:16px;border-bottom:2px solid #f0883e;">'
    '<div style="width:56px;height:56px;border-radius:50%;flex-shrink:0;'
    'background:linear-gradient(135deg,#f0883e,#da3633);display:flex;align-items:center;justify-content:center;'
    'font-size:24px;font-weight:700;color:#fff;">{{ initials }}</div>'
    '<div style="flex:1;min-width:0;"><div style="font-size:22px;font-weight:700;color:#f0883e;">{{ display_name }}</div>'
    '<div style="font-size:13px;color:#8b949e;margin-top:2px;">{{ rank_display }}</div></div>'
    '<div style="background:#f0883e;color:#0d1117;padding:4px 14px;border-radius:20px;'
    'font-size:13px;font-weight:700;white-space:nowrap;">Lv.{{ level }}</div></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">'
    '<div style="'+_GRID+'"><div style="'+_LABEL+'">UUID</div><div style="'+_VAL+'word-break:break-all;">{{ uuid }}</div></div>'
    '<div style="'+_GRID+'"><div style="'+_LABEL+'">语言</div><div style="'+_VAL+'">{{ language }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">Karma</div>'
    '<div style="font-size:18px;color:#3fb950;font-weight:700;margin-top:3px;">{{ karma }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">Rank</div>'
    '<div style="font-size:18px;color:#58a6ff;font-weight:700;margin-top:3px;">{{ rank }}</div></div></div>'
    '<div style="margin-top:16px;padding-top:14px;border-top:1px solid #21262d;">'
    '<div style="display:flex;justify-content:space-between;margin-bottom:6px;">'
    '<span style="font-size:12px;color:#8b949e;">首次登录</span><span style="font-size:13px;color:#e6edf3;">{{ first_login }}</span></div>'
    '<div style="display:flex;justify-content:space-between;">'
    '<span style="font-size:12px;color:#8b949e;">最近活跃</span><span style="font-size:13px;color:#e6edf3;">{{ last_login }}</span></div></div></div>'
)

_BW_BG = "background:linear-gradient(135deg,#0d1117 0%,#1c1212 50%,#0d1117 100%);"
BEDWARS_TPL = (
    '<div style="'+_BW_BG
    +'border-radius:16px;border:1px solid '+_BD+';padding:24px 28px;'
    'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;color:#e6edf3;width:520px;">'
    '<div style="display:flex;align-items:center;gap:12px;padding-bottom:16px;border-bottom:2px solid #da3633;">'
    '<div style="font-size:26px;line-height:1;">🛏️</div>'
    '<div style="flex:1;"><div style="font-size:20px;font-weight:700;color:#f85149;">起床战争</div>'
    '<div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>'
    '<div style="background:#da3633;color:#fff;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:700;">Lv.{{ level }}</div></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">胜场</div>'
    '<div style="font-size:20px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">败场</div>'
    '<div style="font-size:20px;color:#f85149;font-weight:700;margin-top:3px;">{{ losses }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">最终击杀</div>'
    '<div style="font-size:17px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ final_kills }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">最终死亡</div>'
    '<div style="font-size:17px;color:#f85149;font-weight:700;margin-top:3px;">{{ final_deaths }}</div></div></div>'
    '<div style="'+_HL+'margin-top:12px;">'
    '<div style="text-align:center;"><div style="'+_LABEL+'">FKDR</div><div style="font-size:18px;color:#58a6ff;font-weight:700;">{{ fkdr }}</div></div>'
    '<div style="text-align:center;"><div style="'+_LABEL+'">K/D</div><div style="font-size:18px;color:#58a6ff;font-weight:700;">{{ kdr }}</div></div>'
    '<div style="text-align:center;"><div style="'+_LABEL+'">W/L</div><div style="font-size:18px;color:#58a6ff;font-weight:700;">{{ wlr }}</div></div></div>'
    '<div style="margin-top:14px;padding-top:12px;border-top:1px solid '+_BD+';">'
    '<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
    '<span style="font-size:12px;color:#8b949e;">拆床</span><span style="font-size:14px;color:#d2a8ff;">{{ beds_broken }}</span></div>'
    '<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
    '<span style="font-size:12px;color:#8b949e;">丢床</span><span style="font-size:14px;color:#f85149;">{{ beds_lost }}</span></div>'
    '<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
    '<span style="font-size:12px;color:#8b949e;">连胜</span><span style="font-size:14px;color:#3fb950;">{{ winstreak }}</span></div>'
    '<div style="display:flex;justify-content:space-between;">'
    '<span style="font-size:12px;color:#8b949e;">总场次</span><span style="font-size:14px;color:#e6edf3;">{{ games_played }}</span></div></div></div>'
)

_SW_BG = "background:linear-gradient(135deg,#0d1117 0%,#0d1b2a 50%,#0d1117 100%);"
SKYWARS_TPL = (
    '<div style="'+_SW_BG
    +'border-radius:16px;border:1px solid '+_BD+';padding:24px 28px;'
    'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;color:#e6edf3;width:520px;">'
    '<div style="display:flex;align-items:center;gap:12px;padding-bottom:16px;border-bottom:2px solid #58a6ff;">'
    '<div style="font-size:26px;line-height:1;">🌌</div>'
    '<div style="flex:1;"><div style="font-size:20px;font-weight:700;color:#58a6ff;">空岛战争</div>'
    '<div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>'
    '<div style="background:#58a6ff;color:#0d1117;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:700;">Lv.{{ level }}</div></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">胜场</div>'
    '<div style="font-size:20px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">败场</div>'
    '<div style="font-size:20px;color:#f85149;font-weight:700;margin-top:3px;">{{ losses }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">击杀</div>'
    '<div style="font-size:17px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ kills }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">死亡</div>'
    '<div style="font-size:17px;color:#f85149;font-weight:700;margin-top:3px;">{{ deaths }}</div></div></div>'
    '<div style="'+_HL+'margin-top:12px;">'
    '<div style="text-align:center;"><div style="'+_LABEL+'">K/D</div><div style="font-size:18px;color:#58a6ff;font-weight:700;">{{ kdr }}</div></div>'
    '<div style="text-align:center;"><div style="'+_LABEL+'">W/L</div><div style="font-size:18px;color:#58a6ff;font-weight:700;">{{ wlr }}</div></div>'
    '<div style="text-align:center;"><div style="'+_LABEL+'">Souls</div><div style="font-size:18px;color:#58a6ff;font-weight:700;">{{ souls }}</div></div></div>'
    '<div style="margin-top:14px;padding-top:12px;border-top:1px solid '+_BD+';">'
    '<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
    '<span style="font-size:12px;color:#8b949e;">总场次</span><span style="font-size:14px;color:#e6edf3;">{{ games_played }}</span></div>'
    '<div style="display:flex;justify-content:space-between;">'
    '<span style="font-size:12px;color:#8b949e;">Heads</span><span style="font-size:14px;color:#d2a8ff;">{{ heads }}</span></div></div></div>'
)

_AR_BG = "background:linear-gradient(135deg,#0d1117 0%,#1b1b0d 50%,#0d1117 100%);"
ARCADE_TPL = (
    '<div style="'+_AR_BG
    +'border-radius:16px;border:1px solid '+_BD+';padding:24px 28px;'
    'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;color:#e6edf3;width:520px;">'
    '<div style="display:flex;align-items:center;gap:12px;padding-bottom:16px;border-bottom:2px solid #d2a8ff;">'
    '<div style="font-size:26px;line-height:1;">🕹️</div>'
    '<div><div style="font-size:20px;font-weight:700;color:#d2a8ff;">街机游戏</div>'
    '<div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:16px 0 0;">'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">总胜场</div>'
    '<div style="font-size:20px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">总回合</div>'
    '<div style="font-size:20px;color:#58a6ff;font-weight:700;margin-top:3px;">{{ rounds_played }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">硬币</div>'
    '<div style="font-size:20px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ coins }}</div></div></div>'
    '{% if top_games %}'
    '<div style="margin-top:16px;padding-top:14px;border-top:1px solid '+_BD+';">'
    '<div style="font-size:13px;color:#8b949e;margin-bottom:10px;">🏆 热门小游戏排行</div>'
    '{% for gname, gwins in top_games %}'
    '<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #21262d;">'
    '<span style="font-size:13px;color:#e6edf3;">{{ gname }}</span>'
    '<span style="font-size:13px;color:#d2a8ff;font-weight:600;">{{ gwins }} 胜</span></div>'
    '{% endfor %}</div>{% endif %}</div>'
)

_ZO_BG = "background:linear-gradient(135deg,#0d1117 0%,#1a120e 50%,#0d1117 100%);"
ZOMBIES_TPL = (
    '<div style="'+_ZO_BG
    +'border-radius:16px;border:1px solid '+_BD+';padding:24px 28px;'
    'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;color:#e6edf3;width:520px;">'
    '<div style="display:flex;align-items:center;gap:12px;padding-bottom:16px;border-bottom:2px solid #7ee787;">'
    '<div style="font-size:26px;line-height:1;">🧟</div>'
    '<div style="flex:1;"><div style="font-size:20px;font-weight:700;color:#7ee787;">丧尸末日</div>'
    '<div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>'
    '<div style="background:#7ee787;color:#0d1117;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:700;">{{ games_played }} 场</div></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:16px;">'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">胜场</div>'
    '<div style="font-size:18px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">败场</div>'
    '<div style="font-size:18px;color:#f85149;font-weight:700;margin-top:3px;">{{ losses }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">击杀</div>'
    '<div style="font-size:16px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ kills }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">死亡</div>'
    '<div style="font-size:16px;color:#f85149;font-weight:700;margin-top:3px;">{{ deaths }}</div></div></div>'
    '<div style="'+_HL+'margin-top:12px;">'
    '<div style="text-align:center;"><div style="'+_LABEL+'">爆头</div><div style="font-size:17px;color:#d2a8ff;font-weight:700;">{{ headshots }}</div></div>'
    '<div style="text-align:center;"><div style="'+_LABEL+'">开门</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ doors_opened }}</div></div>'
    '<div style="text-align:center;"><div style="'+_LABEL+'">开箱</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ chests_looted }}</div></div></div>'
    '<div style="margin-top:14px;padding-top:12px;border-top:1px solid '+_BD+';">'
    '<div style="display:flex;justify-content:space-between;margin-bottom:5px;">'
    '<span style="font-size:12px;color:#8b949e;">总生存回合</span><span style="font-size:14px;color:#3fb950;">{{ rounds_survived }}</span></div>'
    '<div style="display:flex;justify-content:space-between;margin-bottom:8px;">'
    '<span style="font-size:12px;color:#8b949e;">最佳回合</span><span style="font-size:14px;color:#d2a8ff;">{{ best_round }}</span></div>'
    '{% for mname, mround in maps %}'
    '<div style="display:flex;justify-content:space-between;padding:3px 6px 3px 0;border-bottom:1px solid #21262d;">'
    '<span style="font-size:12px;color:#8b949e;">🗺️ {{ mname }}</span>'
    '<span style="font-size:12px;color:#e6edf3;">最佳 {{ mround }} 回合</span></div>'
    '{% endfor %}</div></div>'
)

_PA_BG = "background:linear-gradient(135deg,#0d1117 0%,#1b0d1b 50%,#0d1117 100%);"
PARTY_TPL = (
    '<div style="'+_PA_BG
    +'border-radius:16px;border:1px solid '+_BD+';padding:24px 28px;'
    'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',sans-serif;color:#e6edf3;width:520px;">'
    '<div style="display:flex;align-items:center;gap:12px;padding-bottom:16px;border-bottom:2px solid #bc8cff;">'
    '<div style="font-size:26px;line-height:1;">🎉</div>'
    '<div><div style="font-size:20px;font-weight:700;color:#bc8cff;">小游戏派对</div>'
    '<div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div></div>'
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 0;">'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">回合胜场</div>'
    '<div style="font-size:20px;color:#3fb950;font-weight:700;margin-top:3px;">{{ round_wins }}</div></div>'
    '<div style="'+_GRID+'text-align:center;"><div style="'+_LABEL+'">总回合</div>'
    '<div style="font-size:20px;color:#58a6ff;font-weight:700;margin-top:3px;">{{ total_rounds }}</div></div></div>'
    '{% if mini_games %}'
    '<div style="margin-top:16px;padding-top:14px;border-top:1px solid '+_BD+';">'
    '<div style="font-size:13px;color:#8b949e;margin-bottom:10px;">🎯 各小游戏胜场</div>'
    '{% for gname, gwins in mini_games %}'
    '<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #21262d;">'
    '<span style="font-size:13px;color:#e6edf3;">{{ gname }}</span>'
    '<span style="font-size:13px;color:#bc8cff;font-weight:600;">{{ gwins }}</span></div>'
    '{% endfor %}</div>{% endif %}</div>'
)

TEMPLATES = {
    "player": PLAYER_TPL,
    "bedwars": BEDWARS_TPL,
    "skywars": SKYWARS_TPL,
    "arcade": ARCADE_TPL,
    "zombies": ZOMBIES_TPL,
    "party": PARTY_TPL,
}
