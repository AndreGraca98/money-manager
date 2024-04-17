from enum import Enum
from pathlib import Path
from tempfile import mkstemp
from typing import Self

from minio.api import Minio
from minio.datatypes import Object
from minio.error import InvalidResponseError

from ..env import ENV


class MinioStoreFileType(Enum):
    UNKNOWN = "application/octet-stream"
    PDF = "application/pdf"
    CSV = "application/csv"
    JSON = "application/json"

    def __str__(self):
        return self.value


class MinioStore:
    """Wrapper around Minio client to store and retrieve files."""

    def __init__(self, bucket_name: str):
        env = ENV()
        address = env.MINIO_ADDRESS
        access_key = env.MINIO_ROOT_USER
        secret_key = env.MINIO_ROOT_PASSWORD
        region = env.MINIO_REGION
        use_https = env.MINIO_USE_HTTPS

        self.client = Minio(
            address,
            access_key=access_key,
            secret_key=secret_key,
            region=region,
            secure=use_https,
        )

        self.should_create_bucket: bool = env.MINIO_SHOULD_CREATE_BUCKET
        self.bucket_name: str = bucket_name
        self.cached_docs: list[Path] = []
        """List of files that have been downloaded to local fs."""

    def list_files(self):
        """List all files in bucket."""
        self._validate_bucket()
        objs = self.client.list_objects(self.bucket_name)

        def map_obj(obj: Object) -> dict:
            return dict(
                bucket_name=obj._bucket_name,
                object_name=obj._object_name,
                last_modified=(
                    obj._last_modified.isoformat() if obj._last_modified else None
                ),
                content_type=obj._content_type,
                size=obj._size,
            )

        return list(map(map_obj, objs))

    def store_file(
        self,
        object_name: str,
        file_path: Path | str,
        file_type: MinioStoreFileType = MinioStoreFileType.UNKNOWN,
    ):
        """Store file in bucket."""
        self._validate_bucket()

        self.client.fput_object(
            self.bucket_name, object_name, str(file_path), file_type.value
        )

    def get_file(self, object_name: str) -> Path:
        """Download file from bucket to local fs."""
        try:
            _, temp_file = mkstemp()
            temp_file = Path(temp_file).resolve()
            self.cached_docs.append(temp_file)
            self.client.fget_object(self.bucket_name, object_name, str(temp_file))
            return temp_file
        except InvalidResponseError as err:
            raise err

    def clean_up(self):
        """Remove all cached files."""
        for file in self.cached_docs:
            Path(file).unlink(missing_ok=True)

    def _validate_bucket(self):
        """Ensure bucket exists, create if necessary."""
        if self.client.bucket_exists(self.bucket_name):
            return
        if not self.should_create_bucket:
            raise ValueError(f"Bucket does not exist: {self.bucket_name}")
        self.client.make_bucket(self.bucket_name)
