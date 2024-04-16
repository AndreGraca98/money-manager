from environs import Env


class ENV:
    def __init__(self):
        self._env = Env()
        self._env.read_env()

        self.MINIO_ADDRESS: str = self._env.str("MINIO_ADDRESS")
        self.MINIO_ROOT_USER: str = self._env.str("MINIO_ROOT_USER")
        self.MINIO_ROOT_PASSWORD: str = self._env.str("MINIO_ROOT_PASSWORD")
        self.MINIO_REGION: str = self._env.str("MINIO_REGION", "us-east-1")
        self.MINIO_USE_HTTPS: bool = self._env.bool("MINIO_USE_HTTPS", False)
        self.MINIO_SHOULD_CREATE_BUCKET: bool = self._env.bool(
            "MINIO_SHOULD_CREATE_BUCKET", True
        )
