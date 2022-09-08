import functools

from flask import request

from packages.http.content_type import ContentTypeEnum
from utils.exceptions import ContentTypeNotPresentException, ContentTypeNotAllowedException


def content_type(ct: ContentTypeEnum):
    def _content_type(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            headers_content_type = request.headers.get("Content-Type", None)

            if headers_content_type is None:
                raise ContentTypeNotPresentException(f"Not present 'content-type' in headers.")

            if headers_content_type.lower() != ct.value.lower():
                raise ContentTypeNotAllowedException(detail=f"Content-Type '{headers_content_type}' not allowed. "
                                                            f"Expected: '{ct}'.")

            return func(*args, **kwargs)
        return _wrapper
    return _content_type


def request_to_object(obj):
    def wrapper(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):

            if request.content_type.lower() != 'application/json':
                raise ContentTypeNotAllowedException(detail=f"Content-Type '{request.content_type}' not allowed. "
                                                            f"Expected: 'application/json'.")

            return func(*args, **kwargs, request_object=obj(**request.json))
        return _wrapper
    return wrapper
