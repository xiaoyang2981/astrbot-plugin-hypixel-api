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
