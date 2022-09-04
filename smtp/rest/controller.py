import os
import requests

from requests.exceptions import ConnectionError, HTTPError
from urllib.parse import urljoin

from utils.logger import smtp_logger


class APIController(object):

    @property
    def url_backend(self) -> str:
        host = os.getenv('BACKEND_HOSTNAME')
        port = os.getenv('BACKEND_PORT')

        # TODO: вынести проверку всех обязательных параметров в отдельную функцию в начале работы сервера.
        if host is None:
            raise Exception('Missing required environment variable: "BACKEND_HOSTNAME"')
        if port is None:
            raise Exception('Missing required environment variable: "BACKEND_PORT"')

        return f"http://{host.strip('/')}:{port}"

    def __request(self, url: str, method: str, json: dict = None, headers: dict = None,
                  expected_status_code: int = 200) -> requests.Response:
        smtp_logger.api_request(f'Preparation of sending a request to the API ({method}: {url}): {json}')
        try:
            response = requests.request(method=method, url=url, json=json, headers=headers)
        except ConnectionError as e:
            smtp_logger.api_request(f"Request ended with an error\n"
                                    f"Exception '{ConnectionError.__class__.__name__}': {e}")
            return

        if response.status_code != expected_status_code:
            raise HTTPError(f'Expected status code: {expected_status_code}. Got: {response.status_code}. '
                            f'Reason: {response.text}')
        else:
            response_json = response.json()
            smtp_logger.api_request(f'Request sent successfully (uuid={response_json.get("uuid")})')
            return response

    def send_message(self, mail_from: str, mail_to: str, content: str, helo_or_ehlo: str) -> requests.Response:
        payload = {'mail_from': mail_from, 'mail_to': mail_to, 'mail_data': content, 'helo_or_ehlo': helo_or_ehlo}
        return self.__request(urljoin(self.url_backend, 'smtp/message'), method='post', json=payload)
