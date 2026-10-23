from urllib.parse import urlencode
import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, DEFAULT_HOST, DEFAULT_PORT

class KacoFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            host = user_input["host"].strip()
            port = user_input["port"]
            try:
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                    url = f"http://{host}:{port}/getdev.cgi?" + urlencode({"device": 2})
                    async with session.get(url) as response:
                        response.raise_for_status()
                        data = await response.json(content_type=None)
                devices = data.get("inv", [])
                if not devices or not devices[0].get("isn"):
                    errors["base"] = "no_inverter"
                else:
                    serial = str(devices[0]["isn"])
                    await self.async_set_unique_id(serial)
                    self._abort_if_unique_id_configured()
                    return self.async_create_entry(title=f"KACO {serial}", data={"host": host, "port": port, "serial": serial})
            except (aiohttp.ClientError, TimeoutError, ValueError, TypeError):
                errors["base"] = "cannot_connect"
        schema = vol.Schema({vol.Required("host", default=DEFAULT_HOST): str, vol.Required("port", default=DEFAULT_PORT): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535))})
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
