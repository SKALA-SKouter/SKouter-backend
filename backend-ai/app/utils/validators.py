"""
데이터 검증
"""


class Validators:
    """
    데이터 검증 클래스
    """

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        이메일 유효성 검증

        :param email: 이메일
        :return: 유효 여부
        """
        # TODO: 이메일 정규표현식 검증
        return True

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        전화번호 유효성 검증

        :param phone: 전화번호
        :return: 유효 여부
        """
        # TODO: 전화번호 정규표현식 검증
        return True

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        URL 유효성 검증

        :param url: URL
        :return: 유효 여부
        """
        # TODO: URL 정규표현식 검증
        return True
