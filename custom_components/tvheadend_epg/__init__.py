import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN, PLATFORMS
from .coordinator import TVHEPGCoordinator
from .storage import EPGStorage
from .api.http import TVHHttpApi

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TVHeadend EPG from a config entry."""

    http_api = TVHHttpApi(
        base_url=entry.data["url"],
        username=entry.data["username"],
        password=entry.data["password"],
    )

    storage = EPGStorage(hass, entry.entry_id)

    coordinator = TVHEPGCoordinator(
        hass=hass,
        http_api=http_api,
        storage=storage,
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # 🔧 SERVICE REGISTRATION (ONCE)
    if not hass.services.has_service(DOMAIN, "refresh"):

        async def handle_refresh(call: ServiceCall) -> None:
            entry_id = call.data.get("entry_id")

            if entry_id:
                coord = hass.data.get(DOMAIN, {}).get(entry_id)
                if not coord:
                    _LOGGER.warning("No coordinator for entry_id %s", entry_id)
                    return
                await coord.force_refresh()
            else:
                # refresh all
                for coord in hass.data.get(DOMAIN, {}).values():
                    await coord.force_refresh()

        hass.services.async_register(
            DOMAIN,
            "refresh",
            handle_refresh,
        )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)

    return unload_ok
