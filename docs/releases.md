# Releases

Релизы выпускаются автоматически при пуше в `main` через [semantic-release](https://semantic-release.gitbook.io/).  
Версия определяется из коммитов по формату [Conventional Commits](https://www.conventionalcommits.org/).  
Тег — `v1.0.0`, черновик релиза — `echo_ > v1.0.0`.

---

## Conventional Commits

Echo использует сокращённый набор типов коммитов.

| Тип        | Версия  | Назначение                                      | Пример                                  |
|------------|---------|-------------------------------------------------|-----------------------------------------|
| `feat`     | Minor   | Новая пользовательская возможность              | `feat(tags): add tag pages`             |
| `fix`      | Patch   | Исправление ошибки                              | `fix(terminal): preserve input on blur` |
| `feat!`    | Major   | Ломающее изменение                              | `feat!: redesign command parser`        |
| `fix!`     | Major   | Ломающее исправление                            | `fix!: remove legacy slug format`       |
| `refactor` | —       | Внутренняя реализация без изменения поведения   | `refactor(orm): extract base query`     |
| `docs`     | —       | Документация, README, release notes             | `docs(readme): update setup guide`      |
| `test`     | —       | Тесты                                           | `test(tags): add tag page tests`        |
| `ci`       | —       | CI/CD, Actions, Poetry, pre-commit, зависимости | `ci(release): add semantic release`     |

---

## Scope

По возможности указывать область изменений:

```
feat(tags): add tag autocomplete
fix(terminal): fix mobile input focus
refactor(orm): split milestone and tag models
docs(architecture): update structure section
ci(release): pin semantic-release version
```

---

## Правила

- Только `feat` и `fix` повышают версию.
- `!` означает breaking change → увеличивает major.
- Остальные типы формируют читаемую историю, но не создают релиз.
- Если в одном PR несколько коммитов — версия определяется по наиболее значимому.
