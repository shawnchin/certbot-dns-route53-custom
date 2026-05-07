# certbot-dns-route53-custom

This is a custom version of the official [certbot-dns-route53](https://github.com/certbot/certbot/tree/main/certbot-dns-route53) 
plugin, with the addition of the `--dns-route53-custom-zone-id` option to explicitly specify the Hosted Zone to use.

## Installation

⚠️ For now, this only works with pip-installed certbot. 

```bash
# install the plugin
pip install certbot-dns-route53-custom

# check that certbot sees the plugin
certbot plugins
```
## Example
```
certbot certonly \
  --authenticator dns-route53-custom \
  --dns-route53-custom-zone-id YOUR_HOSTED_ZONE_ID \
  -d example.com
```

## Why this plugin?

The original version performs a `list_hosted_zones` to discover all Hosted Zones in your AWS account and selects the one
that matches the target domain. This means the plugin requires `route53:ListHostedZones` permissions which can't be 
restricted to a specific subdomain/hosted zone.

By specifying an explicit zone id, we skip the `list_hosted_zones` call and instead calls `get_hosted_zone` to verify 
that the provided Hosted Zone ID is valid and compatible with the target domain.

This allows for a more restrictive set of permissions compared to the [official version](https://certbot-dns-route53.readthedocs.io/en/stable/#sample-aws-policy-json).

Example IAM policy that limits `GetHostedZone` and `ChangeResourceRecordSets` to just a specific Hosted Zone and set of 
records.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "route53:GetChange",
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": "route53:GetHostedZone",
            "Resource": "arn:aws:route53:::hostedzone/YOURHOSTEDZONEID"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/YOURHOSTEDZONEID",
            "Condition": {
                "ForAllValues:StringEquals": {
                    "route53:ChangeResourceRecordSetsNormalizedRecordNames": [
                        "_acme-challenge.example.com",
                        "_acme-challenge.subdomain.domain.com"
                    ]
                }
            }
        }
    ]
}
```