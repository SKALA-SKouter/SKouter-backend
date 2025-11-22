"""
주기적 작업 (크롤링 스케줄러 등)
"""


class TaskScheduler:
    """
    작업 스케줄러
    """

    def __init__(self):
        """
        스케줄러 초기화
        """
        # TODO: 스케줄러 초기화
        pass

    def schedule_crawler(self, cron_expression: str, crawler_name: str):
        """
        크롤러 주기적 실행 스케줄링

        :param cron_expression: Cron 표현식
        :param crawler_name: 크롤러 이름
        """
        # TODO: 크롤링 스케줄 등록
        pass

    def start(self):
        """
        스케줄러 시작
        """
        # TODO: 스케줄러 시작
        pass

    def stop(self):
        """
        스케줄러 종료
        """
        # TODO: 스케줄러 종료
        pass
