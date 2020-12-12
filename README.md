# PostMetheus

This is a tool to continuously check an API described in a Postman collection and exporting the metrics via Prometheus

## Requirements:

The script has been developed using Python 3.9 and it needs the Postman CLI [newman](https://github.com/postmanlabs/newman) to works. It can be installed with:

```
$ npm install -g newman
```

## How to use:

1. Define your Postman collection and include tests to verify the endpoints are working properly. To know more about how to write tests, you can head for official (guideline)[https://learning.postman.com/docs/writing-scripts/test-scripts/]. In addition, there are some samples of collections in the folder `data` to just to play around with this tool.

2. Install the dependencies in the `requirements.txt` with the following command:

    ```
    $ pip install -r requirements.txt
    ```

3. Run the Python script with the following command:

    ```
    $ python3 src/postmetheus.py -c my_collection.json
    ```

    To know more about the different options available in the script you can use the flag `--help`:

    ```
    usage: postmetheus [-h] [--collection COLLECTION] [--environment ENVIRONMENT] [--timer TIMER]

    optional arguments:
    -h, --help            show this help message and exit
    --collection COLLECTION, -c COLLECTION
                            Used to specify a Postman collection file or URL. The env var POSTMAN_COLLECTION can also used.
    --environment ENVIRONMENT, -e ENVIRONMENT
                            Used to specify a Postman environment file. The env var POSTMAN_ENVIRONMENT can also used.
    --timer TIMER, -t TIMER
                            Used to specify the frequency in seconds to run Newman. The env var WORKER_TIMER can also used.

    Examples:
        > python3 postmetheus.py -c mycollection.json -e myenvironment.json -t 5"
    ```

    This script will run periodically the `newman` tool and will expose the result via HTTP by using the Prometheus format.

4. The script will launch a HTTP server listening to the port `8080`, so you can access the path `http:/localhost:8080/metrics` and see the different metrics in the Prometheus text format.

The metrics will include:

- Number of fail tests for every endpoint.
- If every a single assertion for tests in every endpoint has passed or not.
- Response time for endpoints.
- Response size for endpoints.