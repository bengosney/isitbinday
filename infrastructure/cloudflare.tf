resource "cloudflare_record" "cname_dkim" {
  count = 3

  zone_id         = var.zoneid
  name            = "${aws_sesv2_email_identity.email.dkim_signing_attributes[0].tokens[count.index]}._domainkey.${var.domain}"
  content         = "${aws_sesv2_email_identity.email.dkim_signing_attributes[0].tokens[count.index]}.dkim.amazonses.com"
  type            = "CNAME"
  proxied         = false
  comment         = "DKIM ${count.index} - SES"
  depends_on      = [aws_sesv2_email_identity.email]
  allow_overwrite = true
}

resource "cloudflare_record" "api" {
  name            = "api"
  proxied         = true
  type            = "CNAME"
  content         = var.hosting_domain
  zone_id         = var.zoneid
  allow_overwrite = true
}
