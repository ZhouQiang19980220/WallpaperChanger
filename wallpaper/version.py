# wallpaper/version.py

class VersionManager:
    def __init__(self):
        self.version = '0.0.1'

    def get_version(self) -> str:
        """获取软件版本号。"""
        return self.version
