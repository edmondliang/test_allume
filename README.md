### SETUP

1. setup your postgres database
2. create schemas by run the script in migration folder in your postgres server
3. setup your python environment
```
pipenv install -d
cp example.env .env
# modify your .env
cp example.flaskenv .flaskenv
# modify your .flaskenv
```

### test
```
pipenv run pytest
```

### run your server
```
pipenv run flask run
```



