
<div align="center">
  <img src="images/containers.png" alt="containers" width="400"/>
</div>

## Bank API

This is a simple bank API with routes for creating a new bank accounts, transferring money between accounts and getting the balance of an account and creating new customers. The API is built using FastAPI and the data is stored in a postgres database. In the below image, the schema of postgres database is shown:

<div align="center">
  <img src="images/database_schema.png" alt="database_schema" width="400"/>
</div>

<br/>

The API is dockerized and can be run using docker-compose. The docker-compose setup will create 3 containers:

- A container for the FastAPI application (`localhost:8000`)
- A container for the postgres database (`localhost:5433`)
- A container for the pgadmin interface (`localhost:5050`)


## Run the API

There are 2 ways to run the API (run commands from the root directory of the project):

1. Simply use docker-compose to set everything up:

```bash
docker-compose up
```

2. Using uvicorn:

```bash
# install the dependencies
pip install -r requirements.txt

# run the postgres database to serve the backend
docker-compose up -d db

# run the API
python3 banking_api/src/main.py
```

The API will be available at `http://localhost:8000` and the docs will be available at `http://localhost:8000/docs` and `http://localhost:8000/redoc`. 
First send a post request to `http://localhost:8000/auth/token/` to get a jwt token, then use this token in the `Authorization` header of the requests to the API (or use the jwt token in following examples). The username and password are hardcoded in the code and are `admin` and `admin123` respectively.


## Details of the API routes


### Auth

To have a security layer, the API uses a simple authentication mechanism. The API expects an `Authorization` header with the value `Bearer <token>`. The jwt token can be obtained from the `/auth/token/` endpoint. The jwt token includes the username and the passwordm which for this project are set to `admin` and `admin123` respectively.

When a request is sent to retrieve a token, the password will be hashed and compared to the hashed password in the database. This is done for security reasons, so that if the password is leaked, it will not be possible to use it to get a token (only the hash will be leaked).

To get a token, send a post request to `http://localhost:8000/auth/token/`:

```bash
curl -X 'POST' \
  'http://localhost:8000/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=admin&password=admin123&scope=&client_id=string&client_secret=string'
```

the result will be a jwt token such as (Tokens are valid for about 2 years):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTgwMTQwNTk5Mn0.-mfrsoLeT-hhm2snLA4I7zAA1Wu5ZPJrSF3rhKwIjhk",
  "token_type": "bearer"
}
```

This token should be used in the `Authorization` header of the requests to the API.

### Customers

The `customers` route has one endpoint for creating a new customer:

#### Create a new customer

The `http://localhost:8000/customers/create/` end point will create a new customer. here is a simple example of how to create a new customer:

```bash
curl -X 'POST' \
  'http://localhost:8000/customers/create/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTgwMTQwNTk5Mn0.-mfrsoLeT-hhm2snLA4I7zAA1Wu5ZPJrSF3rhKwIjhk' \
  -d '{
  "name": "John Doe",
  "id": 5
}'
```


### Accounts

The `accounts` route has 2 endpoints:

#### Create a new account

The `http://localhost:8000/accounts/create/` end point will create a new account for a customer. here is a simple example of how to create a new account (note that when creating a new account, the customer id should be already in the database):

```bash
curl -X 'POST' \
  'http://localhost:8000/accounts/create/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTgwMTQwNTk5Mn0.-mfrsoLeT-hhm2snLA4I7zAA1Wu5ZPJrSF3rhKwIjhk' \
  -d '{
  "customer_id": 4,
  "initial_deposit": 1234
}'
```

#### Get the balance of an account

The `http://localhost:8000/accounts/{account_id}/balance/` end point will return the balance of the account with the given id. Here is an example of how to get the balance of an account:

```bash
curl -X 'GET' \
  'http://localhost:8000/accounts/1/balance/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTgwMTQwNTk5Mn0.-mfrsoLeT-hhm2snLA4I7zAA1Wu5ZPJrSF3rhKwIjhk'
```

### Transactions

The `transactions` route has 2 endpoints for transferring money between accounts and getting the transaction history of an account:

#### Transfer money between accounts

The `http://localhost:8000/transactions/transfer/` end point will transfer money between 2 accounts. Here is an example of how to transfer money between 2 accounts:

```bash
curl -X 'POST' \
  'http://localhost:8000/transactions/transfer/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTgwMTQwNTk5Mn0.-mfrsoLeT-hhm2snLA4I7zAA1Wu5ZPJrSF3rhKwIjhk' \
  -d '{
    "from_account": 1,
    "to_account": 2,
    "amount": 123
  }'
```

#### Get the transaction history of an account

The `http://localhost:8000/transactions/history/{account_id}/` end point will return the transaction history of the account with the given id. Here is an example of how to get the transaction history of an account:

```bash
curl -X 'GET' \
  'http://localhost:8000/transactions/history/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTgwMTQwNTk5Mn0.-mfrsoLeT-hhm2snLA4I7zAA1Wu5ZPJrSF3rhKwIjhk'
```


## Tests

The tests can be run using the following command:

```bash
pip install pytest
pytest .
```

All the tests are in the `tests` directory and they cover all the endpoints of the API, including exceptions and edge cases.

Subsequently, you can checkout the pytest coverage report by running which will create a `coverage.md` file for detailed coverage report:

```bash
# make sure the database is running, if not run the following command
docker-compose up -d db

python3 -m pip install coverage

coverage run -m pytest 
coverage report -m --format=markdown > coverage.md

# end the database
docker-compose down --volumes
```

Current coverage report looks like this:

```markdown
| Name                                     |    Stmts |     Miss |   Cover |   Missing |
|----------------------------------------- | -------: | -------: | ------: | --------: |
| banking\_api/src/banking\_operations.py  |       30 |        1 |     97% |        52 |
| banking\_api/src/main.py                 |       17 |        4 |     76% | 23, 28-30 |
| banking\_api/src/postgres\_interface.py  |       27 |        0 |    100% |           |
| banking\_api/src/postgres\_models.py     |       21 |        0 |    100% |           |
| banking\_api/src/pydantic\_models.py     |       20 |        0 |    100% |           |
| banking\_api/src/routes/accounts.py      |       18 |        0 |    100% |           |
| banking\_api/src/routes/auth.py          |       15 |        1 |     93% |        23 |
| banking\_api/src/routes/customers.py     |       11 |        0 |    100% |           |
| banking\_api/src/routes/transactions.py  |       21 |        1 |     95% |        34 |
| banking\_api/src/security.py             |       29 |        3 |     90% | 67, 71-72 |
| banking\_api/tests/\_\_init\_\_.py       |        0 |        0 |    100% |           |
| banking\_api/tests/conftest.py           |       22 |        0 |    100% |           |
| banking\_api/tests/test\_accounts.py     |       32 |        0 |    100% |           |
| banking\_api/tests/test\_auth.py         |        9 |        0 |    100% |           |
| banking\_api/tests/test\_customers.py    |       15 |        0 |    100% |           |
| banking\_api/tests/test\_transactions.py |       43 |        0 |    100% |           |
|                                **TOTAL** |  **330** |   **10** | **97%** |           |
```

## Linting

The code is linted using `pre-commit` hooks and linters like `black`, `flake8`, `isort` and `ruff`. The linters can be run using the following command:

```bash
pre-commit run --all-files
```