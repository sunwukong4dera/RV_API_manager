import logging
import sys

from T1_bonded_incidents import explore_incident
from util import setup_logging


logger = logging.getLogger(__name__)


def main():
    setup_logging()
    try:
        if len(sys.argv) > 1:
            identifier: str = sys.argv[1]
            explore_incident(identifier)
            # todo получение списка правил
    except Exception as error:
        logger.exception('%s', error)
        raise
    finally:
        logging.shutdown()


if __name__ == '__main__':
    main()