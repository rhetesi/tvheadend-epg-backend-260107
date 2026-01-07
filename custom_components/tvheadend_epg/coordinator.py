from datetime import timedelta
import logging

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class TVHeadendEPGCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=15),
        )

    async def _async_update_data(self):
        try:
            _LOGGER.debug("Fetching EPG data from TVHeadend")
            epg = await self.api.get_epg()
            _LOGGER.debug("Fetched %s EPG events", len(epg) if epg else 0)
            return epg
        except Exception as err:
            _LOGGER.error("EPG update failed: %s", err)
            raise UpdateFailed(err) from err
