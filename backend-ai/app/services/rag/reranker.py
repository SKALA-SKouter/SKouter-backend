"""
검색 결과 재정렬
"""


class Reranker:
    """
    검색 결과 재정렬 서비스
    """

    def rerank(self, query: str, documents: list, top_k: int = 5) -> list:
        """
        검색 결과 재정렬

        :param query: 쿼리
        :param documents: 문서 리스트
        :param top_k: 상위 K개
        :return: 재정렬된 문서 리스트
        """
        # TODO: 재정렬 로직
        return documents[:top_k]
