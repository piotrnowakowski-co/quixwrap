# QuixWrap
Tiny cli generating application and variable wrappers from quix deployment specification.



## Prerequisites
Make sure you have a `quix.yaml` file generated using `quix` cli.

In case you use placeholders in your `quix.yaml`, make sure you have
`.quix.yaml.variables` file that contains all values for respective placeholders.

You can configure the paths to both files using env vars (or pass them to the script inline)

```
export CONFIG_FILE=quix.yaml
export YAML_VARIABLES_FILE=.quix.yaml.variables

```


## Installation

`pip install git+https://github.com/piotrnowakowski-co/quixwrap.git`



## Quickstart

By default, the cli looks for both configuration files in the current working directory, however the following snippets are using configuration files from the `tests` folder which are passed to the cli script as inline env vars.

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
CONFIG_FILE=tests/quix.yaml YAML_VARIABLES_FILE=tests/.quix.yaml.variables quixwrap apps get enricher

┌─────────────┬────────────────┬─────────────┬──────────┬────────────────────┐
│ Application │ Variable       │ Type        │ Required │ Default            │
├─────────────┼────────────────┼─────────────┼──────────┼────────────────────┤
│ enricher    │ INPUT          │ InputTopic  │ N        │ RecordsDownsampled │
│ enricher    │ OUTPUT         │ OutputTopic │ N        │ RecordsEnriched    │
│ enricher    │ DB_CONN        │ Secret      │ N        │ None               │
│ enricher    │ CONSUMER_GROUP │ FreeText    │ N        │ enricher           │
│ enricher    │ ENV            │ FreeText    │ Y        │ development        │
│ enricher    │ DEBUG          │ FreeText    │ N        │ True               │
│ enricher    │ FOO            │ FreeText    │ N        │ None               │
│ enricher    │ LABEL          │ FreeText    │ N        │ DefaultEnricher    │
└─────────────┴────────────────┴─────────────┴──────────┴────────────────────┘
```


List all applications


```sh
CONFIG_FILE=tests/quix.yaml YAML_VARIABLES_FILE=tests/.quix.yaml.variables quixwrap apps list --expand

┌──────────────────────┬───────────────────┬─────────────┬──────────┬────────────────────────────┐
│ Application          │ Variable          │ Type        │ Required │ Default                    │ 
├──────────────────────┼───────────────────┼─────────────┼──────────┼────────────────────────────┤ 
│ enricher             │ INPUT             │ InputTopic  │ N        │ RecordsDownsampled         │ 
│ enricher             │ OUTPUT            │ OutputTopic │ N        │ RecordsEnriched            │ 
│ enricher             │ DB_CONN           │ Secret      │ N        │ None                       │ 
│ enricher             │ CONSUMER_GROUP    │ FreeText    │ N        │ enricher                   │ 
│ enricher             │ ENV               │ FreeText    │ Y        │ development                │ 
│ enricher             │ DEBUG             │ FreeText    │ N        │ True                       │ 
│ enricher             │ FOO               │ FreeText    │ N        │ None                       │ 
│ enricher             │ LABEL             │ FreeText    │ N        │ DefaultEnricher            │
│ downsampler          │ INPUT             │ InputTopic  │ N        │ RecordsReceived            │ 
│ downsampler          │ OUTPUT            │ OutputTopic │ N        │ RecordsDownsampled         │ 
│ downsampler          │ CONSUMER_GROUP    │ FreeText    │ N        │ downsampler                │ 
│ downsampler          │ ENV               │ FreeText    │ Y        │ development                │ 
│ influxdb-data-reader │ OUTPUT            │ OutputTopic │ N        │ RecordsReceived            │ 
│ influxdb-data-reader │ INFLUXDB_TOKEN    │ Secret      │ N        │ None                       │ 
│ influxdb-data-reader │ INFLUXDB_ORG      │ FreeText    │ N        │ my-company                 │ 
│ influxdb-data-reader │ INFLUXDB_HOST     │ FreeText    │ N        │ http://localhost:8086      │ 
│ influxdb-data-reader │ INFLUXDB_DATABASE │ FreeText    │ N        │ raw-bucket                 │ 
│ influxdb-data-reader │ CONSUMER_GROUP    │ FreeText    │ N        │ influxdb-data-writer       │ 
│ influxdb-data-reader │ ENV               │ FreeText    │ Y        │ development                │ 
│ influxdb-data-writer │ INPUT             │ InputTopic  │ N        │ RecordsEnriched            │
│ influxdb-data-writer │ INFLUXDB_TOKEN    │ Secret      │ N        │ None                       │ 
│ influxdb-data-writer │ INFLUXDB_TAG_KEYS │ FreeText    │ N        │ ['userId',                 │ 
│                      │                   │             │          │ 'userName','userCategory'] │ 
│ influxdb-data-writer │ INFLUXDB_HOST     │ FreeText    │ N        │ https://localhost:8086     │ 
│ influxdb-data-writer │ INFLUXDB_ORG      │ FreeText    │ N        │ my-company                 │ 
│ influxdb-data-writer │ INFLUXDB_DATABASE │ FreeText    │ N        │ silver-bucket              │ 
│ influxdb-data-writer │ CONSUMER_GROUP    │ FreeText    │ N        │ influxdb-data-writer       │ 
│ influxdb-data-writer │ ENV               │ FreeText    │ Y        │ development                │ 
└──────────────────────┴───────────────────┴─────────────┴──────────┴────────────────────────────┘ 
```


Generate python code for given application


```sh 
 CONFIG_FILE=tests/quix.yaml YAML_VARIABLES_FILE=tests/.quix.yaml.variables quixwrap apps get enricher --as-py --no-standalone


from quixwrap import DeploymentWrapper, Config, Variable

class EnricherConfig(Config):
    input = Variable("INPUT", default="RecordsDownsampled", required=False, qtype="InputTopic")    
    output = Variable("OUTPUT", default="RecordsEnriched", required=False, qtype="OutputTopic")    
    db_conn = Variable("DB_CONN", qtype="Secret", required=False)
    consumer_group = Variable("CONSUMER_GROUP", default="enricher", required=False, qtype="FreeText")
    env = Variable("ENV", default="development", required=True, qtype="FreeText")
    debug = Variable("DEBUG", default="True", required=False, qtype="FreeText")
    foo = Variable("FOO", default="None", required=False, qtype="FreeText")
    label = Variable("LABEL", default="DefaultEnricher", required=False, qtype="FreeText")


class Enricher(DeploymentWrapper):
    config : EnricherConfig = EnricherConfig()
```