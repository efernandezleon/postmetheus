import subprocess
import json
import asyncio
import os.path
import sys

from prometheus_client import (
    Gauge, Histogram, REGISTRY, generate_latest
)

METRICS = {}
OUTPUT_FILE = 'outputfile.json'


def run_worker(loop, collection, environment, time_to_wait):
    """ Setup a worker to run Newman CLI periodically """
    print(f"Running Newman for the collection {collection}")

    loop.create_task(
        _run_periodically(
            time_to_wait,
            _generate_metrics,
            collection,
            environment
        )
    )


def metrics_to_text():
    return generate_latest(REGISTRY).decode('utf-8')


async def _run_periodically(wait_time, func, *args):
    while True:
        func(*args)
        await asyncio.sleep(wait_time)


def _run_newman(collection, environment):
    _check_file(collection)
    _check_file(environment) if environment else None

    environment = f'-e {environment}' if environment else ''
    process = subprocess.Popen(
        [f"""
        /usr/local/bin/newman run {collection} {environment} \
            --reporters json --reporter-json-export {OUTPUT_FILE}
        """],
        shell=True, stdout=subprocess.PIPE)
    process.wait()


def _generate_metrics(collection, environment):
    _run_newman(collection, environment)
    data = _read_file(OUTPUT_FILE)
    if not data:
        print('Error reading the newman output file')
        return

    for execution in data['run']['executions']:
        item = execution['item']
        name = item['name']
        assertions = execution.get('assertions') or []
        common_key = f"request_{_normalize(name)}"

        # Generating Gauge metrics for errors in tests
        errors = [e for e in assertions if e.get('error')]
        _create_gauge(
            name=f'{common_key}_errors',
            description=f"Number of failed tests for the request {name}",
            value=len(errors)
        )

        for ass in assertions:
            test_name = ass['assertion']
            _create_gauge(
                name=f"{common_key}_{_normalize(ass['assertion'])}",
                description=f"Number of failure for the test '{test_name}'",
                value=1 if 'error' in ass else 0
            )

        # Generating Histograms for response time and size
        _create_histogram(
            name=f'{common_key}_response_time',
            description=f"Response time for the request {item['name']}",
            value=execution['response']['responseTime']
        )

        _create_histogram(
            name=f'{common_key}_response_size',
            description=f"Response size for the request {item['name']}",
            value=execution['response']['responseSize']
        )


def _normalize(text):
    return text.lower().replace(' ', '_')


def _check_file(file):
    if file.startswith(('http://', 'https://')):
        return
    if not os.path.isfile(file):
        print(f'File {file} not found')
        sys.exit(1)


def _read_file(input_file):
    with open(input_file) as f:
        data = json.load(f)
    return data


def _create_gauge(name, description, value):
    METRICS[name] = METRICS.get(name) or Gauge(name, description)
    gauge = METRICS.get(name)
    gauge.set(value)


def _create_histogram(name, description, value):
    METRICS[name] = METRICS.get(name) or Histogram(name, description)
    histogram = METRICS.get(name)
    histogram.observe(value)
