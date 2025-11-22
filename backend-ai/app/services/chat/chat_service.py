"""
대화 관리
"""


class ChatService:
    """
    챗봇 서비스
    """

    def send_message(self, user_id: str, message: str) -> str:
        """
        사용자 메시지 처리

        :param user_id: 사용자 ID
        :param message: 사용자 메시지
        :return: 챗봇 응답
        """
        # TODO: 메시지 처리 및 응답 생성
        return ""

    def get_conversation_history(self, user_id: str) -> list:
        """
        대화 히스토리 조회

        :param user_id: 사용자 ID
        :return: 대화 히스토리
        """
        # TODO: 대화 히스토리 조회
        return []
