# hemayat

## setup

### install the requirements

```
pip install -r requirements.txt
```

### SECRET_KEY and DATABASES

SECRET_KEY and DATABASES are set in ```hemayat/secrets.py``` file.

rename ```hemayat/secrets-sample.py``` to ```hemayat/secrets.py``` for a basic setup.

### run the migrations
```
python manage.py migrate
```

### start the development server
```
python manage.py runserver
```
