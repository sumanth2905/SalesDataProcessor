# Introduction

Sales Data Processor is an python repo which will have python scripts to process sales data of two regions and load it into the Postgres Database.

# Installation Guide
This project requires the following tools to get started:

- Python - The programming language used.
- PostgreSQL - A relational database management system based on SQL. 
- Virtualenv - A tool for creating isolated Python environments.

To get started, install Python and MySQL on your local computer if you don't have them already.

# Getting started
**Step 1. Clone the repository into a new folder and then switch to code directory**
```
$ git clone https://github.com/sumanth2905/SalesDataProcessor.git
$ cd SalesDataProcessor
```

**Step 2. Create a Virtual Environment and install Dependencies.**

If you don't have the virtualenv command yet, you can find installation [instructions here](https://virtualenv.pypa.io/en/latest/). Learn more about [Virtual Environments](https://www.geeksforgeeks.org/python-virtual-environment/).

```
$ pip install virtualenv
```
If you are not able to install virtualenv through pip, try below command
```
$ sudo apt install python3-virtualenv
```

Create a new Virtual Environment for the project and activate it.
```
$ virtualenv venv
$ source venv/bin/activate
```
Once the virtual environment is activated, the name of your virtual environment will appear on left side of terminal. In our case, venv named virtual environment is active.

Next, we need to install the project dependencies in this virtual environment, which are listed in requirements.txt

```
(venv) $ pip install -r requirements.txt
```
**Step 3. Setup Database and table**

Login to the PostgreSQL using below command, it'll ask your root passowrd

```
$ sudo -u postgres psql
```
Once the database is acessed, the name postgres will appear on left side of terminal. 

Run the below SQL command to create the table into the database
```
CREATE TABLE "SalesData" (
    "OrderId" VARCHAR(25) UNIQUE,
    "OrderItemId" BIGINT,
    "QuantityOrdered" BIGINT,
    "ItemPrice" DOUBLE PRECISION,
    "PromotionDiscount" JSONB, 
    "Region" CHAR(1),
    "TotalSales" DOUBLE PRECISION
);
```

Verify the newly created table schema by running below commands on terminal

- Connect to postgres database
```
postgres=# \c postgres
```

- View details of SalesData table
```
postgres=# \d+ "SalesData"
```

**Step 4. Run the python script**

If PostgreSQL is default configurations are not there on the machine, set the Database details into the connection string mentioned in the line 133 of python script.


```
(venv) $ python3 ProcessAndLoadData.py
```

# Future Enhancements
## Dockerization of application

In order to avoid issues with dependencies and platform compatibility, you can dockerize this project. Look into this [article on medium](https://stefanopassador.medium.com/docker-compose-with-python-and-posgresql-45c4c5174299)
