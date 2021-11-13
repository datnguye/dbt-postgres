# Requirements:
- python >=3.7.x
- dbt >=0.20.2
- postgresql 12

# Getting ready?

## Install dbt 
Installed version: `dbt 0.20.2`

- Windows:
```
python -m venv env
.\env\Scripts\activate
python -m pip install --upgrade pip==21.2.4
python -m pip install -r requirements.txt
```

- Linux (Recommend to install WSL if you're in Windows):
```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```


## Create dbt profile for SQL Server with 5 threads
- Windows:
```
mkdir "%userprofile%/.dbt" 
xcopy "dbt_profile_template.yml" "%userprofile%/.dbt/profiles.yml" /Y
```

- Linux:
```
mkdir ~/.dbt
cp "dbt_profile_template.yml" ~/.dbt/profiles.yml /Y
```


## Install dbt packages 
You will find the basic packages in [packages.yml](packages.yml)
```
dbt deps --project-dir ./dbt
```


## Provision postgresql database (Optional)
```
--Connect to server with `sysadmin`
CREATE USER dbt_user WITH ENCRYPTED PASSWORD 'dbt_user';
ALTER USER dbt_user CREATEDB;

--Connect to server with `dbt_user`
CREATE DATABASE dbt;
```


## Let's run the first model
```
dbt run --project-dir ./dbt --target dev --models MyFirstModel
```

Off we go!
```
Running with dbt=0.20.2
Found 1 model, 2 tests, 0 snapshots, 0 analyses, 448 macros, 0 operations, 1 seed file, 0 sources, 0 exposures

12:37:53 | Concurrency: 10 threads (target='dev')
12:37:53 | 
12:37:53 | 1 of 1 START table model dbo.MyFirstModel............................ [RUN]
12:38:00 | 1 of 1 OK created table model dbo.MyFirstModel....................... [OK in 7.34s]
12:38:00 | 
12:38:00 | Finished running 1 table model in 7.55s.

Completed successfully

Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1
```
