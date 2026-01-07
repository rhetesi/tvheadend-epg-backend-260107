import asyncio
import logging
from datetime import timedelta
from typing import Any

from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.core import HomeAssistant

from .api.http import (
    TVHHttpApi,
    TVHHttpAuthError,
    TVHHttpConnectionError,
    TVHHttpRequestError,
)

_LOGGER = logging.getLogger(__name__)


class TVHEPGCoordinator(DataUpdateCoordinator[Any]):
    """Coordinator for TVHeadend EPG updates."""

    def __init__(
        self,
        hass: HomeAssistant,
        http_api: TVHHttpApi,
        storage,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            name="TVHeadend EPG",
            update_interval=timedelta(minutes=15),
        )

        self._http_api = http_api
        self._storage = storage
        self._lock = asyncio.Lock()

    async def _async_update_data(self) -> Any:
        """Fetch data from TVHeadend and store it."""
        async with self._lock:
            try:
                _LOGGER.debug("Starting TVHeadend EPG update")

                epg = await self._http_api.get_epg()

                await self._storage.save(epg)

                _LOGGER.debug("TVHeadend EPG update successful")
                return epg

            except TVHHttpAuthError as err:
                _LOGGER.error("TVHeadend authentication failed: %s", err)
                raise UpdateFailed("Authentication failed") from err

            except TVHHttpConnectionError as err:
                _LOGGER.error("TVHeadend connection error: %s", err)
                raise UpdateFailed("Cannot connect to TVHeadend") from err

            except TVHHttpRequestError as err:
                _LOGGER.error("TVHeadend HTTP error: %s", err)
                raise UpdateFailed("TVHeadend HTTP error") from err

            except Exception as err:
                _LOGGER.exception("Unexpected error during TVHeadend EPG update")
                raise UpdateFailed(err) from err

    async def force_refresh(self) -> None:
        """Force refresh EPG data (e.g. from frontend)."""
        _LOGGER.debug("Force refresh requested for TVHeadend EPG")
        await self.async_refresh()
