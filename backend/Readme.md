```
  docker run -d \
     --name saline-postgres \
     -e POSTGRES_PASSWORD=pgpassword \
     -e POSTGRES_USER=pguser \
     -e POSTGRES_DB=pgdb \
     -v saline-db:/var/lib/postgresql/data \
     -p 5432:5432 \
     postgres:15.3
```
