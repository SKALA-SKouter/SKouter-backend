"""
공고 분석 로직
"""


class JobAnalyzer:
    """
    공고 분석 서비스
    """

    def analyze(self, job_content: str) -> dict:
        """
        공고 분석

        :param job_content: 공고 내용
        :return: 분석 결과
        """
        # TODO: LangChain을 활용한 공고 분석
        return {
            "skills": [],
            "experience": "",
            "salary_range": "",
            "benefits": []
        }
