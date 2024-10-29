# Background
Tiny cli generating application and variable wrappers from quix deployment specification.



## Prerequisites
The only requirement is a `quix.yaml` file generated using `quix` cli.


## Installation

`pip install git+https://github.com/piotrnowakowski-co/quixwrap.git`



## Quickstart

By default, the cli looks for the `quix.yaml` in current working directory, however the following snippets
are using test spec from different location set via `CONFIG_FILE` env variable.


```sh 
quixwrap apps --help


Usage: quixwrap apps [OPTIONS] COMMAND [ARGS]...

┌─ Options ──────────────────────────────────────────────────────────────┐
│ --help          Show this message and exit.                            │
└────────────────────────────────────────────────────────────────────────┘
┌─ Commands ─────────────────────────────────────────────────────────────┐
│ get    Returns a single deployment metadata and allows to generate a   │
│        python wrapper code from it.                                    │
│ list   Returns deployment(s) metadata found in a given yaml file.      │
└────────────────────────────────────────────────────────────────────────┘


```


Show single application metadata

```sh
CONFIG_FILE=tests/quix.yaml quixwrap apps get enricher


# Output
┌─────────────┬────────────────┬─────────────┬──────────┬────────────────────┐
│ Application │ Variable       │ Type        │ Required │ Default            │
├─────────────┼────────────────┼─────────────┼──────────┼────────────────────┤
│ enricher    │ INPUT          │ InputTopic  │ N        │ RecordsDownsampled │
│ enricher    │ OUTPUT         │ OutputTopic │ N        │ RecordsEnriched    │
│ enricher    │ DB_CONN        │ Secret      │ N        │                    │
│ enricher    │ CONSUMER_GROUP │ FreeText    │ N        │ enricher           │
│ enricher    │ ENV            │ FreeText    │ Y        │ development        │
└─────────────┴────────────────┴─────────────┴──────────┴────────────────────┘
```


List all applications


```sh
CONFIG_FILE=tests/quix.yaml quixwrap apps list


# Output
┌──────────────────────┬───────────────────┬─────────────┬──────────┬───────────────────────────────────────┐
│ Application          │ Variable          │ Type        │ Required │ Default                               │
├──────────────────────┼───────────────────┼─────────────┼──────────┼───────────────────────────────────────┤
│ enricher             │ INPUT             │ InputTopic  │ N        │ RecordsDownsampled                    │
│ enricher             │ OUTPUT            │ OutputTopic │ N        │ RecordsEnriched                       │
│ enricher             │ DB_CONN           │ Secret      │ N        │                                       │
│ enricher             │ CONSUMER_GROUP    │ FreeText    │ N        │ enricher                              │
│ enricher             │ ENV               │ FreeText    │ Y        │ development                           │
│ downsampler          │ INPUT             │ InputTopic  │ N        │ RecordsReceived                       │
│ downsampler          │ OUTPUT            │ OutputTopic │ N        │ RecordsDownsampled                    │
│ downsampler          │ CONSUMER_GROUP    │ FreeText    │ N        │ downsampler                           │
│ downsampler          │ ENV               │ FreeText    │ Y        │ development                           │
│ influxdb-data-reader │ OUTPUT            │ OutputTopic │ N        │ RecordsReceived                       │
│ influxdb-data-reader │ INFLUXDB_TOKEN    │ Secret      │ N        │                                       │
│ influxdb-data-reader │ INFLUXDB_ORG      │ FreeText    │ N        │ my-company                            │
│ influxdb-data-reader │ INFLUXDB_HOST     │ FreeText    │ N        │ http://localhost:8086                 │
│ influxdb-data-reader │ INFLUXDB_DATABASE │ FreeText    │ N        │ raw-bucket                            │
│ influxdb-data-reader │ CONSUMER_GROUP    │ FreeText    │ N        │ influxdb-data-writer                  │
│ influxdb-data-reader │ ENV               │ FreeText    │ Y        │ development                           │
│ influxdb-data-writer │ INPUT             │ InputTopic  │ N        │ RecordsEnriched                       │
│ influxdb-data-writer │ INFLUXDB_TOKEN    │ Secret      │ N        │                                       │
│ influxdb-data-writer │ INFLUXDB_TAG_KEYS │ FreeText    │ N        │ ['userId', 'userName','userCategory'] │
│ influxdb-data-writer │ INFLUXDB_HOST     │ FreeText    │ N        │ https://localhost:8086                │
│ influxdb-data-writer │ INFLUXDB_ORG      │ FreeText    │ N        │ my-company                            │
│ influxdb-data-writer │ INFLUXDB_DATABASE │ FreeText    │ N        │ silver-bucket                         │
│ influxdb-data-writer │ CONSUMER_GROUP    │ FreeText    │ N        │ influxdb-data-writer                  │
│ influxdb-data-writer │ ENV               │ FreeText    │ Y        │ development                           │
└──────────────────────┴───────────────────┴─────────────┴──────────┴───────────────────────────────────────┘
```


Generate python code for given application


```sh 
CONFIG_FILE=tests/quix.yaml quixwrap apps get enricher --as-py --no-standalone

# Output
from quixwrap import DeploymentWrapper, Config, Variable

class EnricherConfig(Config):
    input = Variable("INPUT", default="RecordsDownsampled", required=False, qtype="InputTopic")
    output = Variable("OUTPUT", default="RecordsEnriched", required=False, qtype="OutputTopic")
    db_conn = Variable("DB_CONN", qtype="Secret", required=False)
    consumer_group = Variable("CONSUMER_GROUP", default="enricher", required=False, qtype="FreeText")     
    env = Variable("ENV", default="development", required=True, qtype="FreeText")


class Enricher(DeploymentWrapper):
    config : EnricherConfig = EnricherConfig()


```