import asyncio
import aiohttp

BASE_URL = "https://api.hypixel.net/v2"


class HypixelClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._session: aiohttp.ClientSession | None = None

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _get(self, endpoint: str, params: dict | None = None) -> dict:
        await self._ensure_session()
        if params is None:
            params = {}
        params["key"] = self.api_key
        url = f"{BASE_URL}{endpoint}"
        async with self._session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            data = await resp.json()
            if not data.get("success"):
                raise Exception(data.get("cause", "Unknown API error"))
            return data

    async def get_player(self, uuid: str) -> dict:
        return await self._get("/player", {"uuid": uuid})

    async def get_player_by_name(self, name: str) -> dict:
        return await self._get("/player", {"name": name})

    async def _lookup_player(self, uuid=None, name=None) -> tuple[dict, str]:
        if uuid:
            player_data = await self.get_player(uuid)
        elif name:
            player_data = await self.get_player_by_name(name)
        else:
            raise ValueError("uuid or name required")
        player = player_data.get("player")
        if not player:
            raise Exception("Player not found")
        display_name = player.get("displayname", "Unknown")
        return player, display_name

    async def get_bedwars_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        player, display_name = await self._lookup_player(uuid=uuid, name=name)
        stats = player.get("stats", {}).get("Bedwars", {})
        level = (player.get("achievements", {}).get("bedwars_level", 0) or stats.get("Experience", 0))
        if not isinstance(level, int):
            level = 0
        return {
            "display_name": display_name, "level": level,
            "wins": stats.get("wins_bedwars", 0), "losses": stats.get("losses_bedwars", 0),
            "final_kills": stats.get("final_kills_bedwars", 0), "final_deaths": stats.get("final_deaths_bedwars", 0),
            "kills": stats.get("kills_bedwars", 0), "deaths": stats.get("deaths_bedwars", 0),
            "beds_broken": stats.get("beds_broken_bedwars", 0), "beds_lost": stats.get("beds_lost_bedwars", 0),
            "games_played": stats.get("games_played_bedwars", 0), "winstreak": stats.get("winstreak", 0),
            "coins": stats.get("coins", 0),
        }

    async def get_skywars_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        player, display_name = await self._lookup_player(uuid=uuid, name=name)
        stats = player.get("stats", {}).get("SkyWars", {})
        return {
            "display_name": display_name, "level": stats.get("levelFormatted", "N/A"),
            "wins": stats.get("wins", 0), "losses": stats.get("losses", 0),
            "kills": stats.get("kills", 0), "deaths": stats.get("deaths", 0),
            "souls": stats.get("souls", 0), "coins": stats.get("coins", 0),
            "games_played": stats.get("games_played", 0), "heads": stats.get("heads", 0),
        }

    async def get_arcade_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        player, display_name = await self._lookup_player(uuid=uuid, name=name)
        arcade = player.get("stats", {}).get("Arcade", {})
        coins = player.get("achievements", {}).get("arcade_arcade_arcade", 0)
        wins = arcade.get("wins", 0)
        total_rounds = arcade.get("rounds_played", 0)
        game_wins = {}
        for key, val in arcade.items():
            if key.startswith("wins_"):
                game_wins[key[5:]] = val
        top_games = sorted(game_wins.items(), key=lambda x: x[1], reverse=True)[:5]
        return {
            "display_name": display_name, "coins": coins,
            "wins": wins, "rounds_played": total_rounds, "top_games": top_games,
        }

    async def get_zombies_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        player, display_name = await self._lookup_player(uuid=uuid, name=name)
        a = player.get("stats", {}).get("Arcade", {})
        aliases = {"zombie_dead_end_best_round": "死胡同", "zombie_bad_blood_best_round": "坏血", "zombie_alien_arcadium_best_round": "异星方舟"}
        maps = {cn: a.get(key, 0) for key, cn in aliases.items()}
        return {
            "display_name": display_name,
            "wins": a.get("zombie_wins", 0), "losses": a.get("zombie_losses", 0),
            "kills": a.get("zombie_kills", 0), "deaths": a.get("zombie_deaths", 0),
            "headshots": a.get("zombie_headshots", 0), "games_played": a.get("zombie_games_played", 0),
            "doors_opened": a.get("zombie_doors_opened", 0), "chests_looted": a.get("zombie_chests_looted", 0),
            "rounds_survived": a.get("zombie_total_rounds_survived", 0), "best_round": a.get("zombie_best_round", 0),
            "maps": maps,
        }

    async def get_party_games_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        player, display_name = await self._lookup_player(uuid=uuid, name=name)
        a = player.get("stats", {}).get("Arcade", {})
        round_wins = a.get("party_games_round_wins", 0)
        total_rounds = a.get("party_games_total_rounds_played", 0)
        mini_wins = {}
        for key, val in a.items():
            if key.startswith("party_games_wins_"):
                mini_wins[key[17:]] = val
        top_party = sorted(mini_wins.items(), key=lambda x: x[1], reverse=True)[:6]
        return {
            "display_name": display_name, "round_wins": round_wins,
            "total_rounds": total_rounds, "mini_games": top_party,
        }

    async def get_blitz_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        player, display_name = await self._lookup_player(uuid=uuid, name=name)
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

    async def get_player_rank_info(self, uuid: str | None = None, name: str | None = None) -> dict:
        player, display_name = await self._lookup_player(uuid=uuid, name=name)
        raw_rank = player.get("rank", "NONE")
        new_pkg = player.get("newPackageRank", "")
        pkg = player.get("packageRank", "")
        monthly = player.get("monthlyPackageRank", "NONE")
        rank = raw_rank
        if rank in ("NORMAL", "NONE") and new_pkg:
            rank = new_pkg
        if rank in ("NORMAL", "NONE") and pkg:
            rank = pkg
        if monthly == "SUPERSTAR":
            rank = "MVP++"
        return {
            "display_name": player.get("displayname", "Unknown"),
            "uuid": player.get("uuid", "Unknown"),
            "rank": rank,
            "prefix": player.get("prefix", ""),
            "mvp_plus_color": player.get("rankPlusColor", "RED"),
            "first_login": player.get("firstLogin", 0),
            "last_login": player.get("lastLogin", 0),
            "last_logout": player.get("lastLogout", 0),
            "network_level": (player.get("networkExp", 0) or 0),
            "karma": player.get("karma", 0),
            "language": player.get("userLanguage", "ENGLISH"),
        }
