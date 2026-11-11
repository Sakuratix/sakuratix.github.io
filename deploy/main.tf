# Static hosting for sakuratox.ru in Yandex Object Storage:
# bucket website + Yandex Cloud DNS + Let's Encrypt certificate from Certificate Manager.
#
#   export YC_TOKEN=$(yc iam create-token)
#   terraform init && terraform apply -var cloud_id=... -var folder_id=...
# Then point the domain's NS records at ns1.yandexcloud.net and ns2.yandexcloud.net at your registrar.

terraform {
  required_version = ">= 1.6"
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.130"
    }
  }
}

provider "yandex" {
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
}

variable "cloud_id" { type = string }
variable "folder_id" { type = string }

variable "domain" {
  type    = string
  default = "sakuratox.ru"
}

# ---------- service account for the bucket and for CI uploads ----------
resource "yandex_iam_service_account" "site" {
  name = "site-deployer"
}

resource "yandex_resourcemanager_folder_iam_member" "storage" {
  folder_id = var.folder_id
  role      = "storage.editor"
  member    = "serviceAccount:${yandex_iam_service_account.site.id}"
}

resource "yandex_iam_service_account_static_access_key" "site" {
  service_account_id = yandex_iam_service_account.site.id
  description        = "terraform + github actions upload"
}

# ---------- DNS ----------
resource "yandex_dns_zone" "site" {
  name   = replace(var.domain, ".", "-")
  zone   = "${var.domain}."
  public = true
}

# ---------- certificate ----------
resource "yandex_cm_certificate" "site" {
  name    = replace(var.domain, ".", "-")
  domains = [var.domain, "www.${var.domain}"]
  managed {
    challenge_type  = "DNS_CNAME"
    challenge_count = 2
  }
}

resource "yandex_dns_recordset" "acme" {
  count   = 2
  zone_id = yandex_dns_zone.site.id
  name    = yandex_cm_certificate.site.challenges[count.index].dns_name
  type    = yandex_cm_certificate.site.challenges[count.index].dns_type
  data    = [yandex_cm_certificate.site.challenges[count.index].dns_value]
  ttl     = 60
}

data "yandex_cm_certificate" "site" {
  depends_on      = [yandex_dns_recordset.acme]
  certificate_id  = yandex_cm_certificate.site.id
  wait_validation = true
}

# ---------- bucket ----------
resource "yandex_storage_bucket" "site" {
  bucket     = var.domain # must match the domain for website hosting
  access_key = yandex_iam_service_account_static_access_key.site.access_key
  secret_key = yandex_iam_service_account_static_access_key.site.secret_key

  anonymous_access_flags {
    read = true
    list = false
  }

  website {
    index_document = "index.html"
    error_document = "index.html"
  }

  https {
    certificate_id = data.yandex_cm_certificate.site.id
  }

  depends_on = [yandex_resourcemanager_folder_iam_member.storage]
}

resource "yandex_storage_bucket" "www" {
  bucket     = "www.${var.domain}"
  access_key = yandex_iam_service_account_static_access_key.site.access_key
  secret_key = yandex_iam_service_account_static_access_key.site.secret_key

  website {
    redirect_all_requests_to = "https://${var.domain}"
  }

  https {
    certificate_id = data.yandex_cm_certificate.site.id
  }
}

resource "yandex_dns_recordset" "apex" {
  zone_id = yandex_dns_zone.site.id
  name    = "${var.domain}."
  type    = "ANAME"
  ttl     = 600
  data    = ["${var.domain}.website.yandexcloud.net"]
}

resource "yandex_dns_recordset" "www" {
  zone_id = yandex_dns_zone.site.id
  name    = "www.${var.domain}."
  type    = "CNAME"
  ttl     = 600
  data    = ["www.${var.domain}.website.yandexcloud.net"]
}

# ---------- outputs for GitHub secrets ----------
output "aws_access_key_id" {
  value = yandex_iam_service_account_static_access_key.site.access_key
}

output "aws_secret_access_key" {
  value     = yandex_iam_service_account_static_access_key.site.secret_key
  sensitive = true
}

output "name_servers" {
  value = ["ns1.yandexcloud.net", "ns2.yandexcloud.net"]
}
