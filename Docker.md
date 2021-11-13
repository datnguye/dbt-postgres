### Dockerfile

### Build image:latest
```
docker rm awesome-dbt
docker rmi tuiladat/awesome-dbt
docker build --tag tuiladat/awesome-dbt:latest . -f ./Dockerfile
```

### Run containter
```
docker rm awesome-dbt
docker run --publish 8000:8000 --name "awesome-dbt" ^
    --env SERVER="domain.com" ^
    --env USER="dbt_user" ^
    --env PASSWORD="dbt_user" ^
    tuiladat/awesome-dbt
```


### Publish to Hub
```
docker push tuiladat/awesome-dbt:latest
```
