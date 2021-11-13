# dbt-postgres
This is where to start the data transformation with dbt and SQL Server.
> Sample data mart: `covid`

> Start your local development with `.\env\Scripts\activate`. For more details: [LOCALDEV.md](LOCALDEV.md)


## Common commands:
### Set enviroment variables before any dbt operations as we're gonna use dbt `env_var` within our `profiles.yml`:
- Windows
```
set POSTGRES_HOST=domain.com
set POSTGRES_USER=dbt_user
set POSTGRES_PASS=dbt_user
set POSTGRES_PORT=5432
set POSTGRES_DB=dbt
set POSTGRES_SCHEMA=anly
```

### Seed data
[Covid](/dbt/data/covid/covid_raw.csv)
```
dbt seed --project-dir ./dbt --target dev
```

### Run all models
```
dbt run --project-dir ./dbt --target dev --full-refresh --models +exposure:*
```

### Run all models - DELTA mode
```
dbt run --project-dir ./dbt --target dev --models +exposure:*
```

### Test models
```
dbt test --project-dir ./dbt --target dev --models +exposure:*
```



## `Awesome dbt` service
This is the data service via Restful API ([more details](services/api_service/README.md))

[![SSH deployment](https://github.com/datnguye/dbt-postgres/actions/workflows/ssh-to-server.yml/badge.svg?branch=main)](https://github.com/datnguye/dbt-postgres/actions/workflows/ssh-to-server.yml)

[Sample requests](services/api_service/.insomia/awesome-dbt-api-2021-10-03.json) with using [Insomia](https://insomnia.rest/)

*Swagger*:

![Alt text](/services/api_service/.insomia/awesome-dbt-api-docs-2021-10-03.png?raw=true "api redoc")

*Redoc*:

![Alt text](/services/api_service/.insomia/awesome-dbt-api-redoc-2021-10-03.png?raw=true "api redoc")


# WHAT NEXT?
 - API Header Key