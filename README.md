### Requirements

* An activated python virtualenv.
* mongodb installed and running.

Virtualenv installation/activation example:
```bash
pip install virtualenv
virtualenv cep_api_env
source cep_api_env/bin/activate
```

MongoDB installation/running example to debian distributions:
```bash
sudo apt-get install mongodb
sudo service mongodb start
```

#### After installation of the above requirements:

### Installing the project

Clone the repository and install it:

```bash 
git clone https://github.com/rafaelcassau/cep_api.git
```

Go to `/cep_api` directory:

```bash
cd cep_api
```

Run the following command:

```bash
make install
```

### After installling

After installing the app, edit the `config.py` file with information about your mongodb running instance

```python

MONGO_HOST = 'your localhost address'
MONGO_PORT = 'your mongodb port'
MONGO_DBNAME = 'your database name'
```

#### WARNING: before running the tests is need start the project.

### Running

Running the application:

```bash
make run
```

### Testing

Running tests:

```bash
make test
```