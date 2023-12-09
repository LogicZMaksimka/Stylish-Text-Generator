FROM postgres:latest
WORKDIR /postgres_setup
# COPY fill.sql /docker-entrypoint-initdb.d/create_fixtures.sql
CMD PGPASSWORD=123456 psql -h "db" -U postgres -a -f /postgres_setup/fill.sql