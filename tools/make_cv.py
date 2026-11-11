"""Render the EN and RU CV as one-page A4 PDFs with headless Chromium."""
import html
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

CV = {
    "en": {
        "file": "klimentiy-matveev-devops-en.pdf",
        "name": "Klimentiy Matveev",
        "role": "DevOps Engineer",
        "meta": "Moscow, Russia · remote only · English C1",
        "summary": (
            "DevOps engineer with 4 years in infrastructure, 2 of them on DevOps projects: from CI/CD, Kubernetes, "
            "Terraform and Prometheus to Linux servers, MikroTik networks and Zabbix. I build pipelines that "
            "scan and ship images without manual steps, move services to Kubernetes without downtime and keep "
            "infrastructure in code. Certified Kubernetes Administrator (CKA), Terraform Associate, MTCNA."
        ),
        "h": {"skills": "Skills", "exp": "Experience", "proj": "Open-source projects", "edu": "Certifications and education"},
        "skills": [
            ("Containers", "Kubernetes (CKA), Docker, Helm, Argo CD, k3s, Ingress-NGINX, cert-manager"),
            ("Delivery and IaC", "GitLab CI, GitHub Actions, Terraform (Associate), Ansible, Trivy, Vault, SOPS"),
            ("Observability", "Prometheus, Grafana, Alertmanager, Loki, Zabbix"),
            ("Systems and data", "Linux, systemd, Nginx, MikroTik (MTCNA), VPN (WireGuard, OpenVPN, IPsec), PostgreSQL, Redis, Kafka, TrueNAS/ZFS"),
            ("Cloud and code", "Yandex Cloud, Selectel, Proxmox, Bash, Python, Git"),
        ],
        "jobs": [
            ("Infrastructure Engineer", "LANGAME SOFTWARE · Moscow", "Oct 2024 - present", [
                "Linux servers and TrueNAS storage (ZFS snapshots, replication) across client gaming venues",
                "MikroTik networks: VLAN, firewall, site-to-site VPN; troubleshooting loss and latency",
                "Zabbix templates, triggers and dashboards; Bash automation for checks and diagnostics",
                "Incident root-cause analysis and knowledge-base write-ups so issues do not repeat",
            ]),
            ("DevOps Engineer", "Nixys, DevOps outsourcing · contract · remote", "2022 - 2024", [
                "GitLab CI pipelines: build, tests, image scanning with Trivy, promotion across dev, stage and prod",
                "Moved services from docker-compose to Kubernetes: Helm charts, Ingress-NGINX, cert-manager, HPA, probes",
                "Yandex Cloud infrastructure in Terraform: VPC, Managed Kubernetes, Managed PostgreSQL, remote state",
                "Server baseline with Ansible; monitoring with kube-prometheus-stack and Loki, alerts to Telegram",
            ]),
            ("Back-office Specialist, Anti-fraud", "T-Bank · Moscow", "2020 - 2021", [
                "Incident investigation: rebuilding event chains from transactions and system logs",
                "SLA-driven work under strict procedures; documentation accepted by partner teams without rework",
            ]),
        ],
        "projects": [
            ("infra-lab", "service to production: Docker, Helm, Terraform, Ansible, CI with Trivy, Prometheus"),
            ("k3s-gitops", "single-node k3s managed by Argo CD (app of apps), manifests validated with kubeconform"),
            ("alertmanager-telegram-relay", "dependency-free Alertmanager to Telegram webhook, tested, non-root image"),
            ("pg-backup-s3", "PostgreSQL backups to S3 with retention, systemd timer, Prometheus metrics"),
            ("mikrotik-config-backup", "nightly MikroTik config export into git with per-router history"),
        ],
        "edu": [
            ("CKA, Certified Kubernetes Administrator", "Linux Foundation, 2026"),
            ("HashiCorp Certified: Terraform Associate", "2026"),
            ("MTCNA, MikroTik Certified Network Associate", "Softline, 2026"),
            ("Bachelor's in Applied Informatics, System Administration", "RANEPA, Moscow, 2023"),
            ("Internships during studies", "SberTech, Alfa-Bank"),
            ("English C1", "Skillfactory courses and private tutoring"),
        ],
    },
    "ru": {
        "file": "klimentiy-matveev-devops-ru.pdf",
        "name": "Климентий Матвеев",
        "role": "DevOps-инженер",
        "meta": "Москва · только удалённо · английский C1",
        "summary": (
            "DevOps-инженер: 4 года в инфраструктуре, из них 2 года на DevOps-проектах. От CI/CD, Kubernetes, "
            "Terraform и Prometheus до Linux-серверов, сетей MikroTik и Zabbix. Строю пайплайны, которые проверяют и "
            "выкатывают образы без ручных шагов, переношу сервисы в Kubernetes без простоя и описываю "
            "инфраструктуру кодом. Сертификаты CKA, Terraform Associate, MTCNA."
        ),
        "h": {"skills": "Навыки", "exp": "Опыт работы", "proj": "Открытые проекты", "edu": "Сертификаты и образование"},
        "skills": [
            ("Контейнеры", "Kubernetes (CKA), Docker, Helm, Argo CD, k3s, Ingress-NGINX, cert-manager"),
            ("Доставка и IaC", "GitLab CI, GitHub Actions, Terraform (Associate), Ansible, Trivy, Vault, SOPS"),
            ("Мониторинг", "Prometheus, Grafana, Alertmanager, Loki, Zabbix"),
            ("Системы и данные", "Linux, systemd, Nginx, MikroTik (MTCNA), VPN (WireGuard, OpenVPN, IPsec), PostgreSQL, Redis, Kafka, TrueNAS/ZFS"),
            ("Облака и код", "Yandex Cloud, Selectel, Proxmox, Bash, Python, Git"),
        ],
        "jobs": [
            ("Инженер инфраструктуры", "LANGAME SOFTWARE · Москва", "окт. 2024 - н.в.", [
                "Linux-серверы и хранилища TrueNAS (снапшоты ZFS, репликация) на площадках компьютерных клубов",
                "Сети MikroTik: VLAN, firewall, VPN между площадками; диагностика потерь и задержек",
                "Шаблоны, триггеры и дашборды Zabbix; автоматизация проверок и диагностики на Bash",
                "Разбор инцидентов с поиском первопричины и статьями в базу знаний, чтобы проблемы не повторялись",
            ]),
            ("DevOps-инженер", "Nixys, DevOps-аутсорсинг · контракт · удалённо", "2022 - 2024", [
                "CI/CD в GitLab CI: сборка, тесты, сканирование образов Trivy, деплой по окружениям dev, stage, prod",
                "Перевёл сервисы с docker-compose в Kubernetes: Helm-чарты, Ingress-NGINX, cert-manager, HPA, пробы",
                "Инфраструктура Yandex Cloud на Terraform: VPC, Managed Kubernetes, Managed PostgreSQL, remote state",
                "Базовая настройка серверов через Ansible; мониторинг kube-prometheus-stack и Loki, алерты в Telegram",
            ]),
            ("Специалист бэк-офиса, антифрод", "Т-Банк · Москва", "2020 - 2021", [
                "Разбор инцидентов: восстановление цепочки событий по операциям и логам систем",
                "Работа по SLA и строгим регламентам; документация, которую смежные команды принимали без доработок",
            ]),
        ],
        "projects": [
            ("infra-lab", "сервис от кода до прода: Docker, Helm, Terraform, Ansible, CI с Trivy, Prometheus"),
            ("k3s-gitops", "однонодовый k3s под управлением Argo CD (app of apps), проверка манифестов kubeconform"),
            ("alertmanager-telegram-relay", "webhook Alertmanager в Telegram без зависимостей, тесты, образ без root"),
            ("pg-backup-s3", "бэкапы PostgreSQL в S3 с ротацией, systemd-таймером и метриками Prometheus"),
            ("mikrotik-config-backup", "ночной экспорт конфигов MikroTik в git с историей по каждому роутеру"),
        ],
        "edu": [
            ("CKA, Certified Kubernetes Administrator", "Linux Foundation, 2026"),
            ("HashiCorp Certified: Terraform Associate", "2026"),
            ("MTCNA, MikroTik Certified Network Associate", "Softline, 2026"),
            ("Бакалавр, прикладная информатика, «Системное администрирование»", "РАНХиГС, Москва, 2023"),
            ("Практика и стажировки во время учёбы", "СберТех, Альфа-Банк"),
            ("Английский C1", "курсы Skillfactory и занятия с репетитором"),
        ],
    },
}

CSS = """
@page{size:A4;margin:14mm 15mm}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,'DejaVu Sans',sans-serif;font-size:9.4pt;line-height:1.42;color:#1d2228}
.mono{font-family:'DejaVu Sans Mono',monospace}
header{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.5pt solid #1d2228;padding-bottom:8pt}
h1{font-size:21pt;letter-spacing:-.02em;font-weight:700;line-height:1.05}
.role{font-size:11.5pt;color:#127a5a;font-weight:600;margin-top:3pt}
.contacts{text-align:right;font-size:8.4pt;color:#3c444e;line-height:1.55}
.contacts a{color:#1d2228;text-decoration:none}
.meta{font-size:8.6pt;color:#5b636e;margin-top:3pt}
h2{font-size:8.6pt;text-transform:uppercase;letter-spacing:.12em;color:#127a5a;margin:12pt 0 5pt;font-weight:700}
p.sum{color:#2b323a}
table.sk{border-collapse:collapse;width:100%}
table.sk td{padding:1.6pt 0;vertical-align:top}
table.sk td:first-child{width:28%;color:#5b636e;font-weight:600}
.job{margin-bottom:7pt}
.jh{display:flex;justify-content:space-between;align-items:baseline}
.jh b{font-size:10pt}
.jh span{font-size:8.4pt;color:#5b636e;white-space:nowrap}
.where{font-size:8.6pt;color:#5b636e;margin-bottom:2pt}
ul{padding-left:11pt}
li{margin:1pt 0}
.earlier{font-size:8.5pt;color:#5b636e}
.pr{display:flex;gap:6pt;margin:1.6pt 0}
.pr b{white-space:nowrap}
.pr a{color:#1d2228;text-decoration:none;font-weight:600}
.edu div{display:flex;justify-content:space-between;gap:10pt;margin:1.6pt 0}
.edu span{color:#5b636e;white-space:nowrap}
"""


def render(d: dict) -> str:
    e = html.escape
    skills = "".join(f"<tr><td>{e(k)}</td><td>{e(v)}</td></tr>" for k, v in d["skills"])
    jobs = "".join(
        f'<div class="job"><div class="jh"><b>{e(t)}</b><span>{e(when)}</span></div>'
        f'<div class="where">{e(where)}</div><ul>{"".join(f"<li>{e(x)}</li>" for x in items)}</ul></div>'
        for t, where, when, items in d["jobs"]
    )
    projects = "".join(
        f'<div class="pr"><a class="mono" href="https://github.com/Sakuratix/{e(n)}">{e(n)}</a><span>{e(desc)}</span></div>'
        for n, desc in d["projects"]
    )
    edu = "".join(f"<div><b>{e(a)}</b><span>{e(b)}</span></div>" for a, b in d["edu"])
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<header>
  <div><h1>{e(d['name'])}</h1><div class="role">{e(d['role'])}</div><div class="meta">{e(d['meta'])}</div></div>
  <div class="contacts mono">
    <a href="mailto:sakuratoxs@gmail.com">sakuratoxs@gmail.com</a><br>
    <a href="https://t.me/MountewDew">t.me/MountewDew</a><br>
    <a href="https://github.com/Sakuratix">github.com/Sakuratix</a><br>
    <a href="https://www.linkedin.com/in/klimentii-matveev-59ab38426/">in/klimentii-matveev</a><br>
    <a href="https://sakuratix.github.io">sakuratix.github.io</a>
  </div>
</header>
<p class="sum" style="margin-top:10pt">{e(d['summary'])}</p>
<h2>{e(d['h']['skills'])}</h2><table class="sk">{skills}</table>
<h2>{e(d['h']['exp'])}</h2>{jobs}
<h2>{e(d['h']['proj'])}</h2>{projects}
<h2>{e(d['h']['edu'])}</h2><div class="edu">{edu}</div>
</body></html>"""


OUT.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")
    page = browser.new_page()
    for lang, d in CV.items():
        page.set_content(render(d), wait_until="load")
        pages = page.evaluate("Math.ceil(document.body.scrollHeight / (297/25.4*96 - 2*14/25.4*96))")
        page.pdf(path=str(OUT / d["file"]), format="A4", print_background=True,
                 margin={"top": "14mm", "bottom": "14mm", "left": "15mm", "right": "15mm"})
        print(lang, "estimated pages:", pages)
    browser.close()
