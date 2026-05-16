import aiohttp

BASE_URL = "https://api.mcbjd.net/v2"


class BuGLandClient:
    def __init__(self, token: str):
        self.token = token
        self._session: aiohttp.ClientSession | None = None

    async def _ensure_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def _post(self, endpoint: str, data: dict | None = None) -> dict:
        await self._ensure_session()
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{BASE_URL}{endpoint}"
        async with self._session.post(url, json=data or {}, headers=headers,
                                      timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def get_player(self, name: str) -> dict:
        return await self._post("/player", {"nickname": name})

    async def get_gamestats(self, name: str, game: str = "") -> dict:
        return await self._post("/gamestats", {"nickname": name, "game": game})

    async def get_leaderboard(self, game: str = "", page: int = 1) -> dict:
        return await self._post("/leaderboard", {"game": game, "page": page})

    async def get_blitz_stats(self, name: str) -> dict:
        """Blitz 战绩 — 对局记录聚合"""
        data = await self.get_gamestats(name, game="blitz")
        return {
            "display_name": name,
            "wins": data.get("wins", 0),
            "kills": data.get("kills", 0),
            "deaths": data.get("deaths", 0),
            "games_played": data.get("games", 0),
            "wins_teams": data.get("teamWins", 0),
            "kills_teams": data.get("teamKills", 0),
            "wins_solo": data.get("soloWins", 0),
            "kills_solo": data.get("soloKills", 0),
            "coins": data.get("coins", 0),
            "chests_opened": data.get("chests", 0),
            "time_played": data.get("playTime", 0),
        }
