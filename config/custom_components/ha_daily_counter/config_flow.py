import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN

class CounterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name", default="Contador Diario"): str,
                vol.Required("event_type", default="state_changed"): str,
                vol.Required("entity_id", default=""): str
            }),
        )
