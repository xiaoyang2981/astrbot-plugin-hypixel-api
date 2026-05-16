PLAYER_HTML = r'''
<div style="
  width:480px; margin:0 auto; padding:20px 24px;
  background:linear-gradient(135deg,#0d1117 0%,#161b22 50%,#0d1117 100%);
  border-radius:14px; border:1px solid #30363d;
  font-family:-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif; color:#c9d1d9;
  box-shadow:0 4px 24px rgba(0,0,0,.6);
">
  <div style="display:flex;align-items:center;gap:14px;padding-bottom:14px;border-bottom:2px solid #f0883e;">
    <div style="
      width:52px;height:52px;border-radius:50%;flex-shrink:0;
      background:linear-gradient(135deg,#f0883e,#da3633);
      display:flex;align-items:center;justify-content:center;
      font-size:22px;font-weight:700;color:#fff;
    ">{{ initials }}</div>
    <div style="flex:1;min-width:0;">
      <div style="font-size:20px;font-weight:700;color:#f0883e;">{{ display_name }}</div>
      <div style="font-size:13px;color:#8b949e;margin-top:2px;">{{ rank_display }}</div>
    </div>
    <div style="background:#f0883e;color:#0d1117;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;white-space:nowrap;">Lv.{{ level }}</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;">
    <div style="background:#161b22;border-radius:8px;padding:10px;">
      <div style="font-size:10px;color:#8b949e;letter-spacing:.5px;">UUID</div>
      <div style="font-size:12px;color:#c9d1d9;margin-top:3px;word-break:break-all;">{{ uuid }}</div>
    </div>
    <div style="background:#161b22;border-radius:8px;padding:10px;">
      <div style="font-size:10px;color:#8b949e;letter-spacing:.5px;">语言</div>
      <div style="font-size:13px;color:#c9d1d9;margin-top:3px;">{{ language }}</div>
    </div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;">
      <div style="font-size:10px;color:#8b949e;letter-spacing:.5px;">Karma</div>
      <div style="font-size:16px;color:#3fb950;font-weight:700;margin-top:3px;">{{ karma }}</div>
    </div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;">
      <div style="font-size:10px;color:#8b949e;letter-spacing:.5px;">Rank</div>
      <div style="font-size:16px;color:#58a6ff;font-weight:700;margin-top:3px;">{{ rank }}</div>
    </div>
  </div>
  <div style="margin-top:14px;padding-top:12px;border-top:1px solid #21262d;">
    <div style="display:flex;justify-content:space-between;margin-bottom:5px;"><span style="font-size:11px;color:#8b949e;">首次登录</span><span style="font-size:12px;color:#c9d1d9;">{{ first_login }}</span></div>
    <div style="display:flex;justify-content:space-between;"><span style="font-size:11px;color:#8b949e;">最近活跃</span><span style="font-size:12px;color:#c9d1d9;">{{ last_login }}</span></div>
  </div>
</div>
'''

BEDWARS_HTML = r'''
<div style="
  width:480px; margin:0 auto; padding:20px 24px;
  background:linear-gradient(135deg,#0d1117 0%,#1c1212 50%,#0d1117 100%);
  border-radius:14px; border:1px solid #30363d;
  font-family:-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif; color:#c9d1d9;
  box-shadow:0 4px 24px rgba(0,0,0,.6);
">
  <div style="display:flex;align-items:center;gap:12px;padding-bottom:14px;border-bottom:2px solid #da3633;">
    <div style="font-size:24px;line-height:1;">🛏️</div>
    <div style="flex:1;"><div style="font-size:19px;font-weight:700;color:#f85149;">起床战争</div><div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>
    <div style="background:#da3633;color:#fff;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;">Lv.{{ level }}</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;">
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">胜场</div><div style="font-size:18px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">败场</div><div style="font-size:18px;color:#f85149;font-weight:700;margin-top:3px;">{{ losses }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">最终击杀</div><div style="font-size:16px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ final_kills }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">最终死亡</div><div style="font-size:16px;color:#f85149;font-weight:700;margin-top:3px;">{{ final_deaths }}</div></div>
  </div>
  <div style="background:#161b22;border-radius:8px;padding:12px;margin-top:10px;display:flex;justify-content:space-around;">
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">FKDR</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ fkdr }}</div></div>
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">K/D</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ kdr }}</div></div>
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">W/L</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ wlr }}</div></div>
  </div>
  <div style="margin-top:12px;padding-top:10px;border-top:1px solid #21262d;">
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:11px;color:#8b949e;">拆床</span><span style="font-size:13px;color:#d2a8ff;">{{ beds_broken }}</span></div>
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:11px;color:#8b949e;">丢床</span><span style="font-size:13px;color:#f85149;">{{ beds_lost }}</span></div>
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:11px;color:#8b949e;">连胜</span><span style="font-size:13px;color:#3fb950;">{{ winstreak }}</span></div>
    <div style="display:flex;justify-content:space-between;"><span style="font-size:11px;color:#8b949e;">总场次</span><span style="font-size:13px;color:#c9d1d9;">{{ games_played }}</span></div>
  </div>
</div>
'''

SKYWARS_HTML = r'''
<div style="
  width:480px; margin:0 auto; padding:20px 24px;
  background:linear-gradient(135deg,#0d1117 0%,#0d1b2a 50%,#0d1117 100%);
  border-radius:14px; border:1px solid #30363d;
  font-family:-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif; color:#c9d1d9;
  box-shadow:0 4px 24px rgba(0,0,0,.6);
">
  <div style="display:flex;align-items:center;gap:12px;padding-bottom:14px;border-bottom:2px solid #58a6ff;">
    <div style="font-size:24px;line-height:1;">🌌</div>
    <div style="flex:1;"><div style="font-size:19px;font-weight:700;color:#58a6ff;">空岛战争</div><div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>
    <div style="background:#58a6ff;color:#0d1117;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;">Lv.{{ level }}</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;">
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">胜场</div><div style="font-size:18px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">败场</div><div style="font-size:18px;color:#f85149;font-weight:700;margin-top:3px;">{{ losses }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">击杀</div><div style="font-size:16px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ kills }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:12px;text-align:center;"><div style="font-size:10px;color:#8b949e;">死亡</div><div style="font-size:16px;color:#f85149;font-weight:700;margin-top:3px;">{{ deaths }}</div></div>
  </div>
  <div style="background:#161b22;border-radius:8px;padding:12px;margin-top:10px;display:flex;justify-content:space-around;">
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">K/D</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ kdr }}</div></div>
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">W/L</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ wlr }}</div></div>
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">Souls</div><div style="font-size:17px;color:#58a6ff;font-weight:700;">{{ souls }}</div></div>
  </div>
  <div style="margin-top:12px;padding-top:10px;border-top:1px solid #21262d;">
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:11px;color:#8b949e;">总场次</span><span style="font-size:13px;color:#c9d1d9;">{{ games_played }}</span></div>
    <div style="display:flex;justify-content:space-between;"><span style="font-size:11px;color:#8b949e;">Heads</span><span style="font-size:13px;color:#d2a8ff;">{{ heads }}</span></div>
  </div>
</div>
'''

ARCADE_HTML = r'''
<div style="
  width:480px; margin:0 auto; padding:20px 24px;
  background:linear-gradient(135deg,#0d1117 0%,#1b1b0d 50%,#0d1117 100%);
  border-radius:14px; border:1px solid #30363d;
  font-family:-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif; color:#c9d1d9;
  box-shadow:0 4px 24px rgba(0,0,0,.6);
">
  <div style="display:flex;align-items:center;gap:12px;padding-bottom:14px;border-bottom:2px solid #d2a8ff;">
    <div style="font-size:24px;line-height:1;">🕹️</div>
    <div><div style="font-size:19px;font-weight:700;color:#d2a8ff;">街机游戏</div><div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:14px 0;">
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">总胜场</div><div style="font-size:18px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">总回合</div><div style="font-size:18px;color:#58a6ff;font-weight:700;margin-top:3px;">{{ rounds_played }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">硬币</div><div style="font-size:18px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ coins }}</div></div>
  </div>
  {% if top_games %}
  <div style="padding-top:10px;border-top:1px solid #21262d;">
    <div style="font-size:12px;color:#8b949e;margin-bottom:8px;">🏆 热门小游戏排行</div>
    {% for gname, gwins in top_games %}
    <div style="display:flex;justify-content:space-between;padding:4px 0;"><span style="font-size:12px;color:#c9d1d9;">{{ gname }}</span><span style="font-size:12px;color:#d2a8ff;">{{ gwins }} 胜</span></div>
    {% endfor %}
  </div>
  {% endif %}
</div>
'''

ZOMBIES_HTML = r'''
<div style="
  width:480px; margin:0 auto; padding:20px 24px;
  background:linear-gradient(135deg,#0d1117 0%,#1a120e 50%,#0d1117 100%);
  border-radius:14px; border:1px solid #30363d;
  font-family:-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif; color:#c9d1d9;
  box-shadow:0 4px 24px rgba(0,0,0,.6);
">
  <div style="display:flex;align-items:center;gap:12px;padding-bottom:14px;border-bottom:2px solid #7ee787;">
    <div style="font-size:24px;line-height:1;">🧟</div>
    <div style="flex:1;"><div style="font-size:19px;font-weight:700;color:#7ee787;">丧尸末日</div><div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>
    <div style="background:#7ee787;color:#0d1117;padding:3px 12px;border-radius:20px;font-size:12px;font-weight:700;">{{ games_played }} 场</div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:14px;">
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">胜场</div><div style="font-size:17px;color:#3fb950;font-weight:700;margin-top:3px;">{{ wins }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">败场</div><div style="font-size:17px;color:#f85149;font-weight:700;margin-top:3px;">{{ losses }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">击杀</div><div style="font-size:15px;color:#d2a8ff;font-weight:700;margin-top:3px;">{{ kills }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">死亡</div><div style="font-size:15px;color:#f85149;font-weight:700;margin-top:3px;">{{ deaths }}</div></div>
  </div>
  <div style="background:#161b22;border-radius:8px;padding:10px;margin-top:10px;display:flex;justify-content:space-around;">
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">爆头</div><div style="font-size:16px;color:#d2a8ff;font-weight:700;">{{ headshots }}</div></div>
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">开门</div><div style="font-size:16px;color:#58a6ff;font-weight:700;">{{ doors_opened }}</div></div>
    <div style="text-align:center;"><div style="font-size:10px;color:#8b949e;">开箱</div><div style="font-size:16px;color:#58a6ff;font-weight:700;">{{ chests_looted }}</div></div>
  </div>
  <div style="margin-top:10px;padding-top:10px;border-top:1px solid #21262d;">
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:11px;color:#8b949e;">总生存回合</span><span style="font-size:13px;color:#3fb950;">{{ rounds_survived }}</span></div>
    <div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:11px;color:#8b949e;">最佳回合</span><span style="font-size:13px;color:#d2a8ff;">{{ best_round }}</span></div>
    {% for mname, mround in maps %}
    <div style="display:flex;justify-content:space-between;margin-bottom:2px;"><span style="font-size:11px;color:#8b949e;">{{ mname }}</span><span style="font-size:12px;color:#c9d1d9;">最佳 {{ mround }} 回合</span></div>
    {% endfor %}
  </div>
</div>
'''

PARTY_HTML = r'''
<div style="
  width:480px; margin:0 auto; padding:20px 24px;
  background:linear-gradient(135deg,#0d1117 0%,#1b0d1b 50%,#0d1117 100%);
  border-radius:14px; border:1px solid #30363d;
  font-family:-apple-system,'Segoe UI','Helvetica Neue',Arial,sans-serif; color:#c9d1d9;
  box-shadow:0 4px 24px rgba(0,0,0,.6);
">
  <div style="display:flex;align-items:center;gap:12px;padding-bottom:14px;border-bottom:2px solid #bc8cff;">
    <div style="font-size:24px;line-height:1;">🎉</div>
    <div><div style="font-size:19px;font-weight:700;color:#bc8cff;">小游戏派对</div><div style="font-size:13px;color:#8b949e;margin-top:1px;">{{ display_name }}</div></div>
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:14px 0;">
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">回合胜场</div><div style="font-size:18px;color:#3fb950;font-weight:700;margin-top:3px;">{{ round_wins }}</div></div>
    <div style="background:#161b22;border-radius:8px;padding:10px;text-align:center;"><div style="font-size:10px;color:#8b949e;">总回合</div><div style="font-size:18px;color:#58a6ff;font-weight:700;margin-top:3px;">{{ total_rounds }}</div></div>
  </div>
  {% if mini_games %}
  <div style="padding-top:10px;border-top:1px solid #21262d;">
    <div style="font-size:12px;color:#8b949e;margin-bottom:8px;">🎯 各小游戏胜场</div>
    {% for gname, gwins in mini_games %}
    <div style="display:flex;justify-content:space-between;padding:4px 0;"><span style="font-size:12px;color:#c9d1d9;">{{ gname }}</span><span style="font-size:12px;color:#bc8cff;">{{ gwins }}</span></div>
    {% endfor %}
  </div>
  {% endif %}
</div>
'''


def get_initials(name: str) -> str:
    name = name.strip()
    if not name:
        return "?"
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[1][0]).upper()
    return name[:2].upper()


TEMPLATES = {
    "player": PLAYER_HTML,
    "bedwars": BEDWARS_HTML,
    "skywars": SKYWARS_HTML,
    "arcade": ARCADE_HTML,
    "zombies": ZOMBIES_HTML,
    "party": PARTY_HTML,
}
