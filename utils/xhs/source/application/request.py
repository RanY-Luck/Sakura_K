from aiohttp import ClientError

from utils.xhs.source.module import ERROR
from utils.xhs.source.module import Manager
from utils.xhs.source.module import logging
from utils.xhs.source.module import retry

__all__ = ["Html"]


class Html:
    def __init__(self, manager: Manager, ):
        self.proxy = manager.proxy
        self.retry = manager.retry
        self.prompt = manager.prompt
        self.session = manager.request_session

    @retry
    async def request_url(
            self,
            url: str,
            content=True,
            log=None,
            **kwargs,
    ) -> str:
        try:
            async with self.session.get(
                    url,
                    proxy=self.proxy,
                    **kwargs,
            ) as response:
                if response.status != 200:
                    return ""
                return await response.text() if content else str(response.url)
        except ClientError as error:
            logging(log, str(error), ERROR)
            logging(log, self.prompt.request_error(url), ERROR)
            return ""

    @staticmethod
    def format_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")
