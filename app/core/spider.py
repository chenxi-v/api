"""
Spider 基类定义
所有爬虫必须实现此接口
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import httpx


class Spider(ABC):
    """爬虫基类，所有爬虫必须实现此接口"""

    site_key: str = ""
    """站点唯一标识"""

    def __init__(self):
        """初始化爬虫"""
        self.site_key = ""
        self._client = httpx.Client(timeout=30.0)

    def fetch(self, url: str, **kwargs):
        """
        发送HTTP请求

        Args:
            url: 请求URL
            **kwargs: httpx请求参数

        Returns:
            httpx.Response对象
        """
        return self._client.get(url, **kwargs) if kwargs.get('params') or kwargs.get('headers') else self._client.get(url, **kwargs)

    def _parse_response_data(self, data):
        """
        解析响应数据，处理字符串形式的JSON

        Args:
            data: 响应数据

        Returns:
            解析后的数据
        """
        if isinstance(data, str):
            try:
                import json
                return json.loads(data)
            except:
                return data
        return data

    def init(self, extend: str = "") -> None:
        """
        初始化爬虫

        Args:
            extend: 扩展配置参数
        """
        pass

    @abstractmethod
    def home_content(self, filter: bool = False) -> Dict[str, Any]:
        """
        获取首页内容

        Args:
            filter: 是否启用过滤

        Returns:
            {
                "class": [{"type_id": 1, "type_name": "电影"}],
                "list": [{"vod_id": 1, "vod_name": "视频名"}]
            }
        """
        pass

    @abstractmethod
    def category_content(self, tid: str, pg: str = "1", filter: bool = False, extend: Dict = {}) -> Dict[str, Any]:
        """
        获取分类内容

        Args:
            tid: 分类ID
            pg: 页码
            filter: 是否启用过滤
            extend: 扩展参数

        Returns:
            {
                "page": 1,
                "pagecount": 10,
                "limit": 20,
                "total": 200,
                "list": [...]
            }
        """
        pass

    @abstractmethod
    def detail_content(self, ids: List[str]) -> Dict[str, Any]:
        """
        获取视频详情

        Args:
            ids: 视频ID列表

        Returns:
            {
                "vod_id": 1,
                "vod_name": "视频名",
                "vod_pic": "封面URL",
                "vod_play_from": "播放源",
                "vod_play_url": [{"name": "线路1", "url": ["url1", "url2"]}]
            }
        """
        pass

    @abstractmethod
    def search_content(self, key: str, quick: bool = False) -> Dict[str, Any]:
        """
        搜索内容

        Args:
            key: 搜索关键词
            quick: 是否快速搜索

        Returns:
            {
                "list": [...],
                "page": 1,
                "pagecount": 1
            }
        """
        pass

    @abstractmethod
    def player_content(self, flag: str, id: str, vip_flags: List[str] = None) -> Dict[str, Any]:
        """
        获取播放地址

        Args:
            flag: 播放标识
            id: 视频ID
            vip_flags: VIP标识列表

        Returns:
            {
                "parse": 0,
                "url": "播放地址",
                "header": {"User-Agent": "..."},
                "jx": "解析接口"
            }
        """
        pass

    def proxy(self, params: Dict[str, str]) -> Optional[List[Any]]:
        """
        代理接口

        Args:
            params: 代理参数

        Returns:
            [result1, result2, ...] 或 None
        """
        return None

    def destroy(self) -> None:
        """销毁爬虫，释放资源"""
        if hasattr(self, '_client'):
            self._client.close()
