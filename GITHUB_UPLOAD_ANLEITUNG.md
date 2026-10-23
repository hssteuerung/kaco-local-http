# GitHub-Veröffentlichung Schritt für Schritt

1. Auf github.com ein **öffentliches** Repository mit Namen `kaco-local-http` anlegen. Beim Anlegen **keine** README, Lizenz oder `.gitignore` hinzufügen – sie liegen bereits bei.
2. **Add file → Upload files** öffnen.
3. Den **Inhalt** des Ordners `kaco_local_http_github_2026.10.1` hochladen, nicht den äußeren Ordner als Unterordner. Für versteckte Dateien/Ordner wie `.github` und `.gitignore` ist Git oder GitHub Desktop zuverlässiger als Browser-Upload.
4. `README.md`, `hacs.json` und `custom_components/kaco_local_http/manifest.json` müssen im Repository an den vorgesehenen Stellen liegen.
5. In `manifest.json` die Platzhalter-URLs `hssteuerung` durch den eigenen GitHub-Namen ersetzen. Ebenso die Repository-URL in der README anpassen.
6. Unter **Releases → Draft a new release** Tag `2026.10.1`, Titel `KACO Local HTTP 2026.10.1` anlegen und die Texte aus `RELEASE_NOTES.md` einfügen. GitHub erzeugt automatisch Quellcode-Archive.
7. Das Repository in HACS als **benutzerdefiniertes Repository / Integration** hinzufügen und installieren.
8. Nach einem Neustart die Integration unter **Geräte & Dienste** hinzufügen.

Alternativ per Git:

```bash
git init
git add .
git commit -m "Release 2026.10.1"
git branch -M main
git remote add origin https://github.com/hssteuerung/kaco-local-http.git
git push -u origin main
```

**Hinweis:** Die Logo-Dateien im Repository garantieren kein sichtbares Integrationslogo in der Home-Assistant-Geräteübersicht. Das erfordert ggf. einen separaten Home-Assistant-Brands-Beitrag.
