import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components import websocket_api

from .const import DOMAIN
from .coordinator import TVHeadendEpgCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the TVHeadend EPG integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TVHeadend EPG from a config entry."""

    coordinator = TVHeadendEpgCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Register WebSocket command
    websocket_api.async_register_command(
        hass,
        websocket_epg_fetch,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True


# -----------------------------
# WebSocket API
# -----------------------------

@websocket_api.websocket_command(
    {
        "type": "tvheadend_epg/fetch",
        "entry_id": str,
    }
)
@websocket_api.async_response
async def websocket_epg_fetch(hass, connection, msg):
    """Fetch EPG data on demand (card opened)."""

    entry_id = msg["entry_id"]

    coordinator: TVHeadendEpgCoordinator | None = hass.data.get(DOMAIN, {}).get(entry_id)

    if coordinator is None:
        connection.send_error(
            msg["id"],
            "not_found",
            "TVHeadend EPG entry not found",
        )
        return

    try:
        await coordinator.async_request_refresh()
        data = coordinator.data
    except Exception as err:  # noqa: BLE001
        _LOGGER.exception("Failed to fetch EPG via websocket")
        connection.send_error(
            msg["id"],
            "update_failed",
            str(err),
        )
        return

    connection.send_result(
        msg["id"],
        {
            "epg": data,
        },
    )
