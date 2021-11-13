# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
RUN mkdir app
WORKDIR /app/

# Copy project
RUN mkdir dbt
COPY ./dbt ./dbt
COPY ./services/api_service .

# Create dbt profiles.yml
# Recommend to use environment variables in: profiles.yml/outputs.prod
# [dbt env_var](https://docs.getdbt.com/reference/dbt-jinja-functions/env_var)
RUN mkdir ~/.dbt
COPY dbt_profile_template.yml dbt_profile_template.yml
RUN  cp ./dbt_profile_template.yml ~/.dbt/profiles.yml

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Install dbt packages
RUN dbt deps --project-dir ./dbt

# Arguments
ENV SERVER="dummy"
# TODO: Use Key Vault here
ENV USER="dummy"
ENV PASSWORD="dummy"

# Entry point
CMD export env_postgres_host_secret=${SERVER} && \
    export env_postgres_user_secret=${USER} && \
    export env_postgres_password_secret=${PASSWORD} && \
    uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir "/app"