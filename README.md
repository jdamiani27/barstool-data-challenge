# barstool-data-challenge
## Rundown of Deliverables

1. Produce a single codebase in the language of your choosing that:
- Fetches the list of S3 files from the api above :white_check_mark: [here](run.py#L122-L124)
- Parses each file :white_check_mark: [here](run.py#L64-L70)
- Uploads every “line” in the file as a single row in the MySQL Database :white_check_mark: [here](run.py#L85)
2. Your codebase should contain a single entrypoint `./run.sh` which executes your program in whatever language you choose.
- Please provide [basic instructions](#setup) for installing your language and its dependencies :white_check_mark:

### Bonus Points
- Process files concurrently :white_check_mark: [here](run.py#L132-L133)
- Stream processing :white_check_mark: [here](run.py#L52-L91)

## Setup
The codebase is written in Python, but has been Dockerized.  All that is required is an available Docker engine https://docs.docker.com/get-docker/

## Run

## Developing