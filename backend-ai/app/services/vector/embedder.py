"""
임베딩 생성 (OpenAI, HuggingFace)
"""


class Embedder:
    """
    텍스트 임베딩 서비스
    """

    def __init__(self, model: str = "openai"):
        """
        임베더 초기화

        :param model: 사용할 모델 (openai, huggingface)
        """
        # TODO: 모델 초기화
        self.model = model

    def embed(self, text: str) -> list:
        """
        텍스트 임베딩

        :param text: 텍스트
        :return: 임베딩 벡터
        """
        # TODO: 텍스트 임베딩
        return []
