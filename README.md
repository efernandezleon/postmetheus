# PostMetheus

[![GitHub Super-Linter](https://github.com/efernandezleon/postmetheus/workflows/Super-Linter/badge.svg)](https://github.com/marketplace/actions/super-linter)

A tool for continuously checking an API described in a Postman collection and exporting the metrics via Prometheus.

**The end goal of this tool:**

- Take advantage of the testing feature of Postman to use it as a **Continuous Testing of APIs**
- Provide an easy way to periodically run this monitoring testing without external and more sophisticated tools like NewRelic
- Expose the testing report as a **Prometheus** metrics in order to include them in your own monitoring and alert workflows 

## Requirements:

The script has been developed using Python 3.9 and it needs the Postman CLI [newman](https://github.com/postmanlabs/newman) to works. It can be installed with:

```
$ npm install -g newman
```

## How to use:

1. Define your Postman collection and include tests to verify the endpoints are working properly. To know more about how to write tests, you can head for official [guideline](https://learning.postman.com/docs/writing-scripts/test-scripts/). In addition, there are some samples of collections in the folder `data` to just to play around with this tool.

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
                            Used to specify a Postman environment file or URL. The env var POSTMAN_ENVIRONMENT can also used.
    --timer TIMER, -t TIMER
                            Used to specify the frequency in seconds to run Newman. The env var WORKER_TIMER can also used.

    Examples:
        > python3 postmetheus.py -c mycollection.json -e myenvironment.json -t 5
    ```

    This script will run periodically the `newman` tool and will expose the result via HTTP by using the Prometheus format.

4. The script will launch a HTTP server listening to the port `8080`, so you can access the path `http://localhost:8080/metrics` and see the different metrics in the Prometheus text format.

The metrics will include:

- Number of failed tests for every endpoint.
- If every a single assertion for tests in every endpoint has passed or not.
- Response time for endpoints.
- Response size for endpoints.

## Use with Docker:

The easiest way to run as a Docker container is to pull directly from the [Docker Hub](https://hub.docker.com/r/efernandezleon/postmetheus):

```
$ docker pull efernandezleon/postmetheus
```

Then, just run the container mounting a volume with the folder including the collection you want to monitor:

```
$ docker run \
    -e POSTMAN_COLLECTION=data/api_collection.json \
    -v /path/to/your/data:/usr/src/postmetheus/data \
    -p 8080:8080 \
    efernandezleon/postmetheus
```

## License

- [MIT License](https://github.com/efernandezleon/postmetheus/blob/main/LICENSE)
