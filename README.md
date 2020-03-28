# recomapp

```sql
CREATE DATABASE recom_db;
CREATE USER recom_admin WITH PASSWORD 'recom123';
ALTER ROLE recom_admin SET client_encoding TO 'utf8';
ALTER ROLE recom_admin SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE recom_db TO recom_admin;
```

```sh
pip install -r requirements.txt

python manage.py migrate
python manage.py makemigrations
python manage.py createsuperuser
```
