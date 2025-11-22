"""
공고 비교 로직
"""


class JobComparator:
    """
    공고 비교 서비스
    """

    def compare(self, job_ids: list) -> dict:
        """
        공고 비교

        :param job_ids: 비교할 공고 ID 리스트
        :return: 비교 결과
        """
        # TODO: LangChain을 활용한 공고 비교
        return {
            "similarities": [],
            "differences": [],
            "recommendation": ""
        }
