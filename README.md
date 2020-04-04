# RecoMapp

## First Run

### Creating Database and Authorized User
```shell script
psql -U postgres
# Type the password which is set in the setup. #
```

```sql
CREATE DATABASE recom_db;
CREATE USER recom_admin WITH PASSWORD 'recom123';
ALTER ROLE recom_admin SET client_encoding TO 'utf8';
ALTER ROLE recom_admin SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE recom_db TO recom_admin;
```

### Installing Requirements and First Commands
```shell script
pip install -r requirements.txt
```

```shell script
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
# Fill the form. (Only username and password fields are required.) #
```

## Fresh Start After Migration Faults
1. Drop the database and recreate it using the commands given above.
2. Delete all files in the migrations folder. (excluding \_\_init\_\_.py)
3. Run the commands given in the First Commands section.

## Upgrade setuptools
```shell script
python -m pip install pip --upgrade
pip install setuptools --upgrade --ignore-installed
python -m pip install --upgrade Pillow
```