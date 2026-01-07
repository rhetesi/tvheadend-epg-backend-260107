from homeassistant.components import websocket_api
from .const import DOMAIN

@websocket_api.websocket_command(
    {
        "type": "tvheadend_epg/get",
        "entry_id": str,
        "filters": dict,
    }
)
@websocket_api.async_response
async def ws_get_epg(hass, connection, msg):
    coordinator = hass.data[DOMAIN].get(msg["entry_id"])
    if not coordinator:
        connection.send_error(msg["id"], "not_found", "Invalid entry_id")
        return

    epg = await coordinator.storage.load()
    filters = msg.get("filters", {})

    if "channels" in filters:
        epg = [
            e for e in epg
            if e.get("channelName") in filters["channels"]
        ]

    if "tags" in filters:
        wanted = set(filters["tags"])
        epg = [
            e for e in epg
            if wanted & set(e.get("tags", []))
        ]

    connection.send_result(msg["id"], epg)


def async_register_ws(hass):
    websocket_api.async_register_command(hass, ws_get_epg)
