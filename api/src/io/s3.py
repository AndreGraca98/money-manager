from enum import Enum
from pathlib import Path
from tempfile import mkstemp
from typing import Self

from minio.api import Minio
from minio.datatypes import Object
from minio.error import InvalidResponseError, S3Error

from ..env import ENV


class MinioFileType(Enum):
    UNKNOWN = "application/octet-stream"
    PDF = "application/pdf"
    JPEG = JPG = "image/jpeg"

    def __str__(self):
        return self.value


class MinioBucket:
    """Wrapper around Minio client to store and retrieve files from a bucket."""

    def __init__(self, bucket_name: str):
        env = ENV()

        self._client = Minio(
            env.MINIO_ADDRESS,
            access_key=env.MINIO_ROOT_USER,
            secret_key=env.MINIO_ROOT_PASSWORD,
            region=env.MINIO_REGION,
            secure=env.MINIO_USE_HTTPS,
        )

        self._should_create_bucket: bool = env.MINIO_SHOULD_CREATE_BUCKET
        self._bucket_name: str = bucket_name
        self._local_tmp_filepath: list[Path] = []
        """List of files that have been downloaded to local fs."""

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def local_tmp_filepaths(self) -> list[Path]:
        return self._local_tmp_filepath

    def exists(self) -> bool:
        """Check if bucket exists."""
        return self._client.bucket_exists(self._bucket_name)

    def file_exists(self, object_name: str) -> bool:
        """Check if file exists in bucket."""
        try:
            self._client.stat_object(self._bucket_name, object_name)
            return True
        except (InvalidResponseError, S3Error):
            return False

    def list_files(self):
        """List files in the bucket."""
        objs = self._client.list_objects(self._bucket_name, recursive=True)

        def map_minio_obj(obj: Object) -> dict[str, str | int | None]:
            return dict(
                bucket_name=obj._bucket_name,
                object_name=obj._object_name,
                last_modified=(
                    obj._last_modified.isoformat() if obj._last_modified else None
                ),
                content_type=obj._content_type,
                size=obj._size,  # in bytes
            )

        return list(map(map_minio_obj, objs))

    def store_file(
        self,
        object_name: str,
        file_path: Path | str,
        file_type: MinioFileType = MinioFileType.UNKNOWN,
    ):
        """Store file in bucket."""
        self._validate_bucket()

        self._client.fput_object(
            self._bucket_name, object_name, str(file_path), file_type.value
        )

    def get_file(self, object_name: str) -> Path:
        """Download file from bucket to local fs."""
        try:
            _dir = Path("/tmp/downloaded")
            _dir.mkdir(parents=True, exist_ok=True)
            _, temp_file = mkstemp(dir=str(_dir), prefix="minio_", suffix=".tmp")
            temp_file = Path(temp_file).resolve()
            # temp_file.parent.mkdir(parents=True, exist_ok=True)
            temp_file.touch()
            self._client.fget_object(self._bucket_name, object_name, str(temp_file))
            self._local_tmp_filepath.append(temp_file)
            return temp_file
        except (InvalidResponseError, S3Error) as err:
            raise err

    def clean_up(self):
        """Remove all cached files."""
        for file in self._local_tmp_filepath:
            Path(file).unlink(missing_ok=True)

    def _validate_bucket(self):
        """Ensure bucket exists, create if necessary."""
        if self.exists():
            return
        if not self._should_create_bucket:
            raise ValueError(
                f"Bucket does not exist: {self._bucket_name} "
                "and 'MINIO_SHOULD_CREATE_BUCKET' is set to False."
            )
        self._client.make_bucket(self._bucket_name)


class MinioBucketDownloader:
    """Context manager to download multiple files from Minio.

    ```
    with BucketDownloader(
        bucket_name="my-bucket", object_names=["file1", "file2"]
    ) as downloader:
        files: dict[str, Path] = downloader.download()
        # files is a dict in format {object_name: file_path}
        file1: Path = files["file1"]
        file2: Path = files["file2"]
    ```
    """

    def __init__(self, bucket_name: str, object_names: list[str] | str):
        self._bucket = MinioBucket(bucket_name)
        _obj_names = [object_names] if isinstance(object_names, str) else object_names
        self._object_names: list[str] = _obj_names

    def __enter__(self) -> Self:
        return self

    def download(self) -> dict[str, Path]:
        """Download files from bucket to local fs. Return a dict of
        files in format `{object_name: file_path}`."""
        files: dict[str, Path] = dict()
        for object_name in self._object_names:
            files[object_name] = self._bucket.get_file(object_name)
        return files

    def __exit__(self, exc_type, exc_val, exc_tb): ...
