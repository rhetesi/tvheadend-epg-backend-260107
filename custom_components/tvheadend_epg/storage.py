from homeassistant.helpers.storage import Store

class EPGStorage:
    def __init__(self, hass, entry_id):
        self.store = Store(hass, 1, f"tvheadend_epg_{entry_id}")

    async def load(self):
        return await self.store.async_load() or []

    async def save(self, data):
        await self.store.async_save(data)
