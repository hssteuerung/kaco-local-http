from homeassistant.components.sensor import SensorEntity, SensorDeviceClass, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from .const import DOMAIN

# M11 voltage/current scaling is provisional; verify against inverter display.
DESCRIPTIONS = [
    ('pac','AC-Leistung','W',SensorDeviceClass.POWER,SensorStateClass.MEASUREMENT,1),
    ('tmp','Temperatur','°C',SensorDeviceClass.TEMPERATURE,SensorStateClass.MEASUREMENT,0.1),
    ('fac','Netzfrequenz','Hz',SensorDeviceClass.FREQUENCY,SensorStateClass.MEASUREMENT,0.01),
    ('vac0','Netzspannung','V',SensorDeviceClass.VOLTAGE,SensorStateClass.MEASUREMENT,0.1),
    ('iac0','Netzstrom','A',SensorDeviceClass.CURRENT,SensorStateClass.MEASUREMENT,0.1),
    ('sac','Scheinleistung','VA',SensorDeviceClass.APPARENT_POWER,SensorStateClass.MEASUREMENT,1),
    ('qac','Blindleistung','var',None,SensorStateClass.MEASUREMENT,1),
    ('etd','Tagesertrag','kWh',SensorDeviceClass.ENERGY,SensorStateClass.TOTAL_INCREASING,0.1),
    ('eto','Gesamtertrag Wechselrichter','kWh',SensorDeviceClass.ENERGY,SensorStateClass.TOTAL_INCREASING,0.1),
    ('vpv0','PV1 Spannung','V',SensorDeviceClass.VOLTAGE,SensorStateClass.MEASUREMENT,0.1),
    ('vpv1','PV2 Spannung','V',SensorDeviceClass.VOLTAGE,SensorStateClass.MEASUREMENT,0.1),
    ('ipv0','PV1 Strom','A',SensorDeviceClass.CURRENT,SensorStateClass.MEASUREMENT,0.01),
    ('ipv1','PV2 Strom','A',SensorDeviceClass.CURRENT,SensorStateClass.MEASUREMENT,0.01),
    ('pf','Leistungsfaktor',None,None,SensorStateClass.MEASUREMENT,0.01),
    ('hto','Betriebsstunden','h',SensorDeviceClass.DURATION,SensorStateClass.TOTAL_INCREASING,1),
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator, _, status = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([*(KacoSensor(coordinator, entry, status, *desc) for desc in DESCRIPTIONS), *(KacoDiagnosticSensor(coordinator, entry, status, key, name) for key, name in DIAGNOSTICS), KacoStatusSensor(coordinator, entry, status, "connection"), KacoStatusSensor(coordinator, entry, status, "last_success")])

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
            **({"hinweis": "Betriebsstunden mit KACO-App abgeglichen; Originalwert entspricht Stunden"} if self.key == "hto" else {}),
            **({"umrechnung": "Originalwert / 10; Tages- und Gesamtertrag mit KACO-App abgeglichen"} if self.key in ("eto", "etd") else {}),
            "messwert_status": ("aktuell" if self.status["online"] else
                ("Ersatzwert 0 (offline)" if self.key in ("pac", "sac") else "letzter empfangener Wert")),
            "original_http_feld": self.key,
        }


# Zuordnungen aus der gerätespezifischen Nutzertabelle; unbekannte Codes bleiben erkennbar.
COUNTRY_CODES = {
    70: "VDE-AR-N 4105 (Deutschland)",
    71: "VDE-AR-N 4110 (Deutschland)",
    72: "VDE-AR-N 4110 (Deutschland)",
    1: "IEC 61727 (International, 50 Hz)",
    2: "IEC 61727 (International, 60 Hz)",
    10: "EN 50549-1 (Europa)",
    14: "CEI 0-21 (Italien)",
    20: "TOR Erzeuger (Österreich)",
    30: "NA/EEA (Schweiz)",
    40: "G98 / G99 (Großbritannien)",
    50: "UTE C 15-712-1 (Frankreich)",
    80: "UNE / NTS (Spanien)",
}
MODEL_CODES = {
    47: "blueplanet 1.5 NX1", 48: "blueplanet 2.0 NX1",
    49: "blueplanet 3.0 NX1", 50: "blueplanet 3.6 NX1",
    51: "blueplanet 4.0 NX1", 52: "blueplanet 5.0 NX1",
    61: "blueplanet 3.0 NX3 M2", 62: "blueplanet 4.0 NX3 M2",
    63: "blueplanet 5.0 NX3 M2", 65: "blueplanet 8.0 NX3 M2",
    66: "blueplanet 10.0 NX3 M2", 67: "blueplanet 15.0 NX3 M2",
    68: "blueplanet 20.0 NX3 M2",
}

DIAGNOSTICS = [
    ("err", "Fehlercode"),
    ("add", "Geräteadresse"), ("safety", "Ländercode / Netzstandard"),
    ("mty", "Modelltyp"), ("psb_eb", "Peak Shaving / Erweiterung"),
    ("rate", "Nennleistung"),
]

class KacoDiagnosticSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, entry, status, key, name):
        super().__init__(coordinator)
        self.status = status
        self.key = key
        self._attr_unique_id = f"{entry.data['serial']}_{key}"
        self._attr_name = name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.data['serial'])},
            name=f"KACO {entry.data['serial']}", manufacturer="KACO", model="blueplanet NX1 M2",
        )
        if key == "psb_eb":
            self._attr_icon = "mdi:transmission-tower"
        if key == "rate":
            self._attr_native_unit_of_measurement = "W"

    @property
    def available(self):
        return True

    @property
    def native_value(self):
        raw = (self.coordinator.data or {}).get(self.key)
        if self.key == "safety" and raw is not None:
            return COUNTRY_CODES.get(raw, f"Unbekannter Ländercode ({raw})")
        if self.key == "mty" and raw is not None:
            return MODEL_CODES.get(raw, f"Unbekannter Modelltyp ({raw})")
        return raw

    @property
    def extra_state_attributes(self):
        if self.key == "psb_eb":
            return {
                "beschreibung": "Peak Shaving / Erweiterung (Protokollbedeutung nicht abschließend verifiziert)",
                "wert_1": "Enabled / aktiv (vermutete Bedeutung)",
                "hinweis": "Bei NX1-Modellen kann das Feld mit Energiemanagement- oder Zählererweiterungen zusammenhängen.",
                "original_http_feld": "psb_eb",
            }
        raw = (self.coordinator.data or {}).get(self.key)
        return {"original_http_feld": self.key, "originalcode": raw} if self.key in ("safety", "mty") else {"original_http_feld": self.key}


class KacoStatusSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, status, key):
        super().__init__(coordinator)
        self.status = status
        self.key = key
        self._attr_unique_id = f"{entry.data['serial']}_{key}"
        self._attr_name = "Verbindung" if key == "connection" else "Letzte erfolgreiche Aktualisierung"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
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
