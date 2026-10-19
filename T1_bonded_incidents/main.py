import logging
from util import setup_logging

from search_incident_for_bind import search_incident


logger = logging.getLogger(__name__)


def main():
    """
    компания с id 54 пока что исключена до дальнейшего решения

    :return:
    """
    setup_logging()
    try:
        search_incident()
    except Exception as error:
        logger.exception('%s', error)
        raise
    finally:
        logging.shutdown()


if __name__ == '__main__':
    main()
