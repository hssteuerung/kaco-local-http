from datetime import timedelta, datetime, timezone
import logging
from homeassistant.helpers.storage import Store
from urllib.parse import urlencode
import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    host = entry.data["host"]
    port = entry.data["port"]
    serial = entry.data["serial"]
    session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8))

    status = {"online": False, "last_success": None}
    # Last valid measurement snapshot survives HA restarts and inverter downtime.
    cache_store = Store(hass, 1, f"kaco_local_http_last_{entry.entry_id}")
    cache = await cache_store.async_load() or {}
    last_data = cache.get("data") if isinstance(cache.get("data"), dict) else {}
    if cache.get("last_success"):
        try:
            status["last_success"] = datetime.fromisoformat(cache["last_success"])
        except ValueError:
            pass

    async def fetch():
        nonlocal last_data
        url = f"http://{host}:{port}/getdevdata.cgi?" + urlencode({"device": 2, "sn": serial})
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json(content_type=None)
                if not isinstance(data, dict) or "pac" not in data:
                    raise UpdateFailed("Ungültige Messdaten")
                now = datetime.now(timezone.utc)
                status["online"] = True
                status["last_success"] = datetime.now(timezone.utc)
                last_data = data
                await cache_store.async_save({"data": data, "last_success": status["last_success"].isoformat()})
                return data
        except (aiohttp.ClientError, TimeoutError, ValueError, UpdateFailed) as err:
            status["online"] = False
            _LOGGER.debug("KACO offline, letzter Messwert bleibt erhalten: %s", err)
            return last_data

    coordinator = DataUpdateCoordinator(hass, _LOGGER, name="KACO Local HTTP", update_method=fetch, update_interval=timedelta(seconds=15))
    try:
        await coordinator.async_config_entry_first_refresh()
    except Exception:
        await session.close()
        raise
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = (coordinator, session, status)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok:
        _, session, _ = hass.data[DOMAIN].pop(entry.entry_id)
        await session.close()
    return ok
