#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/16 9:50
# @Author   : 冉勇
# @File     : tool_weather.py
# @Software : PyCharm
# @Desc     :
import os
import json
import httpx
import time
from utils.log_util import logger
from typing import Any
from dotenv import load_dotenv

# 获取当前环境，默认为 'dev'
ENV = os.getenv("ENV", "dev")

# 根据环境加载对应的环境变量文件
env_file = f".env.{ENV}"
print(f"Loading environment from {env_file}")
load_dotenv(env_file)


class WeatherTool:
    # OpenWeather API 配置

    OPENWEATHER_API_BASE = os.getenv("OPENWEATHER_API_BASE")
    API_KEY = os.getenv("API_KEY")  # 请替换为你自己的 OpenWeather API Key
    USER_AGENT = "weather-app/1.0"

    # 内存缓存，为每个城市存储 (数据, 时间戳)
    _cache = {}
    # 缓存有效期（秒）
    CACHE_TTL = 1800  # 30分钟

    @classmethod
    async def check_api_status(cls) -> bool:
        """
        检查 OpenWeather API 是否可用
        :return: API是否可用
        """
        try:
            # 使用一个知名城市做测试查询
            params = {
                "q": "London",
                "appid": cls.API_KEY,
                "units": "metric"
            }
            headers = {"User-Agent": cls.USER_AGENT}

            async with httpx.AsyncClient() as client:
                response = await client.get(
                    cls.OPENWEATHER_API_BASE,
                    params=params,
                    headers=headers,
                    timeout=5.0
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"API状态检查失败: {str(e)}")
            return False

    @classmethod
    async def fetch_weather(cls, city: str) -> dict[str, Any]:
        """
        从 OpenWeather API 获取天气信息，使用缓存优化
        :param city: 城市名称（需使用英文，如 Beijing）
        :return: 天气数据字典；若出错返回包含 error 信息的字典
        """
        # 检查缓存
        current_time = time.time()
        if city in cls._cache:
            data, timestamp = cls._cache[city]
            # 如果缓存有效（未过期）
            if current_time - timestamp < cls.CACHE_TTL:
                logger.info(f"使用缓存数据: {city}, 缓存时间: {int(current_time - timestamp)}秒")
                return data

        # 缓存不存在或已过期，从API获取
        try:
            data = await cls._fetch_from_api(city)
            # 更新缓存
            cls._cache[city] = (data, current_time)
            return data
        except Exception as e:
            logger.error(f"获取天气数据失败: {str(e)}")
            return {"error": f"请求失败: {str(e)}"}

    @classmethod
    async def _fetch_from_api(cls, city: str) -> dict[str, Any]:
        """
        从API直接获取天气数据
        :param city: 城市名称
        :return: 天气数据
        """
        params = {
            "q": city,
            "appid": cls.API_KEY,
            "units": "metric",
            "lang": "zh_cn"
        }
        headers = {"User-Agent": cls.USER_AGENT}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    cls.OPENWEATHER_API_BASE,
                    params=params,
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                error_msg = f"HTTP 错误: {e.response.status_code}"
                if e.response.status_code == 404:
                    error_msg = f"城市 '{city}' 未找到"
                elif e.response.status_code == 401:
                    error_msg = "API密钥无效"
                return {"error": error_msg}
            except httpx.RequestError as e:
                return {"error": f"网络请求错误: {str(e)}"}
            except Exception as e:
                return {"error": f"未知错误: {str(e)}"}

    @classmethod
    def format_weather(cls, data: dict[str, Any] | str) -> str:
        """
        将天气数据格式化为易读文本。
        :param data: 天气数据（可以是字典或 JSON 字符串）
        :return: 格式化后的天气信息字符串
        """
        # 如果传入的是字符串，则先转换为字典
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                return f"无法解析天气数据: {e}"

        # 如果数据中包含错误信息，直接返回错误提示
        if "error" in data:
            return f"⚠️ {data['error']}"

        # 提取数据时做容错处理
        city = data.get("name", "未知")
        country = data.get("sys", {}).get("country", "未知")
        temp = data.get("main", {}).get("temp", "N/A")
        feels_like = data.get("main", {}).get("feels_like", "N/A")
        humidity = data.get("main", {}).get("humidity", "N/A")
        pressure = data.get("main", {}).get("pressure", "N/A")
        wind_speed = data.get("wind", {}).get("speed", "N/A")
        wind_direction = data.get("wind", {}).get("deg", "N/A")
        # weather 可能为空列表，因此用 [0] 前先提供默认字典
        weather_list = data.get("weather", [{}])
        description = weather_list[0].get("description", "未知") if weather_list else "未知"
        icon = weather_list[0].get("icon", "") if weather_list else ""

        # 构建更详细的天气信息
        return (
            f"🌍 {city}, {country}\n"
            f"🌡 温度: {temp}°C (体感温度: {feels_like}°C)\n"
            f"💧 湿度: {humidity}%\n"
            f"🌬 风速: {wind_speed} m/s ({cls._get_wind_direction(wind_direction)})\n"
            f"🌤 天气: {description}\n"
            f"🔄 数据刷新时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

    @staticmethod
    def _get_wind_direction(degrees):
        """根据角度获取风向描述"""
        if degrees is None or degrees == "N/A":
            return "未知"

        directions = [
            "北风", "东北风", "东风", "东南风",
            "南风", "西南风", "西风", "西北风"
        ]
        index = round(((degrees % 360) / 45)) % 8
        return directions[index]

    @classmethod
    def clear_cache(cls):
        """清除所有缓存数据"""
        cls._cache.clear()

    @classmethod
    def get_cache_stats(cls):
        """获取缓存统计信息"""
        return {
            "cache_size": len(cls._cache),
            "cached_cities": list(cls._cache.keys())
        }
