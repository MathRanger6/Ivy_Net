# === 0.1. LIBRARY IMPORTS ===
from functionsG import *

# Import necessary libraries
import modin.pandas as pd
import ray
from datetime import datetime, timedelta

# === 0.2. DATABASE CONNECTION ===
# === Ray/Modin Environment Variables ===
from init_ray_cluster import init_ray_cluster
init_ray_cluster()

# === Secure PostgreSQL Connection String and Create Engine ===
from sqlalchemy import create_engine, text
pp = run_pp()
from urllib.parse import quote_plus
safe_pw = quote_plus(pp)
params_dict = get_params()
conn_str = f"postgresql+psycopg2://an_levinec:{safe_pw}@cpdea-prod.cyrne4ul6ab8.us-gov-west-1.rds.amazonaws.com:5432/cpdeaprod"

#  === Create SQLAlchemy Engine ---
engine = create_engine(conn_str)
check_sqlalchemy_connection(engine)

# === 0.0 SET VARIABLE VALUES ===
table_schema = 'study_talent_net' # local schema since its no longer my default
var_dir = './running_vars'  # Directory for saved variables

# === 1.1. PREPARE SELECT CLAUSE ===
# Load columns to remove
master_remove_cols = load_json('master_remove_cols',var_dir)

# Get all column names from the csource table
query_all_columns = f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{table_schema}' AND table_name = '{table_name}';"
all_columns_df = pd.read_sql_query(query_all_columns, con=engine)
all_table_columns = all_columns_df['columns_name'].tolist()

# Filter out the remove columns
columns_to select = [col for col in all_table_columns if col not in master_remove_cols]

# Build SELECT clause
select_clause = ", ".join(columns_to_select)

sql_query = f"SELECT {select_clause} FROM {table_schema}.{table_name};"
# === 1.2 LOAD TABLE as df_master_pde ===

# === 1.3 LOAD TABLE as df_master ===
# Strip '_pde' from uic column names
keep_cols = [col if 'uic' not in col else col.replace('_pde','') for col in keep_cols]
