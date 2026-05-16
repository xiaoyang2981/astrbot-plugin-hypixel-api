def get_stats(player: dict, display_name: str) -> dict:
    s = player.get("stats", {}).get("Blitz", {})
    return {
        "display_name": display_name,
        "coins": s.get("coins", 0),
        "wins": s.get("wins", 0),
        "kills": s.get("kills", 0),
        "deaths": s.get("deaths", 0),
        "games_played": s.get("games_played", 0),
        "wins_teams": s.get("wins_teams", 0),
        "kills_teams": s.get("kills_teams", 0),
        "wins_solo": s.get("wins_solo", 0),
        "kills_solo": s.get("kills_solo", 0),
        "chests_opened": s.get("chests_opened", 0),
        "time_played": s.get("time_played", 0),
    }
