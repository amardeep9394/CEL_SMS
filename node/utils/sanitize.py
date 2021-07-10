import re
from utils.logger import Logger

logger = Logger().get_logger()


class Sanitize:
    def __init__(self):
        pass

    def sanitize_packet(self, data):
        try:
            logger.info(f"DATA SANITIZE - {data}")

            data = data.replace("\n", "")
            data = data.replace(",", "")

            # found = ''
            # m = re.search('%(.+?)$', data)
            # if m:
            #     found = m.group(1)
            return data

        except Exception as ex:
            logger.exception(f"Getting exception - {str(ex)}")
            return ''
