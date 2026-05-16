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

    async def get_bedwars_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        if uuid:
            player_data = await self.get_player(uuid)
        elif name:
            player_data = await self.get_player_by_name(name)
        else:
            raise ValueError("uuid or name required")

        player = player_data.get("player")
        if not player:
            raise Exception("Player not found")

        stats = player.get("stats", {}).get("Bedwars", {})
        display_name = player.get("displayname", "Unknown")

        level = (player.get("achievements", {}).get("bedwars_level", 0)
                 or stats.get("Experience", 0))
        if not isinstance(level, int):
            level = 0

        return {
            "display_name": display_name,
            "level": level,
            "wins": stats.get("wins_bedwars", 0),
            "losses": stats.get("losses_bedwars", 0),
            "final_kills": stats.get("final_kills_bedwars", 0),
            "final_deaths": stats.get("final_deaths_bedwars", 0),
            "kills": stats.get("kills_bedwars", 0),
            "deaths": stats.get("deaths_bedwars", 0),
            "beds_broken": stats.get("beds_broken_bedwars", 0),
            "beds_lost": stats.get("beds_lost_bedwars", 0),
            "games_played": stats.get("games_played_bedwars", 0),
            "winstreak": stats.get("winstreak", 0),
            "coins": stats.get("coins", 0),
        }

    async def get_skywars_stats(self, uuid: str | None = None, name: str | None = None) -> dict:
        if uuid:
            player_data = await self.get_player(uuid)
        elif name:
            player_data = await self.get_player_by_name(name)
        else:
            raise ValueError("uuid or name required")

        player = player_data.get("player")
        if not player:
            raise Exception("Player not found")

        stats = player.get("stats", {}).get("SkyWars", {})
        display_name = player.get("displayname", "Unknown")

        return {
            "display_name": display_name,
            "level": stats.get("levelFormatted", "N/A"),
            "wins": stats.get("wins", 0),
            "losses": stats.get("losses", 0),
            "kills": stats.get("kills", 0),
            "deaths": stats.get("deaths", 0),
            "souls": stats.get("souls", 0),
            "coins": stats.get("coins", 0),
            "games_played": stats.get("games_played", 0),
            "heads": stats.get("heads", 0),
        }

    async def get_guild(self, player_uuid: str) -> dict | None:
        data = await self._get("/guild", {"player": player_uuid})
        guild = data.get("guild")
        if not guild:
            return None
        return {
            "name": guild.get("name", "Unknown"),
            "tag": guild.get("tag", ""),
            "members": len(guild.get("members", [])),
            "level": guild.get("exp", 0),
        }

    async def get_player_rank_info(self, uuid: str | None = None, name: str | None = None) -> dict:
        if uuid:
            player_data = await self.get_player(uuid)
        elif name:
            player_data = await self.get_player_by_name(name)
        else:
            raise ValueError("uuid or name required")

        player = player_data.get("player")
        if not player:
            raise Exception("Player not found")

        rank = player.get("rank", "NONE")
        prefix = player.get("prefix", "")
        mvp_plus_color = player.get("monthlyPackageRank", "NONE")
        rank_plus = player.get("rankPlusColor", "RED")

        return {
            "display_name": player.get("displayname", "Unknown"),
            "uuid": player.get("uuid", "Unknown"),
            "rank": rank,
            "prefix": prefix,
            "mvp_plus_color": mvp_plus_color,
            "rank_plus_color": rank_plus,
            "first_login": player.get("firstLogin", 0),
            "last_login": player.get("lastLogin", 0),
            "last_logout": player.get("lastLogout", 0),
            "network_level": (player.get("networkExp", 0) or 0),
            "karma": player.get("karma", 0),
            "language": player.get("userLanguage", "ENGLISH"),
        }