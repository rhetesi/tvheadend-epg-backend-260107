from .const import DOMAIN

def async_register_services(hass, coordinator):
    async def refresh(call):
        await coordinator.async_request_refresh()

    async def record(call):
        event_id = call.data.get("event_id")
        if event_id:
            await coordinator.api.record_event(event_id)

    hass.services.async_register(DOMAIN, "refresh", refresh)
    hass.services.async_register(DOMAIN, "record", record)
