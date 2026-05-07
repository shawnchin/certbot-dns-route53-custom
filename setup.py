import os

from setuptools import setup

version = "0.1.1"
upstream_version = "0.5.0"

install_requires = [
    'boto3>=1.20.34',
]

if os.environ.get('SNAP_BUILD'):
    install_requires.append('packaging')
else:
    install_requires.extend([
        f'acme>={upstream_version}',
        f'certbot>={upstream_version}',
    ])

# Load readme to use on PyPI
with open("README.md", encoding="utf8") as f:
    readme = f.read()

setup(
    name="certbot-dns-route53-custom",
    version=version,
    description="Route53 DNS Authenticator plugin for Certbot",
    url="https://github.com/shawnchin/certbot-dns-route53-custom",
    license='Apache',
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: POSIX :: Linux',
        'Environment :: Plugins',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=install_requires,
    entry_points={
        "certbot.plugins": [
            "dns-route53-custom = certbot_dns_route53_custom._internal.dns_route53_custom:Authenticator",
        ],
    },
)
