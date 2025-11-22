"""
날짜 파싱 유틸리티
"""
from datetime import datetime


class DateUtils:
    """
    날짜 유틸리티 클래스
    """

    @staticmethod
    def parse_date(date_string: str, format: str = "%Y-%m-%d") -> datetime:
        """
        문자열을 datetime으로 파싱

        :param date_string: 날짜 문자열
        :param format: 날짜 포맷
        :return: datetime 객체
        """
        # TODO: 날짜 파싱 로직
        return datetime.now()

    @staticmethod
    def format_date(date: datetime, format: str = "%Y-%m-%d") -> str:
        """
        datetime을 문자열로 포맷

        :param date: datetime 객체
        :param format: 날짜 포맷
        :return: 포맷된 문자열
        """
        # TODO: 날짜 포맷팅 로직
        return ""

    @staticmethod
    def get_relative_time(date: datetime) -> str:
        """
        상대 시간 표현

        :param date: datetime 객체
        :return: 상대 시간 문자열 (예: "2시간 전")
        """
        # TODO: 상대 시간 계산
        return ""
