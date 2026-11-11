# sakuratox.ru

Личный сайт: один `index.html` без сборщика, 3D на three.js (частицы меняют форму при прокрутке).

Пасхалка: нажми на облако точек.

Резюме в `cv/` (EN и RU) собираются из `tools/make_cv.py`: `python tools/make_cv.py cv`.

## Хостинг

| Где | Как |
| --- | --- |
| **sakuratox.ru** (основной) | Yandex Object Storage + Cloud DNS + сертификат Let's Encrypt из Certificate Manager. Инфраструктура в `deploy/main.tf`, загрузка через `.github/workflows/deploy-yc.yml`. Работает из России без сюрпризов. |
| **sakuratix.github.io** (зеркало) | GitHub Pages из ветки `main`, без сборки (`.nojekyll`). |

### Первый запуск

```bash
cd deploy
export YC_TOKEN=$(yc iam create-token)
terraform init
terraform apply -var cloud_id=<id> -var folder_id=<id>
terraform output -raw aws_secret_access_key
```

1. У регистратора домена указать NS: `ns1.yandexcloud.net`, `ns2.yandexcloud.net`.
2. В GitHub: Settings → Secrets: `YC_ACCESS_KEY_ID`, `YC_SECRET_ACCESS_KEY`; Variables: `YC_BUCKET=sakuratox.ru`.
3. Любой push в `main` выкатывает сайт.
