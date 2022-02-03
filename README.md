# barstool-data-challenge
## Rundown of Deliverables

1. Produce a single codebase in the language of your choosing that:
- [x] Fetches the list of S3 files from the api above [here](run.py#L122-L124)
- [x] Parses each file [here](run.py#L64-L70)
- [x] Uploads every “line” in the file as a single row in the MySQL Database [here](run.py#L85)
2. Your codebase should contain a [single entrypoint](#run) `./run.sh` which executes your program in whatever language you choose.
- [x] Please provide [basic instructions](#setup) for installing your language and its dependencies 

### Bonus Points
- [x] Process files concurrently [here](run.py#L132-L133)
- [x] Stream processing [here](run.py#L52-L91)

## Setup
The codebase is written in Python, but has been Dockerized.  All that is required is an available Docker engine https://docs.docker.com/get-docker/

## Run
The Dockerized script takes its configuration from environment variables.  Here is a table of what is used:
| Variable | Required? | Description | Default |
| --- | --- | --- | --- |
| MYSQL_DATABASE | Y | Name of the target database ||
| MYSQL_USER | Y | Name of the MySQL user ||
| MYSQL_PASSWORD | Y | MySQL user's password ||
| MYSQL_HOST | Y | MySQL hostname/ip ||
| MYSQL_PORT | N | MySQL port | 3306 |
| CONCURRENT_FILES | N | Number of concurrent files to process | Value returned by `os.cpu_count()` |

Use `run.sh` to execute the process

```sh
chmod +x run.sh
./run.sh
```

In addition to exporting environment variables before running, `run.sh` supports sourcing values from a `.env` file in the same directory.  Here's an example `.env`:

```
MYSQL_DATABASE=barstool-data-challenge
MYSQL_USER=<very secret>
MYSQL_PASSWORD=<much secure>
MYSQL_HOST=<parts unknown>
```

## Developing