import pandas as pd
from sqlalchemy import create_engine
from io import StringIO
import csv
import psycopg2
import sys

def read_excel_data(filename):
  """
  This function is to read the data from excel file
  
  Args:
      filename (str): Path to the Excel file.
  
  Returns:
      pandas.DataFrame: The loaded data.
  """
  try:
    dataframe = pd.read_excel(filename)
    return dataframe
  except Exception as e:
    print(f"FATAL: Error reading Excel file: {e}")
    sys.exit(1)

def add_region(df, region):
  """
  This function is to add region column into the dataframe
  
  Args:
      df (pandas.DataFrame): The input dataframe.
      region (str): The region to add.
  
  Returns:
      pandas.DataFrame: The dataframe with the added region column.
  """
  try:
    df['Region'] = region
    return df
  except Exception as e:
    print(f"FATAL: Error adding region column: {e}")
    sys.exit(1)


def apply_business_rules(region_a_dataframe, region_b_dataframe):
  """
  This function will apply below listed buiness rules on the data
  1. Add region column to identify the region of sales record (A/B).
  2. Combine the data from both regions into a single table.
  3. Add a column total_sales which is calculated as QuantityOrdered * ItemPrice. 
  4. Ensure that there are no duplicate entries based on OrderId. 

  Args:
      region_a_dataframe (dataframe) : Dataframe for region A
      region_b_dataframe (dataframe) : Dataframe for region B

  Returns:
      processed dataframe
  """
  try:
    # Adding region column to identify the region of sales record
    region_a_df_updated = add_region(region_a_dataframe, 'A')
    region_b_df_updated = add_region(region_b_dataframe, 'B')
    print("INFO: Added region column in both dataframes")

    # Combining the data from both regions into a single table
    result = pd.concat([region_a_df_updated, region_b_df_updated])
    print("INFO: Combined region A and region B data into one dataframe")

    # Removed duplicate entries based on 'OrderId'
    # With assumption of keeping first record
    result.drop_duplicates(subset=['OrderId'], inplace=True)
    print("INFO: Removed duplicate rows based on 'OrderId' column")

    # Adding a column TotalSales which is calculated as QuantityOrdered * ItemPrice
    result['TotalSales'] = result['QuantityOrdered'] * result['ItemPrice']
    print("INFO: Added 'TotalSales' column")
    return result
  except Exception as e:
    print(f"FATAL: Error applying business rules: {e}")
    sys.exit(1)


def psql_insert_copy(table, conn, keys, data_iter):
  """
  Executes SQL statement inserting data using COPY for efficiency.

  Args:
    table (sqlalchemy.Table): The table object representing the target table.
    conn (sqlalchemy.engine.Engine): The SQLAlchemy engine connection.
    keys (list): List of column names for the data.
    data_iter (iterable): An iterable object yielding data rows.

  Raises:
    psycopg2.Error: If any error occurs during the COPY operation.
  """
  try:
    # Get DBAPI connection and cursor
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:

      # Prepare data buffer and writer
      s_buf = StringIO()
      writer = csv.writer(s_buf)
      writer.writerows(data_iter)
      s_buf.seek(0)

      # Build column list and table name
      columns = ', '.join('"{}"'.format(k) for k in keys)
      table_name = f"{table.schema}.{table.name}" if table.schema else table.name

      # Construct COPY statement
      sql = f'COPY {table_name} ({columns}) FROM STDIN WITH CSV'

      # Execute COPY operation
      cur.copy_expert(sql=sql, file=s_buf)

  except psycopg2.Error as err:
    # Handle potential errors during COPY
    print(f"FATAL: Error during COPY operation: {err}")
    sys.exit(1)


def load_data(filename):
  """
  This function will load the data into database
  args:
      filename (final csv file)
  """
  try:
    df = pd.read_csv(filename)  # read csv file from your local

    # Example: 'postgresql://username:password@localhost:5432/your_database'
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

    df.to_sql(
        name="SalesData",
        con=engine,
        if_exists="replace",
        index=False,
        method=psql_insert_copy
    )
    print("INFO: Data loaded successfully")
  except Exception as e:
    print(f"FATAL: Error loading data: {e}")
    sys.exit(1)

def main():
  # Read region A order data
  region_a_df = read_excel_data('order_region_a.xlsx')
  # Read region B order data
  region_b_df = read_excel_data('order_region_b.xlsx')

  # Applying business rules
  final_dataframe = apply_business_rules(region_a_df, region_b_df)
  #final_dataframe.drop(final_dataframe.columns[0],axis=1,inplace=True)
  #print("Final df {}".format(final_dataframe.columns))

  filename = "finalSales.csv"
  final_dataframe.to_csv(filename, index=False)

  load_data(filename)

  print("INFO: Final Sales data loaded into sales_data table")

if __name__ == "__main__":
  main()
