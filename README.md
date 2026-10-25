# KACO Local HTTP

**Lokale Home-Assistant-Integration für KACO blueplanet NX1 M2 mit M11-WLAN-Kommunikationseinheit.**

![KACO LOCAL Logo](custom_components/kaco_local_http/brand/logo.png)

**Status:** Community-Projekt; noch nicht vollständig auf unterschiedlichen Geräten getestet  
**Sprache:** Deutsch  
**Aktuelle Version:** `2026.10.2`

> Unabhängiges Community-Projekt. Keine offizielle Integration von KACO. KACO und zugehörige Marken sind Eigentum der jeweiligen Rechteinhaber. Das gestaltete Logo ist ein Community-Motiv und keine offizielle Freigabe durch KACO.

## Funktionen

- Lokale HTTP-Abfrage ohne Cloud über die M11-Kommunikationseinheit (standardmäßig Port `8484`).
- Konfiguration über **Einstellungen → Geräte & Dienste → Integration hinzufügen**.
- Messwerte für AC-Leistung, Scheinleistung, Blindleistung, Leistungsfaktor, Tages- und Gesamtertrag, Betriebsstunden, Temperatur, Netzspannung/-strom/-frequenz und PV1/PV2-Spannung/-Strom.
- Klare Trennung in **Sensoren** und **Diagnose** in Home Assistant.
- Diagnosewerte für Verbindung, letzte erfolgreiche Aktualisierung, Fehlercode, Nennleistung, Geräteadresse, Ländercode/Netzstandard, Modelltyp und Peak Shaving / Erweiterung.
- Verständliche Bezeichnungen für bekannte Modellcodes und Ländercodes statt bloßer Zahlenwerte.
- Zwischenspeicherung der zuletzt erfolgreichen Messdaten und Wiederherstellung nach einem Home-Assistant-Neustart, sobald mindestens eine Messung gespeichert wurde.
- Keine Schätzung der PV-String-Leistung oder einzelner String-Erträge.

**Wichtig:** Der Offline-Ersatzwert **0 W** (bzw. **0 VA** für Scheinleistung) ist **keine echte Messung**. Bei einer Netzwerkstörung am Tag kann der Wechselrichter weiterhin Strom erzeugen. Prüfe dafür den Verbindungsstatus. Andere Messwerte behalten bei Verbindungsabbruch ihren letzten empfangenen Stand und können veraltet sein.

## Voraussetzungen

- Home Assistant mit Unterstützung für benutzerdefinierte Integrationen.
- KACO blueplanet NX1 M2 mit erreichbarer M11-WLAN-Einheit und lokaler HTTP-Schnittstelle.
- `http://WECHSELRICHTER-IP:8484/getdev.cgi?device=2` muss eine `inv`-Liste mit `isn` liefern.
- Home Assistant und Wechselrichter müssen sich im lokalen Netzwerk erreichen können.

Bisher anhand eines **blueplanet 3.0 NX1 M2 / M11 / Firmware 21618-006R** erprobt. Andere Modelle/Firmwares sind nicht bestätigt. Die vorhandenen NX3-Modellzuordnungen bedeuten **keine bestätigte NX3-Kompatibilität**.

## Installation über HACS (benutzerdefiniertes Repository)

1. In Home Assistant **HACS → Drei-Punkte-Menü → Benutzerdefinierte Repositories** öffnen.
2. Repository-URL `https://github.com/hssteuerung/kaco-local-http` eintragen, Typ **Integration** wählen und hinzufügen.
3. **KACO Local HTTP** in HACS installieren.
4. Home Assistant neu starten.
5. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **KACO Local HTTP** suchen.
6. IP/Hostname und Port eingeben (Standard `8484`).

Die genaue Menübezeichnung kann je nach HACS-Version abweichen. **Die Integration ist nicht automatisch im offiziellen HACS-Katalog gelistet.** Das Repository muss dafür auf GitHub veröffentlicht sein.

## Manuelle Installation

Den Ordner `custom_components/kaco_local_http` aus diesem Repository nach `/config/custom_components/kaco_local_http` kopieren und Home Assistant neu starten. Danach über **Geräte & Dienste** einrichten.

## Sensoren und Datenherkunft

| Sensor | HTTP-Feld | Anzeige / Hinweis |
|---|---|---|
| AC-Leistung | `pac` | W; offline Ersatzwert 0 W |
| Scheinleistung | `sac` | VA; offline Ersatzwert 0 VA |
| Blindleistung | `qac` | var; Originalwert |
| Leistungsfaktor | `pf` | `/100`; z. B. `99` → `0,99` |
| Gesamtertrag Wechselrichter | `eto` | `/10` kWh; mit KACO-App abgeglichen |
| Tagesertrag | `etd` | `/10` kWh; mit KACO-App abgeglichen |
| Betriebsstunden | `hto` | h; Originalwert ohne Umrechnung, mit KACO-App abgeglichen |
| Temperatur | `tmp` | `/10` °C; Skalierung geräteabhängig prüfen |
| Netzfrequenz | `fac` | `/100` Hz |
| Netzspannung | `vac[0]` | `/10` V |
| Netzstrom | `iac[0]` | `/10` A; Skalierung prüfen |
| PV1 / PV2 Spannung | `vpv[0]` / `vpv[1]` | `/10` V; Skalierung prüfen |
| PV1 / PV2 Strom | `ipv[0]` / `ipv[1]` | `/100` A; Skalierung prüfen |

**Hinweis:** Nicht alle Spannungs-, Strom- und Temperatur-Skalierungen wurden unabhängig bestätigt. Vor einer Verwendung für Abrechnung oder Steuerung mit der Original-App vergleichen.

## Diagnose

| Diagnose | HTTP-Feld / Quelle | Anzeige / Bedeutung |
|---|---|---|
| Verbindung | HTTP-Erreichbarkeit | Online / Offline |
| Letzte erfolgreiche Aktualisierung | Lokaler Zeitstempel | Datum/Uhrzeit |
| Fehlercode | `err` | Originalcode; `0` = kein gemeldeter Fehler |
| Nennleistung | `rate` | W |
| Geräteadresse | `add` | Originalwert |
| Ländercode / Netzstandard | `safety` | Bekannter Code wird in Norm/Land übersetzt |
| Modelltyp | `mty` | Bekannter Code wird in Modellname übersetzt |
| Peak Shaving / Erweiterung | `psb_eb` | Originalwert; `1` vermutlich aktiv, Bedeutung nicht abschließend verifiziert |

Der separate **Status-Rohwert `flg`** wird in Version `2026.10.2` nicht mehr als Entität angelegt. `flg` und `psb_eb` sind unterschiedliche HTTP-Felder; ihre Bedeutungen dürfen nicht gleichgesetzt werden.

### Bekannte Ländercodes (`safety`)

Die folgenden Zuordnungen stammen aus einer gerätespezifischen Tabelle und sind nicht für alle Firmwareversionen unabhängig verifiziert.

| Code | Netzstandard / Land |
|---|---|
| `70` | VDE-AR-N 4105 (Deutschland) |
| `71`, `72` | VDE-AR-N 4110 (Deutschland) |
| `1` | IEC 61727 (International, 50 Hz) |
| `2` | IEC 61727 (International, 60 Hz) |
| `10` | EN 50549-1 (Europa) |
| `14` | CEI 0-21 (Italien) |
| `20` | TOR Erzeuger (Österreich) |
| `30` | NA/EEA (Schweiz) |
| `40` | G98 / G99 (Großbritannien) |
| `50` | UTE C 15-712-1 (Frankreich) |
| `80` | UNE / NTS (Spanien) |

Unbekannte Codes werden als solche mit ihrem Originalwert angezeigt.

### Bekannte Modellcodes (`mty`)

| Code | Modell | Code | Modell |
|---|---|---|---|
| `47` | blueplanet 1.5 NX1 | `61` | blueplanet 3.0 NX3 M2 |
| `48` | blueplanet 2.0 NX1 | `62` | blueplanet 4.0 NX3 M2 |
| `49` | blueplanet 3.0 NX1 | `63` | blueplanet 5.0 NX3 M2 |
| `50` | blueplanet 3.6 NX1 | `65` | blueplanet 8.0 NX3 M2 |
| `51` | blueplanet 4.0 NX1 | `66` | blueplanet 10.0 NX3 M2 |
| `52` | blueplanet 5.0 NX1 | `67` | blueplanet 15.0 NX3 M2 |
| | | `68` | blueplanet 20.0 NX3 M2 |

## Datenschutz und Sicherheit

Die Integration fragt die lokale HTTP-Adresse des Geräts ab und benötigt keine Cloud-Zugangsdaten. Die Verbindung ist **unverschlüsseltes HTTP**; nur in einem vertrauenswürdigen lokalen Netz einsetzen und den Port nicht ins Internet freigeben. Bei Fehlermeldungen bitte Registrierungscodes, Tokens und öffentliche IP-Adressen schwärzen.

## Fehlerbehebung

- **Nicht gefunden:** IP und Port prüfen; `getdev.cgi?device=2` im lokalen Netz testen.
- **Sensoren offline:** WLAN-Verbindung und Kommunikationsmodul prüfen; Messwerte bleiben gegebenenfalls gespeichert.
- **0 W trotz Sonne:** Verbindungsstatus prüfen – bei Offline ist 0 W ein Ersatzwert.
- **Alte Entitäten noch sichtbar:** Nicht mehr angelegte Entitäten gegebenenfalls unter **Einstellungen → Geräte & Dienste → Entitäten** entfernen.
- **Logo fehlt:** Home Assistant und HACS verwalten Branding teilweise getrennt; eine Anzeige in allen Ansichten ist nicht garantiert.

## Änderungen

Siehe [CHANGELOG.md](CHANGELOG.md) für die Versionshistorie.

## Mitwirken

Fehlerberichte bitte mit Home-Assistant-Version, KACO-Modell, M11-Firmware, reproduzierbaren Schritten und anonymisierten Logs einreichen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz

Quellcode unter der [MIT-Lizenz](LICENSE). Marken- und Logo-Rechte bleiben bei den jeweiligen Inhabern; die Lizenz stellt keine Markenfreigabe dar.
