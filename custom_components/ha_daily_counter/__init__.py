from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_component import async_get_entity_platform
from .const import DOMAIN
from .sensor import DailyCounterSensor

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Ensure entity is properly registered."""
    hass.data.setdefault(DOMAIN, {})
    platform = async_get_entity_platform(hass, "sensor", DOMAIN)
    sensor = DailyCounterSensor(hass, entry)
    await platform.async_add_entities([sensor], update_before_add=True)
    return True
