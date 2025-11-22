"""
텍스트 전처리
"""


class TextProcessor:
    """
    텍스트 전처리 서비스
    """

    @staticmethod
    def clean_text(text: str) -> str:
        """
        텍스트 정제

        :param text: 원본 텍스트
        :return: 정제된 텍스트
        """
        # TODO: 정제 로직 (특수문자 제거, 공백 정규화 등)
        return text

    @staticmethod
    def tokenize(text: str) -> list:
        """
        텍스트 토큰화

        :param text: 텍스트
        :return: 토큰 리스트
        """
        # TODO: 토큰화 로직
        return []

    @staticmethod
    def remove_stopwords(tokens: list) -> list:
        """
        불용어 제거

        :param tokens: 토큰 리스트
        :return: 불용어 제거된 토큰 리스트
        """
        # TODO: 불용어 제거 로직
        return tokens
