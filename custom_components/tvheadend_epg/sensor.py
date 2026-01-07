from homeassistant.components.sensor import SensorEntity

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([TVHEPGStatusSensor(entry.entry_id)])

class TVHEPGStatusSensor(SensorEntity):
    _attr_icon = "mdi:television-guide"

    def __init__(self, entry_id):
        self._attr_name = f"TVHeadend EPG ({entry_id})"
        self._attr_unique_id = f"tvheadend_epg_status_{entry_id}"

    @property
    def native_value(self):
        return "ok"
