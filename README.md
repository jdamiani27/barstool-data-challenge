# barstool-data-challenge
## Rundown of Deliverables

1. Produce a single codebase in the language of your choosing that:
a. Fetches the list of S3 files from the api above :white_check_mark: (here)[run.py#L122-L124]
b. Parses each file 
c. Uploads every “line” in the file as a single row in the MySQL Database
2. Your codebase should contain a single entrypoint `./run.sh` which executes your program in whatever language you choose.
a. Please provide basic instructions for installing your language and its dependencies