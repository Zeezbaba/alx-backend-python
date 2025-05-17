# ALX ProDev Database Seeder

This project provides a Python script (`seed.py`) to automate the creation and seeding of a MySQL database named `ALX_prodev`. It reads user data from a CSV file and inserts it into a table named `user_data`.

## 📌 Features

- Connects to a local MySQL server.
- Creates a database (`ALX_prodev`) if it does not already exist.
- Connects to the newly created database.
- Creates a `user_data` table with the following fields:
  - `user_id` (UUID, primary key)
  - `name` (string)
  - `email` (string, unique)
  - `age` (number)
- Reads user data from a CSV file (`user_data.csv`).
- Inserts data into the table while checking for duplicate email addresses to avoid redundancy.

## 🛠️ Technologies Used

- Python 3
- MySQL
- `mysql-connector-python` (for MySQL connection)
- `uuid` (for unique user ID generation)
- `csv` module (for reading CSV data)


## 🔄 How It Works

1. **Connect to MySQL** using credentials provided in the script.
2. **Create Database** `ALX_prodev` if it doesn't exist.
3. **Create Table** `user_data` inside the database with appropriate schema.
4. **Load CSV** file `user_data.csv` and parse it into a list of dictionaries.
5. **Insert Data** into the table only if the email does not already exist (ensuring uniqueness).

## 🚀 Getting Started

### Prerequisites

- MySQL server running locally
- Python 3.x installed
- Required Python packages:
  ```bash
  pip install mysql-connector-python
