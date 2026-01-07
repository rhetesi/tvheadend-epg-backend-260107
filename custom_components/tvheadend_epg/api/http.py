import logging
import aiohttp
from typing import List

_LOGGER = logging.getLogger(__name__)


class TVHeadendHttpApi:
    def __init__(self, host: str, username: str, password: str, port: int = 9981):
        self._host = host.rstrip("/")
        self._username = username
        self._password = password
        self._port = port

    @property
    def _base_url(self) -> str:
        if self._host.startswith("http"):
            return f"{self._host}:{self._port}"
        return f"http://{self._host}:{self._port}"

    async def get_epg(self, limit: int = 1000) -> List[dict]:
        url = f"{self._base_url}/api/epg/events/grid"

        params = {
            "limit": limit,
        }

        auth = aiohttp.BasicAuth(self._username, self._password)

        _LOGGER.debug("Requesting EPG from %s", url)

        async with aiohttp.ClientSession(auth=auth) as session:
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    text = await response.text()
                    raise RuntimeError(
                        f"TVHeadend EPG request failed: {response.status} {text}"
                    )

                data = await response.json()

        # TVHeadend válasz tipikusan: { "entries": [...] }
        return data.get("entries", [])
