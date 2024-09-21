# setup.py

from setuptools import setup

APP = ["main.py"]  # 主程序入口文件
DATA_FILES = []  # 需要包含的其他数据文件
OPTIONS = {
    "includes": ["ctypes", "libffi"],
    "frameworks": [
        "/usr/local/Cellar/libffi/3.4.6/lib/libffi.dylib"
    ],  # 指定 libffi 的路径
    "argv_emulation": True,
    "iconfile": "MyIcon.iconset/icon.icns",  # 指定你的图标文件
    "plist": {
        "CFBundleName": "WallpaperChanger",  # 软件名称
        "CFBundleShortVersionString": "0.0.1",  # 软件版本
        "CFBundleVersion": "0.0.1",
        "CFBundleIdentifier": "WallpaperChanger.qjszm.top",  # 唯一标识符
    },
    "packages": ["wallpaper"],  # 需要包含的包
}

setup(
    app=APP,
    name="WallpaperChanger",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
