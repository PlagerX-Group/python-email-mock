class BaseHttpException(Exception):
    detail: str = None
    exc: str = None
    status_code: int = None

    def __init__(self, detail: str = None, status_code: int = None):
        self.exc = self.__class__.__name__
        self.detail = detail if detail is not None else ''
        self.status_code = status_code if status_code is not None else 500

    @property
    def jsonify_response(self) -> dict:
        return {"detail": self.detail, "status": self.status_code, "exc": self.exc}


class ContentTypeNotAllowedException(BaseHttpException):
    """
    Ошибка: content-type не прошел валидацию
    """

    status_code = 400


class ContentTypeNotPresentException(BaseHttpException):
    """
    Ошибка: content-type отсутствует в заголовках.
    """

    status_code = 400
