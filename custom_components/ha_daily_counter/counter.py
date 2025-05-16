import logging
from datetime import datetime, timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfNone
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

class HADailyCounterEntity(SensorEntity, RestoreEntity):
    def __init__(self, entry_id: str, counter_config: dict) -> None:
        self._entry_id = entry_id
        self._unique_id = f"{entry_id}_{counter_config['id']}"
        self._name = counter_config["name"]
        self._trigger_entity = counter_config["trigger_entity"]
        self._trigger_state = counter_config["trigger_state"]
        self._device_id = counter_config["id"]
        self._device_name = counter_config["name"]
        self._attr_native_value = 0

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def device_info(self) -> dict:
        return {
            "identifiers": {(self._entry_id, self._device_id)},
            "name": self._device_name,
            "manufacturer": "Geek-MD",
            "model": "HA Daily Counter",
            "entry_type": "service",
        }

    @property
    def native_value(self) -> int:
        return self._attr_native_value

    @property
    def native_unit_of_measurement(self) -> None:
        return None  # No unit, just a number

    async def async_added_to_hass(self) -> None:
        """Restore state and set up daily reset & trigger listener."""
        old_state = await self.async_get_last_state()
        if old_state and old_state.state.isdigit():
            self._attr_native_value = int(old_state.state)
            _LOGGER.debug("Restored state for %s: %s", self._name, self._attr_native_value)

        # Listen for changes in trigger entity
        self.async_on_remove(
            self.hass.helpers.event.async_track_state_change(
                self._trigger_entity,
                self._handle_trigger_state_change,
            )
        )

        # Daily reset at midnight
        self.async_on_remove(
            async_track_time_interval(self.hass, self._reset_counter, timedelta(days=1))
        )

    @callback
    def _handle_trigger_state_change(self, entity_id, old_state, new_state) -> None:
        if new_state is None:
            return

        if new_state.state == self._trigger_state:
            self._attr_native_value += 1
            self.async_write_ha_state()
            _LOGGER.debug("Counter '%s' incremented to %s", self._name, self._attr_native_value)

    @callback
    def _reset_counter(self, now) -> None:
        self._attr_native_value = 0
        self.async_write_ha_state()
        _LOGGER.debug("Counter '%s' reset to 0 at midnight", self._name)
