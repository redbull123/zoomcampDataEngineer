docker run -it \
  --network=pipeline_default\
  taxi_ingest:v001 \
    --username=root \
    --password=root \
    --port=5432 \
    --database=ny_taxi \
    --chunk-size=10000\
    --table-name=yellow_taxi_trips \
    --hostname=pgdatabase2 


    ## to cli database
    uv run pgcli -h localhost -p 5432 -u root -d ny_taxi



    #to create and run databse
    docker run -it --rm   -e POSTGRES_USER="root"   -e POSTGRES_PASSWORD="root"   -e POSTGRES_DB="ny_taxi"   -v ny_taxi_postgres_data:/var/lib/postgresql   -p 5432:5432  --network=pg-network postgres:18

    docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4