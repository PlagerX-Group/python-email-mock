import functools

from flask import request

from utils.exceptions import ContentTypeNotPresentException, ContentTypeNotAllowedException


def content_type(ct):
    def _content_type(func):

        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            headers_content_type = request.headers.get("Content-Type", None)

            if headers_content_type is None:
                raise ContentTypeNotPresentException(f"Not present 'content-type' in headers.")

            if headers_content_type != ct:
                raise ContentTypeNotAllowedException(detail=f"Content-Type '{headers_content_type}' not allowed. "
                                                            f"Expected: '{ct}'.")

            return func(*args, **kwargs)

        return _wrapper

    return _content_type
