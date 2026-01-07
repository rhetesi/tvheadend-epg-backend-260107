import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import websocket_api

from .const import DOMAIN
from .coordinator import TVHeadendEPGCoordinator
from .api.http import TVHeadendHttpApi

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    _LOGGER.info("Setting up TVHeadend EPG integration")

    api = TVHeadendHttpApi(
        host=entry.data["host"],
        username=entry.data["username"],
        password=entry.data["password"],
    )

    coordinator = TVHeadendEPGCoordinator(hass, api)

    # Initial refresh (startup)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    async def websocket_get_epg(hass, connection, msg):
        entry_id = msg.get("entry_id")
        _LOGGER.debug("WebSocket get_epg called for entry_id=%s", entry_id)

        coord = hass.data.get(DOMAIN, {}).get(entry_id)
        if coord is None:
            connection.send_error(
                msg["id"],
                "not_found",
                "TVHeadend EPG config entry not found",
            )
            return

        # 🔥 Fallback logika:
        # panel megnyitás → azonnali frissítés
        await coord.async_refresh()

        connection.send_result(msg["id"], coord.data)

    websocket_api.async_register_command(
        hass,
        websocket_api.WebSocketCommand(
            {
                "type": "tvheadend_epg/get_epg",
                "entry_id": str,
            },
            websocket_get_epg,
        ),
    )

    _LOGGER.info("TVHeadend EPG WebSocket API registered")

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    _LOGGER.info("TVHeadend EPG integration unloaded")
    return True
