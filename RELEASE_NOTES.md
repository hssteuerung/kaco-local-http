# KACO Local HTTP 2026.10.1

Erste GitHub-Veröffentlichung der lokalen Home-Assistant-Integration für KACO blueplanet NX1 M2 mit M11-WLAN-Modul.

**Enthalten:** lokale HTTP-Messwerte über Port 8484, deutschsprachige Einrichtung, originaler Gesamtertrag in kWh (`eto / 10`), Offline-Ersatzwert 0 W für AC-Leistung, Speicherung letzter Messwerte, Online-/Offline-Status und KACO LOCAL Community-Branding-Dateien.

**Bekannte Einschränkungen:** Tagesertrag weiterhin als Rohwert; nicht alle Skalierungsfaktoren validiert; Integrationslogo wird in Home Assistant nicht allein durch lokale Bilddateien angezeigt; noch keine umfassenden Modelltests. Kein offizielles KACO-Produkt.

**Installation:** Repository in HACS als benutzerdefinierte Integration hinzufügen oder `custom_components/kaco_local_http` manuell kopieren und Home Assistant neu starten.
