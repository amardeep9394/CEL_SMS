import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.error import HTTPError
import settings.settings as settings
from utils.logger import Logger

logger = Logger().get_logger()


class Server_Call:

    @staticmethod
    def requests_retry_session(self, retries=10, backoff_factor=1, session=None):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            method_whitelist=frozenset(['HEAD', 'TRACE', 'GET', 'PUT', 'OPTIONS', 'DELETE', 'POST'])
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def send_data_to_api(self, url, headers, method, data=None):
        try:
            data = json.dumps(data) if data else None

            response_api = self.requests_retry_session().request(method=method,
                                                                 url=url,
                                                                 headers=headers,
                                                                 data=data,
                                                                 timeout=300)
            response_object = response_api.json()
            response_api.raise_for_status()
            return response_object
        except (HTTPError, Exception) as ex:
            raise ex

    def post_to_server(self, payload):
        try:
            url = settings.SERVER_URL
            headers = settings.HEADER

            logger.info(f"URL - {url},  HEADER - {headers}, PAYLOAD - {payload}")
            response = self.send_data_to_api(url, headers, "POST", data=payload)

            return response
        except Exception as ex:
            logger.exception(f"Getting exception - {str(ex)}")
            raise ex

    def send_health_to_server(self):
        try:
            url = settings.SERVER_URL
            headers = settings.HEADER
            payload = {
                "status": 200,
                "message": "I am Alive!!"
            }
            logger.info(f"URL - {url},  HEADER - {headers}, PAYLOAD - {payload}")
            response = self.send_data_to_api(url, headers, "POST", data=payload)

            return response
        except Exception as ex:
            logger.exception(f"Getting exception - {str(ex)}")
            raise ex