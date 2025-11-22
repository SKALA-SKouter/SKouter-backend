"""
Qdrant 클라이언트
"""


class QdrantClient:
    """
    Qdrant 벡터 DB 클라이언트
    """

    def __init__(self, url: str):
        """
        Qdrant 클라이언트 초기화

        :param url: Qdrant URL
        """
        # TODO: Qdrant 클라이언트 초기화
        self.url = url

    def create_collection(self, name: str, size: int) -> bool:
        """
        컬렉션 생성

        :param name: 컬렉션 이름
        :param size: 벡터 크기
        :return: 생성 성공 여부
        """
        # TODO: 컬렉션 생성
        pass

    def insert(self, collection: str, vector: list, metadata: dict) -> str:
        """
        벡터 삽입

        :param collection: 컬렉션 이름
        :param vector: 벡터
        :param metadata: 메타데이터
        :return: 벡터 ID
        """
        # TODO: 벡터 삽입
        pass

    def search(self, collection: str, vector: list, limit: int = 10) -> list:
        """
        유사도 검색

        :param collection: 컬렉션 이름
        :param vector: 쿼리 벡터
        :param limit: 검색 결과 제한
        :return: 검색 결과 리스트
        """
        # TODO: 유사도 검색
        pass
