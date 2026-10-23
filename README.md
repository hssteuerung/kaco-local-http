# KACO Local HTTP

**Lokale Home-Assistant-Integration für KACO blueplanet NX1 M2 mit M11-WLAN-Kommunikationseinheit.**

![KACO LOCAL Logo](custom_components/kaco_local_http/logo.png)

**Version:** `2026.10.1` · **Status:** erste GitHub-Veröffentlichung, noch nicht vollständig auf unterschiedlichen Geräten getestet · **Sprache:** Deutsch

> Unabhängiges Community-Projekt. Keine offizielle Integration von KACO. KACO und zugehörige Marken sind Eigentum der jeweiligen Rechteinhaber. Das gestaltete Logo ist ein Community-Motiv und keine offizielle Freigabe durch KACO.

## Funktionen

- Lokale HTTP-Abfrage ohne Cloud über die M11-Kommunikationseinheit (standardmäßig Port `8484`).
- Konfiguration über **Einstellungen → Geräte & Dienste → Integration hinzufügen**.
- Sensoren für AC-Leistung, Scheinleistung, Netzspannung, Netzstrom, Netzfrequenz, Temperatur, Fehlercode, Status-Rohwert sowie PV1/PV2-Spannung und -Strom.
- Originaler Gesamtertrag `eto / 10` in **kWh** (gegen KACO-App abgeglichen).
- Tagesertrag `etd` zunächst **als Rohwert**, da seine Skalierung noch nicht bestätigt ist.
- Bei Offline-Verbindung **0 W** für AC-Leistung und **0 VA** für Scheinleistung als *Ersatzwert*; andere Sensoren behalten den letzten empfangenen Wert.
- Zwischenspeicherung der zuletzt erfolgreichen Messdaten und Wiederherstellung nach Home-Assistant-Neustart, sobald mindestens eine Messung gespeichert wurde.
- Sensoren für Verbindungsstatus und letzte erfolgreiche Aktualisierung.

**Wichtig:** Offline-0-W ist **keine echte Messung**. Bei einer Netzwerkstörung am Tag kann der Wechselrichter trotzdem Strom erzeugen. Verwende den Verbindungsstatus, um solche Werte zu erkennen. Die PV-String-Leistung und getrennte String-Erträge werden **nicht geschätzt**.

## Voraussetzungen

- Home Assistant mit Unterstützung für benutzerdefinierte Integrationen.
- KACO blueplanet NX1 M2 mit erreichbarer M11-WLAN-Einheit und lokaler HTTP-Schnittstelle.
- Die Abfrage `http://WECHSELRICHTER-IP:8484/getdev.cgi?device=2` muss eine `inv`-Liste mit `isn` liefern.
- Das Gerät und Home Assistant müssen sich im Netzwerk erreichen können.

Bisher anhand eines **blueplanet 3.0 NX1 M2 / M11 / Firmware 21618-006R** erprobt. Andere Modelle/Firmwares sind nicht bestätigt.

## Installation über HACS (benutzerdefiniertes Repository)

1. Dieses Repository in GitHub veröffentlichen.
2. In Home Assistant **HACS → Drei-Punkte-Menü → Benutzerdefinierte Repositories** öffnen.
3. Repository-URL `https://github.com/hssteuerung/kaco-local-http` eintragen, Typ **Integration** wählen und hinzufügen.
4. **KACO Local HTTP** in HACS installieren.
5. Home Assistant neu starten.
6. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach **KACO Local HTTP** suchen.
7. IP/Hostname und Port eingeben (Standard `8484`).

Die genaue Menübezeichnung kann je nach HACS-Version abweichen. **Die Integration ist nicht automatisch im offiziellen HACS-Katalog gelistet.**

## Manuelle Installation

Den Ordner `custom_components/kaco_local_http` aus diesem Repository nach `/config/custom_components/kaco_local_http` kopieren und Home Assistant neu starten. Danach über **Geräte & Dienste** einrichten.

## Sensoren und Datenherkunft

| Sensor | HTTP-Feld | Anzeige / Hinweis |
|---|---|---|
| AC-Leistung | `pac` | W, offline Ersatzwert 0 W |
| Scheinleistung | `sac` | VA, offline Ersatzwert 0 VA |
| Gesamtertrag Wechselrichter | `eto` | `eto / 10` kWh, mit KACO-App bestätigt |
| Tagesertrag Rohwert | `etd` | Unskalierter Originalwert |
| Temperatur | `tmp` | `/10` °C, Skalierung noch geräteabhängig prüfen |
| Netzfrequenz | `fac` | `/100` Hz |
| Netzspannung | `vac[0]` | `/10` V |
| Netzstrom | `iac[0]` | `/10` A, Skalierung prüfen |
| PV1 / PV2 Spannung | `vpv[0/1]` | `/10` V |
| PV1 / PV2 Strom | `ipv[0/1]` | `/100` A |
| Fehlercode | `err` | Rohwert |
| Status-Rohwert | `flg` | Rohwert |
| Verbindung | HTTP-Erreichbarkeit | Online / Offline |
| Letzte erfolgreiche Aktualisierung | lokaler Zeitstempel | Datum/Uhrzeit |


## Datenschutz und Sicherheit

Die Integration fragt die lokale HTTP-Adresse des Geräts ab und benötigt keine Cloud-Zugangsdaten. Die Verbindung ist **unverschlüsseltes HTTP**; nur in einem vertrauenswürdigen lokalen Netz einsetzen und den Port nicht ins Internet freigeben. Bei Fehlermeldungen bitte Registrierungscodes, Tokens und öffentliche IP-Adressen schwärzen.

## Fehlerbehebung

- **Nicht gefunden:** IP und Port prüfen; `getdev.cgi?device=2` im lokalen Netz testen.
- **Sensoren offline:** WLAN-Verbindung und Kommunikationsmodul prüfen; Messwerte bleiben ggf. gespeichert.
- **0 W trotz Sonne:** Verbindungsstatus prüfen – bei Offline ist 0 W ein Ersatzwert.
- **Logo fehlt:** Das Branding wird von Home Assistant separat verwaltet, siehe oben.

## Mitwirken

Fehlerberichte bitte mit Home-Assistant-Version, KACO-Modell, M11-Firmware, reproduzierbaren Schritten und anonymisierten Logs einreichen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

## Lizenz

Quellcode unter der [MIT-Lizenz](LICENSE). Marken- und Logo-Rechte bleiben bei den jeweiligen Inhabern; die Lizenz stellt keine Markenfreigabe dar.
