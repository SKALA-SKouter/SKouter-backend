"""
대화 히스토리 관리
"""


class ChatMemory:
    """
    대화 히스토리 관리 서비스
    """

    def add_message(self, user_id: str, message: str, sender: str) -> None:
        """
        메시지 추가

        :param user_id: 사용자 ID
        :param message: 메시지
        :param sender: 발신자 (user, bot)
        """
        # TODO: 메시지 저장
        pass

    def get_history(self, user_id: str, limit: int = 50) -> list:
        """
        히스토리 조회

        :param user_id: 사용자 ID
        :param limit: 조회 제한
        :return: 히스토리 리스트
        """
        # TODO: 히스토리 조회
        return []

    def clear_history(self, user_id: str) -> None:
        """
        히스토리 초기화

        :param user_id: 사용자 ID
        """
        # TODO: 히스토리 삭제
        pass
