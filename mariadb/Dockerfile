FROM mariadb:focal

# this only runs on the first startup so if you're debugging
# make sure to stop and prune any volumes from the docker container
# after making changes
COPY *.sql /docker-entrypoint-initdb.d/
