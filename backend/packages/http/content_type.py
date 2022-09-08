import enum


@enum.unique
class ContentTypeEnum(enum.Enum):
    APPLICATION_JSON: str = 'application/json'
