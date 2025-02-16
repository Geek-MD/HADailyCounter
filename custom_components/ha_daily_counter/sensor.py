from homeassistant.helpers.entity import Entity
from .const import DOMAIN
async def async_setup_entry(hass, entry, async_add_entities):
    counters = hass.data[DOMAIN]["counters"]
    async_add_entities([DailyCounterSensor(counter) for counter in counters.values()])
class DailyCounterSensor(Entity):
    def __init__(self, counter):
        self._counter = counter
    @property
    def name(self):
        return f"Counter {self._counter.name}"
    @property
    def state(self):
        return self._counter.value
    @property
    def unit_of_measurement(self):
        return "events"
