<h1 align="center">Webapp<h1>

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python installed
- PIP installed
- mysql set up

##### For a Virtual Machine

Run the following command to set up all the prerequisites required for the application.

```sh
./installations.sh
```

Running this script will set up

- Python
- PIP
- MariaDB
- unzip
- A directory named demo with .env file
- start the MariaDB server

## Intructions

1. Clone the repo
2. Navigate to the repo
   ```sh
   cd your-flask-app
   ```
3. setup the .env file with the following
   ```sh
   DB_USER=<user>
   DB_PASSWORD=<your_password>
   DB_HOST=<host>
   DB_PORT=3306
   DB_NAME=<your_db_name>
   ```
4. To install everything else required for the application to run, do the following in the directory

   ```sh
   pip3 install -r requirements.txt
   ```

   It installs all the following

   - Flask
   - Flask-SQLAlchemy
   - pymysql
   - python-dotenv
   - flask-bcrypt
   - pytest

5. Once this is done, run this command to start the application
   ```sh
   python3 main.py
   ```
   
