# Changelog – KACO Local HTTP

Alle Änderungen an der veröffentlichten GitHub-/HACS-Reihe. Diese Version bündelt die bisherigen Änderungen und ersetzt den bisherigen Pre-Release-Stand `2026.10.2`.

## [2026.10.2] – Stabile Veröffentlichung: Sensoren, Diagnose und verständliche Werte

### Hinzugefügt

- Entitäten in Home Assistant nach **Sensoren** und **Diagnose** aufgeteilt (`entity_category: diagnostic` für technische Informationen).
- **Blindleistung** (`qac`) wieder als Messsensor mit Einheit **var** hinzugefügt.
- **Leistungsfaktor** (`pf`) als Messsensor: Umrechnung `/100`, zum Beispiel `99` → `0,99`.
- **Betriebsstunden** (`hto`) als Sensor in **h**; Originalwert ohne Umrechnung, mit KACO-App abgeglichen.
- Diagnose **Peak Shaving / Erweiterung** (`psb_eb`) mit unverändertem Originalwert und vorsichtiger Beschreibung der noch nicht abschließend verifizierten Bedeutung.
- Übersetzung bekannter **Ländercodes / Netzstandards** (`safety`), z. B. `70` → `VDE-AR-N 4105 (Deutschland)`.
- Übersetzung bekannter **Modelltypcodes** (`mty`), z. B. `49` → `blueplanet 3.0 NX1`; weitere NX1-/NX3-Zuordnungen hinterlegt, ohne eine Gerätekompatibilität zu garantieren.

### Geändert

- Nennleistung, Fehlercode, Geräteadresse, Ländercode, Modelltyp, Peak-Shaving-Feld, Verbindungsstatus und Zeitstempel der letzten erfolgreichen Aktualisierung unter **Diagnose** eingeordnet.
- Betriebsstunden nicht mehr als „Rohwert“ bezeichnet.
- Diagnosewerte behalten ihre ursprünglichen HTTP-Codes in Attributen, wo für die Zuordnung hilfreich.
- Dokumentation für den aktuellen Sensorumfang, die Skalierungen und das Offline-Verhalten aktualisiert.

### Entfernt

- Eigenständige Diagnose-Entität **Status-Rohwert** (`flg`). Das separate Feld `psb_eb` bleibt erhalten; beide Felder sind nicht gleichbedeutend.

### Unverändert

- Lokale HTTP-Kommunikation über M11/Port 8484 ohne Cloud.
- Offline-Ersatzwert **0 W** für AC-Leistung und **0 VA** für Scheinleistung; übrige Messwerte behalten den letzten erfolgreichen Stand.
- Keine berechnete oder geschätzte PV-String-Leistung beziehungsweise getrennte String-Erträge.
- KACO-LOCAL-Community-Branding und GitHub-/HACS-Paketstruktur.

### Weitere Korrektur: Tagesertrag

### Behoben

- **Tagesertrag** (`etd`) nicht mehr als unskalierter Rohwert: Umrechnung `etd / 10` und Anzeige in **kWh**.
- Tagesertrag als Energie-Entität mit passender Home-Assistant-Sensorklassifizierung geführt.

### Unverändert

- **Gesamtertrag** (`eto / 10` kWh), bereits mit der KACO-App abgeglichen.
- Lokale HTTP-Abfrage, Speicherung letzter gültiger Messwerte, Verbindungsdiagnose und Community-Branding.

## [2026.10.1] – Erste GitHub-Veröffentlichung

- Home-Assistant-Custom-Integration für KACO blueplanet NX1 M2 mit M11-WLAN-Kommunikationseinheit.
- Lokale HTTP-Abfrage über Port `8484`, deutscher Einrichtungsdialog.
- Messsensoren für AC-Leistung, Scheinleistung, Netzwerte, PV-String-Spannung/-Strom und Temperatur.
- Gesamtertrag `eto / 10` kWh, anhand der KACO-App geprüft.
- Offline-Ersatzwerte für momentane Leistung, Zwischenspeicherung zuletzt gültiger Daten und Wiederherstellung nach Neustart.
- Verbindungsstatus und Zeitstempel der letzten erfolgreichen Abfrage.
- Community-Logo sowie GitHub-/HACS-Dateien und grundlegende Dokumentation.

> **Kompatibilität:** Bisher anhand eines blueplanet 3.0 NX1 M2 mit M11-Firmware 21618-006R erprobt. Andere Modelle und Firmwareversionen sind nicht bestätigt. Nicht alle elektrischen Skalierungen sind unabhängig validiert.
