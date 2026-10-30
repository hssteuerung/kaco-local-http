# Changelog

## 2026.10.3 – NX1-/NX3-Unterstützung (Testversion)

### Neu
- Modellname aus dem Seriennummernpräfix (`isn`) abgeleitet; NX1 und NX3 werden unterschieden.
- Für dreiphasige Geräte zusätzliche Sensoren **Netzspannung L2/L3** und **Netzstrom L2/L3**, sofern die HTTP-Daten bei der Einrichtung drei Phasen enthalten.
- `mty` bleibt als Diagnose-Attribut `originalcode` sichtbar, wird aber nicht mehr über eine widersprüchliche Modellcode-Tabelle übersetzt.

### Behoben
- Ein blueplanet 20.0 NX3 M2 mit `mty: 51` wird nicht mehr fälschlich als blueplanet 4.0 NX1 angezeigt.
- Geräteinformationen zeigen nicht mehr pauschal „blueplanet NX1 M2“.

### Kompatibilität
- Bestehende Entitäts-IDs für Netzspannung/Netzstrom L1 bleiben unverändert.
- Die bekannten Sensoren, Diagnosewerte, das Offline-Verhalten und die Ertragsumrechnung bleiben bestehen.
- NX3-Testwerte für die Netzstromskalierung sind noch zu validieren.

## 2026.10.2 – Reguläres Release

- Lokale M11-HTTP-Abfrage und HACS-Installation.
- Tages- und Gesamtertrag `/10` in kWh; Leistungsfaktor `/100`.
- Betriebsstunden in `h` ohne Umrechnung.
- Blindleistung und Scheinleistung als Sensoren.
- Trennung von Sensoren und Diagnose einschließlich Ländercode und Erweiterungsstatus.
- Offline-Ersatzwert 0 W für AC-Leistung und Speicherung zuletzt erfolgreicher Daten.
- KACO-LOCAL-Branding und GitHub-Dokumentation.

> Die Version 2026.10.2 bleibt als veröffentlichter Stand unverändert. 2026.10.3 ist die nächste Testversion.
