# sakuratox.is-a.dev

Личный сайт: один `index.html` без сборщика, 3D на three.js (частицы меняют форму при прокрутке).

Пасхалка: нажми на облако точек.

Резюме в `cv/` (EN и RU) собираются из `tools/make_cv.py`: `python tools/make_cv.py cv`.

## Хостинг

| Где | Как |
| --- | --- |
| **sakuratox.ru** (запасной вариант, не развёрнут) | Yandex Object Storage + Cloud DNS + сертификат Let's Encrypt из Certificate Manager. Инфраструктура в `deploy/main.tf`, загрузка через `.github/workflows/deploy-yc.yml`. Работает из России без сюрпризов. |
| **[sakuratox.is-a.dev](https://sakuratox.is-a.dev)** | GitHub Pages из ветки `main`, без сборки (`.nojekyll`). Домен выдан [is-a.dev](https://github.com/is-a-dev/register/blob/main/domains/sakuratox.json): CNAME на `sakuratix.github.io`, файл `CNAME` в корне, HTTPS от GitHub Pages. Старый адрес sakuratix.github.io редиректит сюда. |

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
