import requests
import json
import logging

logger = logging.getLogger(__name__)

def get_response(end_point: str, query_field=None, query_msg=None):
    response = None

    try:
        if query_msg and query_field:
            response = requests.get(end_point, params={query_field: query_msg})
        else:
            response = requests.get(end_point, params={})
    except Exception as e:
        logger.exception(e)

    if response is not None and response.status_code == 200:
        return json.loads(response.text)
    else:
        if response is not None:
            logger.error(
                "\n\t".join(
                    (
                        "Response Error",
                        str(response.status_code),
                        str(response.text),
                    )
                )
            )
        else:
            logger.error("Response is None")

        return None
