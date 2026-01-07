from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .api.http import TVHeadendHttpApi

_LOGGER = logging.getLogger(__name__)


class TVHeadendEpgCoordinator(DataUpdateCoordinator[list[dict[str, Any]]]):
    """Coordinator to manage TVHeadend EPG data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry

        self.api = TVHeadendHttpApi(
            host=entry.data["host"],
            port=entry.data["port"],
            username=entry.data["username"],
            password=entry.data["password"],
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=timedelta(minutes=15),
        )

    async def _async_update_data(self) -> list[dict[str, Any]]:
        """Fetch EPG data from TVHeadend."""
        try:
            epg = await self.api.get_epg()
            _LOGGER.debug("Fetched %s EPG events", len(epg))
            return epg
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Failed to fetch EPG: {err}") from err
