import pydantic
import typing as t


class BasePydanticModel(pydantic.BaseModel):

    @property
    def as_json(self) -> dict:
        raise NotImplementedError()


class PySMTPMessageModel(BasePydanticModel):
    mail_from: str
    mail_to: t.List[str]
    mail_data: str
    helo_or_ehlo: str

    @property
    def as_json(self) -> dict:
        return {'mail_from': self.mail_from, 'mail_to': self.mail_to, 'data': self.mail_data}
