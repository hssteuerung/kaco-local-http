from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from .const import DOMAIN

# M11 voltage/current scaling is provisional; verify against inverter display.
DESCRIPTIONS = [
    ('pac','AC-Leistung','W',SensorDeviceClass.POWER,SensorStateClass.MEASUREMENT,1),
    ('tmp','Temperatur','°C',SensorDeviceClass.TEMPERATURE,SensorStateClass.MEASUREMENT,0.1),
    ('fac','Netzfrequenz','Hz',SensorDeviceClass.FREQUENCY,SensorStateClass.MEASUREMENT,0.01),
    ('vac0','Netzspannung','V',SensorDeviceClass.VOLTAGE,SensorStateClass.MEASUREMENT,0.1),
    ('iac0','Netzstrom','A',SensorDeviceClass.CURRENT,SensorStateClass.MEASUREMENT,0.1),
    ('sac','Scheinleistung','VA',SensorDeviceClass.APPARENT_POWER,SensorStateClass.MEASUREMENT,1),
    ('err','Fehlercode',None,None,None,1),
    ('flg','Status-Rohwert',None,None,None,1),
    ('etd','Tagesertrag Rohwert',None,None,None,1),
    ('eto','Gesamtertrag Wechselrichter','kWh',SensorDeviceClass.ENERGY,SensorStateClass.TOTAL_INCREASING,0.1),
    ('vpv0','PV1 Spannung','V',SensorDeviceClass.VOLTAGE,SensorStateClass.MEASUREMENT,0.1),
    ('vpv1','PV2 Spannung','V',SensorDeviceClass.VOLTAGE,SensorStateClass.MEASUREMENT,0.1),
    ('ipv0','PV1 Strom','A',SensorDeviceClass.CURRENT,SensorStateClass.MEASUREMENT,0.01),
    ('ipv1','PV2 Strom','A',SensorDeviceClass.CURRENT,SensorStateClass.MEASUREMENT,0.01),
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator, _, status = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([*(KacoSensor(coordinator, entry, status, *desc) for desc in DESCRIPTIONS), KacoStatusSensor(coordinator, entry, status, "connection"), KacoStatusSensor(coordinator, entry, status, "last_success")])

class KacoSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, status, key, name, unit, device_class, state_class, scale):
        super().__init__(coordinator)
        self.status = status
        self.key = key
        self.scale = scale
        self._attr_unique_id = f"{entry.data['serial']}_{key}"
        self._attr_name = name
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._attr_device_info = DeviceInfo(identifiers={(DOMAIN, entry.data['serial'])}, name=f"KACO {entry.data['serial']}", manufacturer='KACO', model='blueplanet NX1 M2')

    @property
    def available(self):
        # Keep last valid values when the HTTP poll fails.
        return True

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        if self.key.endswith(('0','1')) and self.key.startswith(('vac','iac','vpv','ipv')):
            idx = int(self.key[-1])
            values = data.get(self.key[:-1])
            raw = values[idx] if isinstance(values, list) and len(values) > idx else None
        else:
            raw = data.get(self.key)
        # Only instantaneous power is replaced by zero while offline.
        # This is a fallback value, never a measured inverter reading.
        if not self.status["online"] and self.key in ("pac", "sac"):
            return 0
        return round(raw * self.scale, 3) if isinstance(raw, (int, float)) else raw

    @property
    def extra_state_attributes(self):
        return {
            **({"umrechnung": "Originalwert eto / 10; mit KACO-App abgeglichen"} if self.key == "eto" else {}),
            "messwert_status": ("aktuell" if self.status["online"] else
                ("Ersatzwert 0 (offline)" if self.key in ("pac", "sac") else "letzter empfangener Wert")),
            "original_http_feld": self.key,
        }


class KacoStatusSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, status, key):
        super().__init__(coordinator)
        self.status = status
        self.key = key
        self._attr_unique_id = f"{entry.data['serial']}_{key}"
        self._attr_name = "Verbindung" if key == "connection" else "Letzte erfolgreiche Aktualisierung"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data['serial'])},
            name=f"KACO {entry.data['serial']}",
            manufacturer="KACO", model="blueplanet NX1 M2",
        )
        if key == "last_success":
            self._attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def available(self):
        return True

    @property
    def native_value(self):
        if self.key == "connection":
            return "Online" if self.status["online"] else "Offline"
        return self.status["last_success"]
