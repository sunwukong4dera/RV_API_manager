import logging
import sys

from util import setup_logging
from T1_bonded_incidents import binding

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    try:
        if len(sys.argv) > 1:
            identifier: str = sys.argv[1]
            binding(identifier)
    except Exception as error:
        logger.exception('%s', error)
        raise
    finally:
        logging.shutdown()


if __name__ == '__main__':
    main()