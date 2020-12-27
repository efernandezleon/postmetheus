import asyncio
import argparse
import logging
import os
import sys

from api import run_api
from metrics import run_worker

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s - %(message)s")


async def main():
    """
    This function takes the arguments from the command line
    and will execute the worker and the API server
    """
    example = """Examples:
    > python3 postmetheus.py -c mycollection.json -e myenvironment.json -t 10"
    """

    parser = argparse.ArgumentParser(
        prog='postmetheus',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=example
        )
    parser.add_argument('--collection', '-c',
                        dest='collection',
                        default=os.environ.get('POSTMAN_COLLECTION'),
                        required=False,
                        help='Used to specify a Postman collection file. \
                              The env var POSTMAN_COLLECTION can also used.')

    parser.add_argument('--environment', '-e',
                        dest='environment',
                        default=os.environ.get('POSTMAN_ENVIRONMENT'),
                        required=False,
                        help='Used to specify a Postman environment file or URL. \
                              The env var POSTMAN_ENVIRONMENT can also used.')

    parser.add_argument('--timer', '-t',
                        dest='timer',
                        default=os.environ.get('WORKER_TIMER') or 10,
                        type=int,
                        required=False,
                        help='Used to specify the frequency in seconds to run Newman. \
                              The env var WORKER_TIMER can also used.')

    args = parser.parse_args()

    if args.collection is None:
        logging.error("The collection should be provided using the argument "
                      "--collection/-c or the env var POSTMAN_COLLECTION")
        sys.exit(1)

    loop = asyncio.get_event_loop()
    run_worker(loop, args.collection, args.environment, args.timer)
    run_api(loop)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
