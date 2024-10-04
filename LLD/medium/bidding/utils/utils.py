from datetime import datetime


class Utils:
    @staticmethod
    def date_to_str(date: datetime.date) -> str:
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def str_to_date(date_string: str) -> datetime.date:
        return datetime.strptime(date_string, '%Y-%m-%d').date()

    @staticmethod
    def represents_int(s: str) -> bool:
        try:
            int(s)
        except ValueError:
            return False
        return True

    @staticmethod
    def represents_date(s: str) -> bool:
        try:
            datetime.strptime(s, '%Y-%m-%d').date()
        except ValueError:
            return False
        return True
