"""
로깅 설정 (JSON 포맷)
"""
import logging
import json
from datetime import datetime


def setup_logging(log_level: str = "INFO"):
    """
    구조화된 로깅 설정

    :param log_level: 로그 레벨
    """
    # TODO: JSON 포맷 로깅 설정
    pass


def get_logger(name: str) -> logging.Logger:
    """
    로거 인스턴스 반환

    :param name: 로거 이름
    :return: 로거 인스턴스
    """
    # TODO: 로거 반환
    return logging.getLogger(name)
