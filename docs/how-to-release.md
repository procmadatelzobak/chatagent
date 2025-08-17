# Jak vydat verzi

Tento projekt používá [release-please](https://github.com/googleapis/release-please) pro spravování verzí a changelogu.

## Postup

1. Slouč požadované změny do branch `main` s konvenčními commit message.
2. Workflow `Release` na GitHubu spustí release-please a otevře *release PR* s navrhovaným zvýšením verze a úpravou `CHANGELOG.md`.
3. Zkontroluj a mergni release PR.
4. Po mergnutí se automaticky vytvoří tag a GitHub Release. Workflow navíc sestaví Python balíček (bez publikace).
5. Soubor `dist/` obsahuje sestavené artefakty. Publikaci na PyPI lze zapnout později doplněním kroku.

## První vydání

Pro ověření lze workflow spustit ručně přes `Run workflow` (dry run). Release-please vygeneruje návrh PR bez publikace.
