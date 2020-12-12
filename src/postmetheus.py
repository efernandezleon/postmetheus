import asyncio
import argparse
import sys
import os

from api import run_api
from metrics import run_worker

async def main():
    """
    This function takes the arguments from the command line and will execute the worker and API server
    """
    example = """Examples:
    > python3 postmetheus.py -c mycollection.json -e myenvironment.json -t 5"
    """

    parser = argparse.ArgumentParser(prog='postmetheus',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=example)
    parser.add_argument('--collection', '-c', 
        dest='collection', 
        default=os.environ.get('POSTMAN_COLLECTION') or 'data/postman_collection.json', 
        required=False, 
        help='Used to specify a Postman collection file. The env var POSTMAN_COLLECTION can also used.')
    
    parser.add_argument('--environment', '-e', 
        dest='environment',
        default=os.environ.get('POSTMAN_ENVIRONMENT'),  
        required=False, 
        help='Used to specify a Postman environment file or URL. The env var POSTMAN_ENVIRONMENT can also used.')
    
    parser.add_argument('--timer', '-t', 
        dest='timer', 
        default=os.environ.get('WORKER_TIMER') or 5, 
        required=False, 
        help='Used to specify the frequency in seconds to run Newman. The env var WORKER_TIMER can also used.')
    
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    run_worker(loop, args.collection, args.environment, args.timer)
    run_api(loop)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    try:
        loop.run_forever()
    except:
        pass
