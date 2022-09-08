import base64
import email

from email.header import decode_header


def decode_quoted_printable_string(_s: str) -> str:
    if _s is None:
        return None

    _s = _s.replace('\n', '').replace('\t', '')

    return_list = []
    for _string, _encoding in decode_header(_s):
        if _encoding is None:
            if type(_string) is bytes:
                return_list.append(_string.decode("utf-8"))
            else:
                return_list.append(_string)
        else:
            return_list.append(_string.decode(_encoding))
    return ', '.join(return_list).replace('  ', ' ')


def parse_multipart_in_email(_s: str) -> None:
    email_message = email.message_from_string(_s)
    for payload in email_message.get_payload():
        if type(payload) is str:
            return email_message.get_payload()
        for message_payload in payload.get_payload():
            return base64.b64decode(message_payload.get_payload()).decode('utf-8')
