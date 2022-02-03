import requests
import os
import zlib
import json
import sys
from functools import partial
from multiprocessing import Pool
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    DateTime,
    Text,
    JSON,
)


MYSQL_DATABASE = os.environ["MYSQL_DATABASE"]
MYSQL_USER = os.environ["MYSQL_USER"]
MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]
MYSQL_HOST = os.environ["MYSQL_HOST"]
MYSQL_PORT = os.environ.get("MYSQL_PORT", "3306")

try:
    CONCURRENT_FILES = int(os.environ["CONCURRENT_FILES"])
    if CONCURRENT_FILES < 1:
        raise ValueError
except KeyError:
    CONCURRENT_FILES = os.cpu_count()
    print(f"Defaulting CONCURRENT_FILES to cpu count: {CONCURRENT_FILES}")
except ValueError:
    sys.exit(f"CONCURRENT_FILES must be an integer greater than 0")
    
    

STREAM_CHUNK_SIZE = 2**10
LINE_DELIMETER = b"\n"
BULK_INSERT_SIZE = 1000


def stream_parse_load(url: str, table: Table, connection_string: str):
    """Streams the content of `url`, parses each json line, and loads to `table`

    Arguments:
    :param str url: url of the gzipped jsonlines file to load
    :param sqlalchemy.Table table: destination table
    :param str connection_string: sqlalchemy connection string
    """
    source_file = url.split("/")[-1]
    engine = create_engine(connection_string)
    content_stream = requests.get(url, stream=True)

    # We can iteratively decompress a streamed gzip file using zlib
    decompresser = zlib.decompressobj(32 + zlib.MAX_WBITS)  # skip header on gzip file
    content_stream_decompressed = b""
    value_buffer = []

    for chunk in content_stream.iter_content(chunk_size=STREAM_CHUNK_SIZE):
        content_stream_decompressed += decompresser.decompress(chunk)

        # After decompressing a chunk from the stream, check to see if there are any complete json lines
        while True:
            index_of_newline = content_stream_decompressed.find(LINE_DELIMETER)

            if index_of_newline == -1:
                break

            current_line = content_stream_decompressed[:index_of_newline]
            current_line_parsed = json.loads(current_line)

            value_buffer.append(
                dict(
                    timestamp=current_line_parsed["TIMESTAMP"],
                    user_id=current_line_parsed["USER_ID"],
                    episode_id=current_line_parsed["EPISODE_ID"],
                    show_id=current_line_parsed["SHOW_ID"],
                    source_file=source_file,
                    raw=current_line_parsed,
                )
            )

            # When the buffer reaches the configured size, flush it to the database
            if len(value_buffer) == BULK_INSERT_SIZE:
                engine.execute(table.insert(), value_buffer)
                value_buffer = []

            # This might not be super efficient as the data is copied, i.e. no popping
            content_stream_decompressed = content_stream_decompressed[
                index_of_newline + 1 :
            ]

    # Flush any remaining records to the db
    if len(value_buffer) > 0:
        engine.execute(table.insert(), value_buffer)


if __name__ == "__main__":
    connection_string = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    engine = create_engine(connection_string)

    # TODO:
    #   - Determine if incremental id is useful
    #   - Determine if Text fields should have length limits
    #   - Determine if there should be any unique constraints
    #   - Determine if any indexes will help support common query patterns
    table = Table(
        "user_episode_log",
        MetaData(),
        Column("timestamp", DateTime, nullable=False),
        Column("user_id", Text, nullable=False),
        Column("episode_id", Text, nullable=False),
        Column("show_id", Text, nullable=False),
        Column("source_file", Text, nullable=False),
        Column("raw", JSON, nullable=False),
    )

    # TODO: consider use of migration tool, e.g. Alembic
    table.drop(engine, checkfirst=True)
    table.create(engine)

    files = requests.get("https://data-challenge.origin.barstool.dev/files").json()[
        "files"
    ]

    # In order to map the file urls to the stream_parse_load function,
    # we have to create a new function with table and connection_string pre-baked
    worker = partial(
        stream_parse_load, table=table, connection_string=connection_string
    )

    with Pool(CONCURRENT_FILES) as pool:
        pool.map(worker, files)
