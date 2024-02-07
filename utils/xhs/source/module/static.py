from pathlib import Path

__all__ = [
    "VERSION_MAJOR",
    "VERSION_MINOR",
    "VERSION_BETA",
    "ROOT",
    "ERROR",
    "WARNING",
    "INFO",
    "USERSCRIPT",
    "USERAGENT",
    "HEADERS",
]

VERSION_MAJOR = 1
VERSION_MINOR = 8
VERSION_BETA = True
ROOT = Path(__file__).resolve().parent.parent.parent


USERSCRIPT = "https://raw.githubusercontent.com/JoeanAmier/XHS-Downloader/master/static/XHS-Downloader.js"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Dnt": "1",
    "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Microsoft Edge\";v=\"120\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}
USERAGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 "
    "Safari/537.36 Edg/121.0.0.0")

ERROR = "b bright_red"
WARNING = "b bright_yellow"
INFO = "b bright_green"
