# Awesome dbt
This is the data services via Restful API

[![SSH deployment](https://github.com/datnguye/dbt-postgres/actions/workflows/ssh-to-server.yml/badge.svg?branch=main)](https://github.com/datnguye/dbt-postgres/actions/workflows/ssh-to-server.yml)

[Sample requests](.insomia/awesome-dbt-api-2021-10-03.json) with using [Insomia](https://insomnia.rest/)

*Swagger*:

![Alt text](.insomia/awesome-dbt-api-docs-2021-10-03.png?raw=true "api redoc")

*Redoc*:

![Alt text](.insomia/awesome-dbt-api-redoc-2021-10-03.png?raw=true "api redoc")



### DEV
- [Optional] Set the `python` alias (if Linux)
```
update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1
python --version
```
- [Install dbt & activate env](../../LOCALDEV.md)


#### Start service locally
```
set env_postgres_user_secret=dbt_user
set env_postgres_password_secret=dbt_user
set env_postgres_host_secret=domain.com
uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir "./services/api_service" --reload
```

- To see the API document: http://127.0.0.1:8000/docs
- To see the Open API document: http://127.0.0.1:8000/redoc


