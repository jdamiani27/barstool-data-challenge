if [ -f .env ];
then
    echo "Found .env file, sourcing"
    export $(cat .env | xargs)
fi

echo "Building the Docker container"
docker build . -t jdamiani/barstool-data-challenge

echo "Running the container"
docker run --env MYSQL_DATABASE --env MYSQL_USER --env MYSQL_PASSWORD --env MYSQL_HOST --env MYSQL_PORT --env CONCURRENT_FILES jdamiani/barstool-data-challenge