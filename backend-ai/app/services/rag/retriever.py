"""
문서 검색 (RAG)
"""


class Retriever:
    """
    문서 검색 서비스
    """

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        관련 문서 검색

        :param query: 쿼리
        :param top_k: 상위 K개 검색
        :return: 검색된 문서 리스트
        """
        # TODO: 문서 검색 로직
        return []
