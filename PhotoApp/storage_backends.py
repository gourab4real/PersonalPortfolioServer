# PhotoApp/storage_backends.py
from storages.backends.s3 import S3Storage
from botocore.config import Config
import urllib3

# Suppress insecure connection warnings in local terminal console
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CloudflareR2Storage(S3Storage):
    def _get_or_create_default_settings(self):
        settings = super()._get_or_create_default_settings()
        # Ensure verify is passed to the underlying boto3 client
        settings['verify'] = False
        return settings

    def _get_client_config(self):
        # Explicitly configure botocore client parameters
        return Config(
            s3={'addressing_style': 'path'},
            signature_version='s3v4'
        )

    @property
    def connection(self):
        conn = super().connection
        # Enforce verify=False on the HTTP session level
        conn.meta.client._endpoint.http_session.verify = False
        return conn