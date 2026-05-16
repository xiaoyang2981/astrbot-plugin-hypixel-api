PLAYER_TMPL = '''
<div style="
  width: 500px;
  padding: 24px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  border-radius: 16px;
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  color: #e0e0e0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.6);
  border: 1px solid #2a2a4a;
">
  <div style="
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 2px solid #FFAA00;
  ">
    <div style="
      width: 60px; height: 60px;
      border-radius: 50%;
      background: linear-gradient(135deg, #FFAA00, #FF6600);
      display: flex; align-items: center; justify-content: center;
      font-size: 28px; font-weight: bold; color: #fff;
      flex-shrink: 0;
    ">{{ initials }}</div>
    <div style="flex: 1;">
      <div style="font-size: 24px; font-weight: bold; color: #FFAA00;">{{ display_name }}</div>
      <div style="font-size: 14px; color: #aaa; margin-top: 2px;">{{ rank_display }}</div>
    </div>
    <div style="
      background: #FFAA00; color: #1a1a2e;
      padding: 4px 14px; border-radius: 20px;
      font-size: 13px; font-weight: bold;
    ">Lv.{{ level }}</div>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px;">UUID</div>
      <div style="font-size: 13px; color: #ccc; margin-top: 4px;">{{ uuid }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px;">语言</div>
      <div style="font-size: 14px; color: #ccc; margin-top: 4px;">{{ language }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px;">Karma</div>
      <div style="font-size: 16px; color: #55FF55; margin-top: 4px;">{{ karma }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 1px;">Rank</div>
      <div style="font-size: 16px; color: #55FFFF; margin-top: 4px;">{{ rank }}</div>
    </div>
  </div>

  <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid #2a2a4a;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
      <span style="font-size: 12px; color: #888;">首次登录</span>
      <span style="font-size: 13px; color: #ccc;">{{ first_login }}</span>
    </div>
    <div style="display: flex; justify-content: space-between;">
      <span style="font-size: 12px; color: #888;">最近活跃</span>
      <span style="font-size: 13px; color: #ccc;">{{ last_login }}</span>
    </div>
  </div>
</div>
'''

BEDWARS_TMPL = '''
<div style="
  width: 500px;
  padding: 24px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  border-radius: 16px;
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  color: #e0e0e0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.6);
  border: 1px solid #2a2a4a;
">
  <div style="
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid #FF5555;
  ">
    <div style="font-size: 28px;">🛏️</div>
    <div style="flex: 1;">
      <div style="font-size: 22px; font-weight: bold; color: #FF5555;">Bed Wars</div>
      <div style="font-size: 14px; color: #aaa; margin-top: 2px;">{{ display_name }}</div>
    </div>
    <div style="
      background: #FF5555; color: #fff;
      padding: 4px 14px; border-radius: 20px;
      font-size: 13px; font-weight: bold;
    ">{{ level }}</div>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">胜场</div>
      <div style="font-size: 20px; color: #55FF55; font-weight: bold; margin-top: 4px;">{{ wins }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">败场</div>
      <div style="font-size: 20px; color: #FF5555; font-weight: bold; margin-top: 4px;">{{ losses }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">最终击杀</div>
      <div style="font-size: 18px; color: #FFAA00; font-weight: bold; margin-top: 4px;">{{ final_kills }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">最终死亡</div>
      <div style="font-size: 18px; color: #FF5555; font-weight: bold; margin-top: 4px;">{{ final_deaths }}</div>
    </div>
  </div>

  <div style="
    background: rgba(255,255,255,0.05);
    border-radius: 10px; padding: 14px;
    margin-top: 12px;
    display: flex; justify-content: space-around;
  ">
    <div style="text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">FKDR</div>
      <div style="font-size: 20px; color: #55FFFF; font-weight: bold;">{{ fkdr }}</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">K/D</div>
      <div style="font-size: 20px; color: #55FFFF; font-weight: bold;">{{ kdr }}</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">W/L</div>
      <div style="font-size: 20px; color: #55FFFF; font-weight: bold;">{{ wlr }}</div>
    </div>
  </div>

  <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid #2a2a4a;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
      <span style="font-size: 12px; color: #888;">拆床</span>
      <span style="font-size: 14px; color: #FFAA00;">{{ beds_broken }}</span>
    </div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
      <span style="font-size: 12px; color: #888;">丢床</span>
      <span style="font-size: 14px; color: #FF5555;">{{ beds_lost }}</span>
    </div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
      <span style="font-size: 12px; color: #888;">连胜</span>
      <span style="font-size: 14px; color: #55FF55;">{{ winstreak }}</span>
    </div>
    <div style="display: flex; justify-content: space-between;">
      <span style="font-size: 12px; color: #888;">总场次</span>
      <span style="font-size: 14px; color: #ccc;">{{ games_played }}</span>
    </div>
  </div>
</div>
'''

SKYWARS_TMPL = '''
<div style="
  width: 500px;
  padding: 24px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  border-radius: 16px;
  font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
  color: #e0e0e0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.6);
  border: 1px solid #2a2a4a;
">
  <div style="
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 2px solid #55FFFF;
  ">
    <div style="font-size: 28px;">🌌</div>
    <div style="flex: 1;">
      <div style="font-size: 22px; font-weight: bold; color: #55FFFF;">Sky Wars</div>
      <div style="font-size: 14px; color: #aaa; margin-top: 2px;">{{ display_name }}</div>
    </div>
    <div style="
      background: #55FFFF; color: #1a1a2e;
      padding: 4px 14px; border-radius: 20px;
      font-size: 13px; font-weight: bold;
    ">Lv.{{ level }}</div>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">胜场</div>
      <div style="font-size: 20px; color: #55FF55; font-weight: bold; margin-top: 4px;">{{ wins }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">败场</div>
      <div style="font-size: 20px; color: #FF5555; font-weight: bold; margin-top: 4px;">{{ losses }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">击杀</div>
      <div style="font-size: 18px; color: #FFAA00; font-weight: bold; margin-top: 4px;">{{ kills }}</div>
    </div>
    <div style="background: rgba(255,255,255,0.05); border-radius: 10px; padding: 12px; text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">死亡</div>
      <div style="font-size: 18px; color: #FF5555; font-weight: bold; margin-top: 4px;">{{ deaths }}</div>
    </div>
  </div>

  <div style="
    background: rgba(255,255,255,0.05);
    border-radius: 10px; padding: 14px;
    margin-top: 12px;
    display: flex; justify-content: space-around;
  ">
    <div style="text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">K/D</div>
      <div style="font-size: 20px; color: #55FFFF; font-weight: bold;">{{ kdr }}</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">W/L</div>
      <div style="font-size: 20px; color: #55FFFF; font-weight: bold;">{{ wlr }}</div>
    </div>
    <div style="text-align: center;">
      <div style="font-size: 11px; color: #888; text-transform: uppercase;">Souls</div>
      <div style="font-size: 20px; color: #55FFFF; font-weight: bold;">{{ souls }}</div>
    </div>
  </div>

  <div style="margin-top: 14px; padding-top: 12px; border-top: 1px solid #2a2a4a;">
    <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
      <span style="font-size: 12px; color: #888;">总场次</span>
      <span style="font-size: 14px; color: #ccc;">{{ games_played }}</span>
    </div>
    <div style="display: flex; justify-content: space-between;">
      <span style="font-size: 12px; color: #888;">Heads</span>
      <span style="font-size: 14px; color: #FFAA00;">{{ heads }}</span>
    </div>
  </div>
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
