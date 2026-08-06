import sys
import numpy as np
from collections import defaultdict
from itertools import combinations
from numpy.random import choice
import os
import pandas as pd
# import cx_Oracle as cx
import csv

from datetime import timedelta, time
from time import gmtime, localtime, strftime, sleep
import traceback
import yaml

    
def make_bidict(d: dict) -> dict:
    # Ensure values are unique (otherwise invert would overwrite keys)
    if len(set(d.values())) < len(d.values()):
        raise VlueError("Values are not tunique, can't invert safely")
    # Use Python 3.9 merge operator
    return d | {v:k for k,v in d.items()}
    
def print_syntax(code_str, lang='sql', style='colorful', show=True):
    if not show:
        return
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import HtmlFormatter
    from IPython.display import HTML, display
    """
    Print a string with syntax highlighting in Jupyter Notebook
    Parameters:
        code_str (str): The code to highlight.
        lang (str): The programming language ('sql','python','bash').
        style (str): Pygments style ('colorful', 'monokai', 'friendly').
    """
    lexer = get_lexer_by_name(lang)
    formatter = HtmlFormatter(style=style, noclasses=True)
    highlighted = highlight(code_str, lexer, formatter)
    display(HTML(highlighted))

def redux_perc(before_num,after_num,sig_digs=2):
    redux = 100*(before_num-after_num)/before_num
    return f"{round(redux,sig_digs)} %"
    
def datetime_converter(o):
    if isinstance(o, pd.Timestamp) or isinstance(o, datetime):
        return o.isoformat()
    return o

# Function to convert DataFrame to yaml-safe dictionary
def dataframe_to_yaml_safe_dict(df):
    # Converts a pandas DataFrame into a dictionary where datetime objects are 
    # ISO-formatted
    df_safe = df.copy()
    for col in df_safe.columns:
        if pd.api.types.is_datetime64_any_dtype(df_safe[col]):
            df_safe[col] = df_safe[col].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
    return df_safe.to_dict(orient='records')

def store_yaml(var,file_name,store_dir='./'):
    import pandas as pd; import yaml; import os;from datetime import datetime
    # Stores a pandas DataFrame as a yaml file.
    file_path = os.path.join(store_dir,file_name+'.yml')
    # Convert DataFrame to yaml-safe dictionary 
    data_dict = dataframe_to_yaml_safe_dict(var)
    
    # Write yaml safely
    with open(file_path, "w") as file:
        yaml.dump(data_dict,file,Dumper=yaml.SafeDumper,default_flow_style=False,sort_keys=False)
        

def load_yaml(file_name,load_dir='./'):
    import pandas as pd; import yaml; import os;from datetime import datetime
    file_path = os.path.join(load_dir,file_name+'.yml')
    # Load yaml safeley using SafeLoader
    with open(file_path,"r") as file:
        data = yaml.load(file,Loader=yaml.SafeLoader) # Explicitly use SafeLoader
    # Convert back to a DataFrame
    df = pd.DataFrame(data)
    # Convert any ISO strings back into datetime objects
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col],errors='ignore')
            except Exception as e:
                print(f"Could not convert column '{col}' to datetime: {e}")
    return df

def check_sqlalchemy_connection(engine):
    from sqlalchemy.engine import Engine
    if not isinstance(engine, Engine):
        raise TypeError(f"Expected SQLAlchemy Engine, got {type(engine)}.")
    print(" Valid SQLAlchemy Engine.")
    
# def store_feather(df,file_name,store_dir='./big_dfs',log=None):
#     import pandas as pd;import os
#     # Stores a pandas DataFrame as a feather file.
#     file_path = os.path.join(store_dir,file_name+'.feather')
#     if hasattr(df, "_to_pandas"):
#         df = df._to_pandas() # convert from Modin
#     print(f"Number of nulls: {df.isnull().sum().sum():,}")
#     # Write to feather which natively handles datetime
#     df.reset_index(drop=True)
#     df.to_feather(file_path)
#     if log:
#         log.info(f"Feather file saved {file_path}")
        

# def load_feather(file_name,load_dir='./big_dfs',log=None):
#     import pandas as pd, os
#     file_path = os.path.join(load_dir,file_name+'.feather')
#     df = pd.read_feather(file_path)
#     if log:
#         log.info(f"Feather file loaded {file_path}")

#     return df
def store_feather(df,file_name,store_dir='./big_dfs',show=True,log=None):
    import pandas as pd;import os
    import time; import datetime
    from time import gmtime, localtime, strftime, sleep, time
    starty = time()
    # Stores a pandas DataFrame as a feather file.
    file_path = os.path.join(store_dir,file_name+'.feather')
    if hasattr(df, "_to_pandas"):
        df = df._to_pandas() # convert from Modin
    # Write to feather which natively handles datetime
    df.reset_index(drop=True)
    df.to_feather(file_path)
    mem_before = df.memory_usage().sum() / (1024**2)
    if show:
        print(f" {file_name} Stored!!  - ({hms_string(time()-starty)} and {mem_before:,.3f} MB of memory)")
    if log:
        log.info(f"Feather file saved {file_path}")
        
def load_feather(file_name,load_dir='./big_dfs',show=True,log=None):
    import pandas as pd, os
    import time; import datetime
    from time import gmtime, localtime, strftime, sleep, time
    starty = time()
    file_path = os.path.join(load_dir,file_name+'.feather')
    df = pd.read_feather(file_path)
    mem_before = df.memory_usage().sum() / (1024**2)
    msg = f" {file_name} Loaded!!  - ({hms_string(time()-starty)} and {mem_before:,.3f} MB of memory)"
    if log:
        log.info(msg)
    if show:
        print(msg)
    return df
    
def run_pp():
    pp = "XXXXXXXXXX"
    return pp

def get_params():
    params_dict = { 'host':'XXXXXXXXXX',
                    'port':'XXXXXXXXXX',
                  'dbname':'XXXXXXXXXX',
                    'user':'XXXXXXXXXX',
                'password':run_pp()}
    return params_dict

def get_db_connection_info():
    """
    Returns both:
    - params: a dictionary for pycopg2.connect(**params)
    - conn_str: a SQLAlchemy-compatible connection string for Modin or SQLAlchemy
    """
    from urllib.parse import quote_plus
    params = { 'host':'XXXXXXXXXX',
                'port':'XXXXXXXXXX',
              'dbname':'XXXXXXXXXX',
                'user':'XXXXXXXXXX',
                'password':run_pp()}
    conn_str = (f"postgresl://{params['user']}:{quote_plus(params['password'])}"
                f"@{params['host']}:{params['port']}/{params['dbname']}")
    return params, conn_str
        
        
def hello_world():
	return("Hello WORLD!!")

def tyme(add = 3):
    # This returns EST time by default
    import datetime
    zone_time = (datetime.datetime.now()+timedelta(hours=add))
    return zone_time.strftime("%m/%d/%Y %H:%M:%S")

def tyme1():
    # This returns local time
    return strftime("%a, %d %b %Y %H:%M:%S %Z", localtime())

def tyme2():
    # This returns local time
    return strftime("%H:%M:%S %m/%d/%Y", localtime())



# def tymeout(add=3):
#     import datetime
#     zone_time = (datetime.datetime.now()+timedelta(hours=add))
#     return str(datetime.datetime.now().time()) + \
#         str(strftime(" (%Z) %a, %d %b %Y", localtime()))
def tymeout(add=3):
    #this returns EST time by default
    import datetime
    zone_time = (datetime.datetime.now()+timedelta(hours=add))
    continyoo = True
    if add == 0:
        local_zone = str(strftime("%Z", localtime()))
        time_out = str(datetime.datetime.now().time()) +  str(strftime(" (%Z) %a, %d %b %Y", localtime())) + "  hahahahahahaha"
        continyoo = False
    if continyoo:
        if add == 3:
            local_zone = 'EST'
        else:
            local_zone = str(strftime("%Z", localtime())) + '+{}'.format(add)
        time_out = str(zone_time.strftime("%H:%M:%S")) +  \
              str(zone_time.strftime(" ({}) %a, %d %b %Y").format(local_zone))
    return time_out

def hms_string(sec_elapsed):
    h = int(sec_elapsed / (60 * 60))
    m = int((sec_elapsed % (60 * 60)) / 60)
    s = sec_elapsed % 60.
    if h > 0:
        return_string = "{}:{:>02}:{:>05.2f} hours".format(h, m, s)
    elif m > 2:
        return_string = "{:>02}:{:>05.2f} minutes".format(m, s)
    else:
        return_string = "{:>05.2f} seconds".format(sec_elapsed)
    return return_string

# def time_start(process, iteration = None, data_file = None, show=True, log=None):
#     import time; import datetime
#     from colorama import Fore, Back, Style
#     from time import gmtime, localtime, strftime, sleep, time
#     start = time()
#     if show:
#         msg = ""
#         if iteration is not None and data_file is not None:
#             msg = f"Starting iteration {iteration} of {process} on '{data_file}' at {tymeout()}"
#         elif data_file is not None:
#             msg = f"Starting {process} on '{data_file}' at {tymeout()}"
#         else:
#             msg = f"Starting {process} at {tymeout()}"
#         print(Fore.LIGHTGREEN_EX + Style.BRIGHT + msg)
#     if log:
#         log.info(f"START:  {process}")
    
#     print(Style.RESET_ALL)
#     return start

# def time_stop(start,action = None,show=True,log=None):
#     import time; import datetime
#     from time import gmtime, localtime, strftime, sleep, time
#     from colorama import Fore, Back, Style
#     duration = time()-start
    
#     if action:
#         msg = f"     ...{action} complete. duration: {hms_string(duration)} at {tymeout()}\n"
#     else:
#         msg = f"     ...complete. duration: {hms_string(duration)} at {tymeout()}\n"
#     if show:
#         print(Fore.LIGHTRED_EX + Style.BRIGHT + msg)
#     if log:
#         log.info(f"{action} - Elapsed:  {hms_string(duration)}")
#     print(Style.RESET_ALL)
#     return duration
            
def time_start(process, nest=0,iteration = None, data_file = None, show=True, log=None):
    import time; import datetime
    from colorama import Fore, Back, Style
    from time import gmtime, localtime, strftime, sleep, time
    start = time()
    if show:
        msg ='_____'*nest
        if iteration is not None and data_file is not None:
            msg += f"Starting iteration {iteration} of {process} on '{data_file}' at {tymeout()}"
        elif data_file is not None:
            msg += f"Start {process} on '{data_file}' at {tymeout()}"
        else:
            msg += f"Start {process} at {tymeout()}"
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + msg + Style.RESET_ALL)
    if log:
        log.info(f"START:  {process}")
    return start
    
def time_stop(start,action = None,nest=0,show=True,log=None):
    import time; import datetime
    from time import gmtime, localtime, strftime, sleep, time
    from colorama import Fore, Back, Style
    duration = time()-start
    msg ='_____'*nest
    if action:
        msg += f"...{action} complete. duration: {hms_string(duration)} at {tymeout()}"
    else:
        msg += f"...complete. duration: {hms_string(duration)} at {tymeout()}"
    if show:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + msg + Style.RESET_ALL)
    if log:
        log.info(f"{action} - Elapsed:  {hms_string(duration)}")
    return duration
    
    
def store_json(var, file_name, store_dir = './',show=False):
    import json
    store_dir = os.path.expanduser(store_dir)
    os.makedirs(store_dir, exist_ok=True)
    fpath = os.path.join(store_dir, f"{file_name}.json")
    print(f"Saving {fpath}")
    json1 = json.dumps(var)
    with open(fpath, "w") as f1:
        f1.write(json1)
    if show:
        print(f"{fpath} Stored...")
    
def load_json(file_name, load_dir = './'):
    import json
    load_dir = os.path.expanduser(load_dir)
    fpath = os.path.join(load_dir, f"{file_name}.json")
    try:
        with open(fpath, "r") as f3:
            return json.load(f3)
    except:
        print(file_name,' there was a problem')
        with open(fpath,"r") as fl:
            return json.loads(fl.readline())

def store_sparse(var, file_name, store_dir = './'):
    from scipy import sparse
    sparse.save_npz("{}/{}.npz".format(store_dir,file_name), var)

def load_sparse(file_name, load_dir = './'):
    from scipy import sparse
    var = sparse.load_npz("{}/{}.npz".format(load_dir,file_name))
    return var

def store_pickle(var, file_name, store_dir = './'):
    import pickle
    with open("{}/{}.pik".format(store_dir,file_name),"wb") as file:
        pickle.dump(var, file, pickle.HIGHEST_PROTOCOL)

def load_pickle(file_name, load_dir = './'):
    import pickle
    with open("{}/{}.pik".format(load_dir,file_name),"rb") as file:
        var = pickle.load(file)
    return var

    
def table_to_csv(table_name, select = '*', schema = "XXXXXXXXXX",path ='./csv_files/'):
	## This function will convert a table in the USER's schema
	## into a csv file by bringing it into pandas.  It will retun a dataframe
	## and automatically write a csv file with the same name as the 
	## original table
	#conn = raw_input("Enter Oracle DB connection (uid/pwd@db) :")
	tns="(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(Host = XXXXXXXXXX)(Port = XXXXXXXXXX))\
	 (CONNECT_DATA = (SERVICE_NAME = XXXXXXXXXX)))"
	#connect to PDEA oracle database using your username and password
	orcl=cx.connect("XXXXXXXXXX",pp,tns)
	curs=orcl.cursor()
	printHeader=True
	sql="select {} from {}.".format(select,schema) +table_name
	print(sql)
	curs.execute(sql) # execute sql query 
	df=pd.read_sql(sql,orcl) # load into pandas df
	df.to_csv(path+table_name + '.csv',index = 'False', quoting = csv.QUOTE_MINIMAL)
	return df


def table_to_df(table_name, select = '*', more_sql = '', show=False):
    import psycopg2
    import pandas.io.sql as sqlio
    params_dict = get_params()
    ## This function will convert a table in the USER's schema
    ## into a dataframe by bringing it into pandas.  It will retun a dataframe.
    try:
        with psycopg2.connect(**params_dict) as conn:
            from colorama import Fore, Back, Style
            sql="SELECT {} FROM {} {};".format(select,'study_talent_net_shared.'+table_name, more_sql)
            if show:
                print_syntax(sql)
            df = pd.read_sql_query(sql,conn) # load into pandas df
            if show:
                print("table {} converted to DataFrame".format(table_name))
        return df
    except Exception as error:
        print("** --> Error finding {} or converting it to a DataFrame{}".\
              format(table_name,": {}".format(error) if show else "."))
        return None
    
def v_index(array_name, value):
    index = list(np.where(array_name == value)[0])[0]
    return index

def v_value(array_name, posit):
    value = list(array_name)[posit]
    return value

def update_finished(finished, store_dir = './'):
    store_pickle(finished,'finished',store_dir = store_dir)
    return

def check_finished(load_dir = './'):
    finished = load_pickle('finished',load_dir=load_dir)
    return finished

def zip_look(zipp):
    import zipcodes
    if 'X' in zipp:
        zipt = zipp.translate({ord(i): None for i in 'X'})
        zip_list = zipcodes.similar_to(zipt)
        out_str = "\tZIPCODE: {}".format(zipp)
        for area in zip_list:
            out_str += "\n\t\tnear zipcode {} --> {}, {}".\
            format(area['zip_code'],area['city'],area['state'])
    else:
        area = zipcodes.matching(zipp)[0]
        out_str = "\tZIPCODE: {} --> {}, {}".\
            format(area['zip_code'],area['city'],area['state'])
    return out_str

def zip_return(indexes, branch_dir = './output/ALL_PAX'):
    UIC_list = load_json('base_UICs_list', load_dir = branch_dir)
    UICs = np.load(branch_dir+'/base_UICs.npy')
    zip_dict_tup = load_pickle('zip_dict_tup', load_dir = branch_dir)
    len(UIC_list) 
    for index in indexes:
        print("*********** Adjacency Matrix index no. {} is UIC {}".format(index,UICs[index]))
        zip_sums = []
        for zip_type in zip_dict_tup[UICs[index]]:
            zip_sums.append(sum([freq for z,freq in zip_dict_tup[UICs[index]][zip_type]]))
        for zip_type in zip_dict_tup[UICs[index]]:
            zippy = zip_dict_tup[UICs[index]][zip_type][0]                    
            print("     {} {} x {} entries at {:.2f}% codes:".\
                  format(zip_type,zippy[0],zippy[1],100*zippy[1]/zip_sums[0]))
            if zippy[0] == 'None':
                print("                {}".format(zippy[0]))
            else:
                print(zip_look(zippy[0]))
    return


def list_to_sql(listy,alias=None):
    text = alias + str(listy[0])
    for element in listy[1:]:
        text += f',{alias}{str(element)}'
    return text

def col_list_to_sql(listy):
    text = listy[0]
    for element in listy[1:]:
        text += ',{}'.format(element)
    return text

def or_list_to_sql(prefix,listy):
    text = prefix + "'{}'".format(listy[0])
    for element in listy[1:]:
        text += " OR {}".format(prefix+"'{}'".format(element))
    return text

def DTS(dt):
    return str(dt).split('T')[0]

def plain_snap(time_stamp):
    return str(time_stamp).split('T')[0].split(' ')[0]

def dtg():
    tm = tyme()
    raw = tm.split(' ')
    return raw[0].split('/')[2]+raw[0].split('/')[1]+raw[0].split('/')[0]+'_'+tm.split(' ')[1]


# Look for junior and senior officers, and only grab their PID_PDEs
def nc_get_list_of_offcrs(pp, table_name,schema,load_dir,store_dir):
    value_field = 'RANK_GRP_PDE'
    values = ['OJ','OS']
    fields = ['PID_PDE']
    df_offcr_pids = nc_build_query_df(pp, table_name = table_name, schema = schema,\
                                      fields = fields, value_field = value_field, \
                               values = values, show = True)
    offcr_pid_list = list(df_offcr_pids.PID_PDE.unique())
    o_num = len(offcr_pid_list) 
    row_num = len(df_offcr_pids.index)
    print("number unique PID_PDEs: {:,}, number of dataframe records: {:,}, ratio: {:.2f}".\
          format(o_num, row_num,row_num/o_num))
    ## Now lets save the list of officer PID_PDEs as offcr_pid_list
    df_save = time_start('to save officer PID_PDE values list (offcr_pid_list)  \n')
    store_pickle(offcr_pid_list, 'offcr_pid_list', store_dir = store_dir)
    time_stop(df_save)
    return offcr_pid_list

def df_save(df_tosave,df_name,store_dir):
    import pickle
    start = time_start('saving dataframe to {}'.format(store_dir + '/'+ df_name +'.pkl'))
    df_tosave.to_pickle(store_dir + '/'+ df_name +'.pkl')
    time_stop(start)
    return

def df_load(df_toload, load_dir):
    import pickle
    address = load_dir + '/'+ df_toload +'.pkl'
    start = time_start('loading dataframe from {}'.format(address))
    loaded_df = pd.read_pickle(address)
    time_stop(start)
    return loaded_df

def get_snpsht_dates(store_dir='./chapter_folder', schema="XXXXXXXXXX",\
                     table='XXXXXXXXXX', field='snpsht_dt', show=True, \
                     strings=True, save=False, table_drop=True):
    print(f"store directory: {store_dir}, schema: {schema}, table: {table}, field: {field}, show?: {show}, strings?: {strings}, save?: {save}")
    ## This function reads in a table, and gives you a sorted list of all snapshot dates contained within the table, using
    # the default table name of MV_FOUO_UZ_MASTER_AD_ARMY_V3A and the default field of SNPSHT_DT
    suffix = 'str' if strings else 'dt64'
    store_name = 'snapshots_' + suffix
    import psycopg2
    with psycopg2.connect(**get_params()) as conn:
        curs = conn.cursor()
        try:
            if show:
                print(f"trying to DROP TABLE {store_name};")
            curs.execute(f"DROP TABLE {store_name};")

        except:
            if show:
                print(f"No previous {store_name} table as expected, executing ROLLBACK \n")
            curs.execute("ROLLBACK;")

    sql_start = time_start('Execute SQL Query')
    sql = f"CREATE TABLE {store_name} AS SELECT DISTINCT {field} FROM {schema}.{table} ORDER BY {field};"
    if show:
        print(sql)    
    with psycopg2.connect(**get_params()) as conn:
        curs = conn.cursor()
        curs.execute(sql) # execute sql query 
    time_stop(sql_start)

    ##  now load the table as a dataframe to get a list of PID_PDE's
    df_loading = time_start("to load the table as a dataframe to get a list of snapshot dates")
    try:
        df_snapshots = table_to_df(f'{store_name}')
    except:
        print("problem with table to df")
        curs.execute("ROLLBACK;")
        raise
    time_stop(df_loading)

    if table_drop:
        ## now drop the snapshots_{suffix} table
        if show:
            print(f"Dropping table {store_name}...")
        with psycopg2.connect(**get_params()) as conn:
            curs = conn.cursor()        
            curs.execute(f"DROP TABLE {store_name};")
    elif show:
        print(f"Table {store_name} remains in schema")
        
    # make a list of the snpsht_dt's and sort
    if show:
        print("Making a list of the snapshots from the working dataframe, sorting and returning")
    snapshots = sorted(list(df_snapshots.snpsht_dt.unique()))
    if strings:
        snapshots = [str(snap) for snap in snapshots]
    if save:
        save_snap = time_start(f'Saving list as {store_name}')
        if strings:
            store_json(snapshots,store_name,store_dir)
        else:
            store_pickle(snapshots,store_name,store_dir)
        time_stop(save_snap)
    return snapshots

def create_in_text_sql(in_list):
    return"{}".format(in_list).replace('[','(').replace(']',')')

def deidentify_pid_dict(pid_dict):
    work_dict = pid_dict.copy()
    pid_list = list(work_dict.keys())
    out_dict = {count:work_dict[pid] for count,pid in enumerate(pid_list)}
    return out_dict

def rank_val(grade_or_rank):
    grades = [1,2,3,4,5,6,7,8,9,10]
    ranks = ['2LT','1LT','CPT','MAJ','LTC','COL','BG','MG','LTG','GEN']
    rank_dict = {rank:grade for rank, grade in zip(ranks+grades,grades+ranks)}
    try:
        order = rank_dict[grade_or_rank]
    except:
        order = None
        print('not a valid grade or rank')
    return order

def rank_val_PDE(grade_or_rank):
    grades = [1,2,3,4,5]
    ranks = ['2LT','1LT','CPT','MAJ','OOO']
    rank_dict = {rank:grade for rank, grade in zip(ranks+grades,grades+ranks)}
    try:
        order = rank_dict[grade_or_rank]
    except:
        order = None
        print('{} of type {} is not a valid grade or rank'.format(grade_or_rank,type(grade_or_rank)))
    return order

def update_rank_tig(pid_list, rank, offcr_dictionary):
    # this function will input a list of pids, the main officer dictionary, (probably offcr_yg_), and a rank
    ## and put a key such as 'CPT_TIG_days' into the offcr_dict like 
    ## offcr_dict[pid]['CPT_TIG_days'] = xxxx
    wrkng_offcr_dict = offcr_dictionary.copy()
    # itianlize tracking lists
    found_pid_list = []; already_found_pid_list = []; pid_issue_list = []
    # determine the above and below ranks
    print("Rank: {}, Above Rank: {}".format(rank,rank_val_PDE(rank_val_PDE(rank)+1)))
    above_rank = rank_val_PDE(rank_val_PDE(rank)+1);below_rank = rank_val_PDE(rank_val_PDE(rank)-1);tgts = [below_rank,rank,above_rank]
#     print(tgts)
    # make a working copy of the input pid_list
    pid_list_work = pid_list.copy()
    # now remove the pids that already have tig entries for that grade 
    for pid in pid_list:
        issue = False
        if pid in wrkng_offcr_dict:
            if '{}_TIG_days'.format(rank) in wrkng_offcr_dict[pid]:
                already_found_pid_list.append(pid); pid_list_work.remove(pid)
            else:
                if len(list(set(tgts) & set(wrkng_offcr_dict[pid]['grades']))) == 3:
                    try:
                        tgt_rank_dt = max([dt for dt in wrkng_offcr_dict[pid]['grades'][rank]['PPLN_PGRD_EFF_DT'] if dt])
                        
                    except ValueError:
#                         print("ValueError with {} PPLN_PGRD_EFF_DT\n".format(rank),pid,tgts,wrkng_offcr_dict[pid]['grades'])
                        pid_issue_list.append((pid,'No rank dates for {}'.format(rank)))
                        issue = True
                    except TypeError:
#                         print("TypeError with {} PPLN_PGRD_EFF_DT\n".format(rank),pid,tgts,wrkng_offcr_dict[pid]['grades'])
                        pid_issue_list.append((pid,'TypeError PPLN_PGRD_EFF_DT for {}'.format(rank)))
                        issue = True
                    try:
                        above_rank_dt = min([dt for dt in wrkng_offcr_dict[pid]['grades'][above_rank]['PPLN_PGRD_EFF_DT'] if dt])
                    except TypeError:
#                         print("TypeError with {} PPLN_PGRD_EFF_DT\n".format(above_rank),pid,tgts,wrkng_offcr_dict[pid]['grades'])
                        pid_issue_list.append((pid,'TypeError PPLN_PGRD_EFF_DT for {}'.format(above_rank)))
                        issue = True
                    except ValueError:
#                         print("ValueError with {} PPLN_PGRD_EFF_DT\n".format(above_rank),pid,tgts,wrkng_offcr_dict[pid]['grades'])
                        pid_issue_list.append((pid,'No rank dates for {}'.format(above_rank)))
                        issue = True                 
                    tig = above_rank_dt - tgt_rank_dt
                    if tig != tig:
#                         print("PID: {} NaN promblem: {} date: {}, {} date: {}\n".format\
#                               (pid, rank, next_rank_dt, above_rank, tgt_rank_dt))
                        pid_issue_list.append((pid, "NaN date issue"))
                    else:
                        wrkng_offcr_dict[pid]['{}_TIG_days'.format(rank)] = tig.days
                        found_pid_list.append(pid); pid_list_work.remove(pid);issue = False

                else:
                    pid_issue_list.append((pid,"no bracket")); pid_list_work.remove(pid)
            if issue:
                pid_list_work.discard(pid)  
        else:
            pid_issue_list.append((pid,"pid not found")); pid_list_work.remove(pid)
    if len(pid_list_work) != 0:
        print("Counting ERROR - - {} PIDS unverified - See source code of update_rank_tig function".format(len(pid_list_work)))
    return wrkng_offcr_dict, found_pid_list, already_found_pid_list, pid_issue_list

def clean_list(list_in):
    list_in = list(list_in)
    return [x for x in list_in if x]


def combine_graphs_edges(Gw,H):
    for u,v,hdata in H.edges(data=True):
        attr = dict((key,value) for key,value in hdata.items())
        # get data from Gw or use empty dict if no edge in Gw
        gdata = G.get_edge_data(u,v,{})
        # add data from Gw
        # sum shared items
        shared = set(gdata) & set(attr)
#         print(set(gdata) , set(attr))
        attr.update(dict((key, attr[key] + gdata[key]) for key in shared if \
                         (type(attr[key]) == int or type(attr[key]) == float)))
        attr.update(dict((key, attr[key] + gdata[key]) for key in shared if key == 'unit_list'))
        
        # non shared items
        non_shared = set(gdata) - set(attr)
        attr.update(dict((key, gdata[key]) for key in non_shared))
        yield u,v,attr
    return

def append_the_graphs(G,H):
    Gw = G.copy()
    def combine_graphs_edges(Gw,H):
        for u,v,hdata in H.edges(data=True):
            attr = dict((key,value) for key,value in hdata.items())
            # get data from Gw or use empty dict if no edge in Gw
            gdata = G.get_edge_data(u,v,{})
            # add data from Gw
            # sum shared items
            shared = set(gdata) & set(attr)
    #         print(set(gdata) , set(attr))
            attr.update(dict((key, attr[key] + gdata[key]) for key in shared if \
                             (type(attr[key]) == int or type(attr[key]) == float)))
            attr.update(dict((key, attr[key] + gdata[key]) for key in shared if key == 'unit_list'))

            # non shared items
            non_shared = set(gdata) - set(attr)
            attr.update(dict((key, gdata[key]) for key in non_shared))
            yield u,v,attr
        return
    G.add_nodes_from(H.nodes(data=True))
    G.add_edges_from(list(combine_graphs_edges(Gw,H)))
    return G


def scrub_graph_for_dup_edges(G):
    Gw = G.copy()
    for u,v,edata in Gw.edges.data():
        for attr in edata:
            if attr == 'unit_list':
                Gw.edges[u,v][attr] = list(set(Gw.edges[u,v][attr]))
        Gw.edges[u,v]['weight'] = len(list(set(Gw.edges[u,v]['unit_list'])))*3
    return Gw
    
def rank_srt_func(rank_tup):
    rank_list_1 = ['PV1','PV2','PFC','SPC','CPL','SGT','SSG','SFC','EEE','WO1','CW2','CW3','WWW','2LT','1LT','CPT','MAJ','OOO']
    rank_list_2 = [1,2,3,4,4.5,5,6,7,8,11,12,13,14,21,22,23,24,25]
    rank_dict = dict(zip(rank_list_1,rank_list_2))
    return rank_dict[rank_tup[0]]

def rank_num_func(rank):
    rank_list_1 = ['PV1','PV2','PFC','SPC','CPL','SGT','SSG','SFC','EEE','WO1','CW2','CW3','WWW','2LT','1LT','CPT','MAJ','OOO']
    rank_list_2 = [1,2,3,4,4.5,5,6,7,8,11,12,13,14,21,22,23,24,25]
    rank_dict = dict(zip(rank_list_1,rank_list_2))
    if rank == None:
        return None
    else:
        return rank_dict[rank]
    

def optimize_dtypes(df,show=True):
    column_count = 0
    total_cols = len(df.columns)
    change_to_int_list = ['pn_age_qy']
    if show:
        mem_before = df.memory_usage().sum() / (1024**2)
        print(f"Current dataframe is using {mem_before:,.3f} MB of memory before optimization reduction.")
    for column in df.columns:
        column_count += 1
        # Check if the column is on the 'change to integer list'
        if column in change_to_int_list:
            if show:
                print(f"Changing column {column} to integer ('Int64'...")
            df[column] = df[column].astype('Int64') 
        
        # Check if the column is a datetime type
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            if show:
                print(f"Column {column_count} of {total_cols:,} -> {column} is a datetime64 timestamp.")
            continue # Skip this column if it is a datetime type
        #Check if the column is of object type
        elif df[column].dtype == 'object':
            num_unique_values = df[column].nunique()
            total_values = len(df[column])
            # If unique values are less than 50% of the total
            # Convert to 'category'
            if num_unique_values / total_values < 0.5:
                df[column] = df[column].astype('category')
                if show:
                    print("Column {} of {} -> {} coverted to category with {:,} unique values".\
                      format(column_count,total_cols,column,num_unique_values), tymeout())

    if show:
        mem_after = df.memory_usage().sum() / (1024**2)
        print(f"Current dataframe is using {mem_after:,.3f} MB of memory after optimization reduction.")
        print(f"for a reduction of {mem_before-mem_after:,.3f} MB ({(mem_before-mem_after)*100/mem_before:,.2f} %) ")
    return df

def categorize(df_input, tup):
    # === Convert object columns to categorical for memory efficiency ===
    mem_before = df_input.memory_usage().sum() / (1024**2)
    print(f"Current dataframe ({tup[3]}) is using {mem_before:,.3f} MB of memory before categorization reduction.")
    categories = [col for col in df_input.columns if df_input[col].dtype == 'object']
    print(f"There are {len(categories):,} object columns that are being reduced to categorical for {tup[3]}.")
    print(f"Columns: {categories}")
    if not df_input.empty and categories:
        cat_start = time_start(f"Convert {tup[3]} object fields to categorical")
        for col in categories:
            df_input[col] = df_input[col].astype('category').cat.add_categories('NA')
        time_stop(cat_start,action=f"Categorical conversion of {tup[3]}")
    mem_after = df_input.memory_usage().sum() / (1024**2)
    print(f"Current dataframe ({tup[3]}) is using {mem_after:,.3f} MB of memory after categorization reduction.")
    print(f"for a reduction of {mem_before-mem_after:,.3f} MB ({(mem_before-mem_after)*100/mem_before:,.2f}) %")
    return df_input

def reduce_floats(df_big_work,tup):
    # === Convert float64 columns to float32 to save memory ===
    if df_big_work.empty:
        print(f"Skipping float reduction for {tup[3]} - DataFrame is empty.")
        return df_big_work
    mem_before = df_big_work.memory_usage().sum() / (1024**2)
    print(f"Current dataframe ({tup[3]}) is using {mem_before:,.3f} MB of memory before floating point reduction.")
    floats = df_big_work.select_dtypes(include=['float64']).columns.tolist()
    if not floats:
        print(f"No float64 columns found in {tup[3]}, skipping float conversion.")
        return df_big_work
    print(f"There are {len(floats):,} float64 columns that are being reduced to float32 for {tup[3]}.")
    float_start = time_start(f"Convert {table_name} columns to float32")
    df_big_work[floats] = df_big_work[floats].astype('float32')
    time_stop(float_start,action=f"Float conversion of {tup[3]}")
    mem_after = df_big_work.memory_usage().sum() / (1024**2)
    print(f"Current dataframe ({tup[3]}) is using {mem_after:,.3f} MB of memory after floating point reduction.")
    print(f"for a reduction of {mem_before-mem_after:,.3f} MB ({(mem_before-mem_after)*100/mem_before:,.2f}) %")
    return df_big_work
        
def convert_all_nulls_to_str(df, null_entry="NA"):
    return df.fillna(null_entry)
   
def hw():
    print_syntax("CREATE TABLE hello_world")

def run_sql_script(filename,show=True,log=None,sql_dir='./sql_scripts'):
    """
    Runs a .sql script using psycopG directly. Supports multi-statement SQL scripts.
    """
    import os, psycopg2
    from psycopg2 import OperationalError
    from colorama import Fore, Back, Style
    
    # Build full path
    file_path = os.path.join(sql_dir, filename)
    if not os.path.exists(file_path):
        print(f"{Fore.RED}SQL file not found: {file_path}{Style.RESET_ALL}")
        return
    # Open and read the SQL file
    with open(file_path, 'r') as file:
        sql_script = file.read()
    if show:
        print(f"{Fore.GREEN}Running SQL script: {filename}{Style.RESET_ALL}")
    if show:
        print_syntax(sql_script)
    conn = None

    # Connect to your PostgreSQL database
    try:
        conn = psycopg2.connect(**get_params())
        conn.autocommit = False  # Ensure changes are committed only after all commands execute
        # Execute the SQL script
        with conn.cursor() as curs:
            curs.execute(sql_script)
        # Commit the transaction
        conn.commit()
        print(f"{Fore.GREEN}Script executed successfully: {filename}{Style.RESET_ALL}")
        if log:
            log.info(f"Script executed successfully: {filename}")
    except (Exception, OperationalError) as error:
        print(f"{Fore.RED}SError executing SQL script {filename}: {error}{Style.RESET_ALL}")
        if conn:
            conn.rollback()  # Roll back the transaction on error
    finally:
        if conn:
            conn.close()

def get_uic_hierarchy_tables(engine, schema='XXXXXXXXXX',prefix='XXXXXXXXXX'):
    from sqlalchemy import create_engine, text
    query = text(f"""
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = :schema
        AND table_name LIKE :prefix
        AND table_type = 'BASE TABLE'
    ORDER BY table_name;
    """)
    with engine.begin() as conn:
        result = conn.execute(query,{"schema": schema, "prefix": f"{prefix}%"})
        table_names = [row[0] for row in result]
    return table_names


def add_fy_col(df_input, date_column = 'snpsht_dt', show=True, log=None):
    import pandas as pd
    """
    Adds a 'fy' column to the DataFrame that represents the DoD fiscal year.
    Parameters:
        df_input(pd.DataFrame): the input DataFrame with a datetime column.
        date_column(str): The name of the datetime column to convert to fiscal year
    Returns:
    pd.DataFrame: a new df with the added 'fy' column
    """
    df_out = df_input.copy()
    df_out[date_column] = pd.to_datetime(df_out[date_column], errors='coerce')
    if not pd.api.types.is_datetime64_any_dtype(df_out[date_column]):
        raise TypeError(f"Column {date_column} could not be converted to datetime.")
    try:
        df_out['fy'] = df_out[date_column].dt.year + \
            (df_out[date_column].dt.month >= 10).astype(int)
        msg = f"Added 'fy' column based on {date_column}"
        if show:
            print(msg)
        if log:
            log.info(msg)
    except Exception as e:
        err_msg = f"Failed to add 'fy' column using {date_column}: {e}"
        if show:
            print(err_msg)
        if log:
            log.info(err_msg)
    return df_out

def add_dor_col(df_in, nest=0,rank_list = ['CPT','MAJ']):
    t0=time_start(f"Add date of rank (dor) for {rank_list}", nest)
    df = df_in.copy()
    dfw = df[['pid_pde','snpsht_dt','rank_pde','ppln_pgrd_eff_dt']].copy()
    
    dfw = dfw.sort_values(by=["pid_pde", "snpsht_dt"])
    
    for rank in rank_list:
        dor_col = f"dor_{rank.lower()}"
        
        if dor_col not in df.columns:
            t1act = f"Adding {dor_col}..."
            t1=time_start(t1act,nest=nest+1)
            
            rank_dates = (
                dfw[dfw["rank_pde"] == rank]
                    .groupby("pid_pde")
                    .first()["ppln_pgrd_eff_dt"]
            )
            df[dor_col] = df["pid_pde"].map(rank_dates)
            time_stop(t1,nest=nest+1)
        else:
            print(f"Date of rank column {dor_col} is already in DataFrame")
    time_stop(t0,nest=nest)
    return df
    
def move_column_after(df, move_column, target_column):
    cols = df.columns.tolist()
    cols.remove(move_column)
    target_idx = cols.index(target_column)
    cols.insert(target_idx+1,move_column)
    return df[cols]
    
def get_fy(date_in):
    try:
        date_ts = pd.to_datetime(date_in)
        fy = date_ts.year + 1 if date_ts.month>= 10 else date_ts.year
        return fy
    except Exception as e:
        return f"Error processing {date_in}: {e}"
    
def fast_copy(df, table_name, schema='XXXXXXXXXX', nest=0):
    import psycopg2
    from io import StringIO
    actfscp = time_start(f"Pushing DataFrame to {schema}.{table_name}.")
    fscp = time_start(actfscp,nest = nest+1,show=True)
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    conn = psycopg2.connect(**get_params())
    with conn.cursor() as cursor:
        cursor.copy_expert(f"COPY {schema}.{table_name} FROM STDIN WITH CSV", buffer)
        conn.commit()
    conn.close()
    time_stop(fscp,action=actfscp,nest=nest+1)

def plot_promos_snap_idx(df_in,min_promos, min_label,top_num=3,date_ticks=True):
    import pandas as pd
    import seaborn as sns
    from matplotlib import pyplot as plt
    snap_dict = load_pickle('snap_dict_506','./running_vars')
    df = df_in.copy()
    # --- a. Create the bar plot using sns.barplot()
    sns.set_theme(style='whitegrid')
    figsize = (10,5)
    # Start the graph with a minimum CPT count of 200
    min_idx = df[df.new_captains_num > min_promos].iloc[0]['snap_idx']
    min_snpsht_dt = plain_snap(snap_dict[min_idx])
    df_cut = df[df.snap_idx >= min_idx]
    plt.figure(figsize = figsize)
    ax=sns.barplot(x='snap_idx', y='new_captains_num',
                   data =df_cut, palette='viridis',
                   hue='new_captains_num',legend=False)
    ax.set_xlabel('Quarters',fontsize=14)
    ax.set_ylabel('Officers Promoted',fontsize=14)
    ax.set_title(f"Officers Promoted to Captain by Quarter\n(Date > {min_snpsht_dt})",fontsize=18)
    
    tick_locations = []; tick_labels = []; bar_labels = []
    for idx, row in df_cut.iterrows():
        tick_locations.append(idx-min_idx+1)
        if row['new_captains_num'] > min_label:
            if date_ticks:
                tick_labels.append(plain_snap(snap_dict[row['snap_idx']]))
            else:
                tick_labels.append(plain_snap(row['snap_idx']))
            bar_labels.append(row['new_captains_num'])
        else:
            tick_labels.append('')
            bar_labels.append('')
    # display(bar_labels)
    for container in ax.containers:
        for bar in container:
            if bar.get_height() > min_label:
                ax.bar_label(container,fontsize=10,fmt='{:,.0f}')
    ax.set_xticks(tick_locations)
    ax.set_xticklabels(tick_labels,rotation=45, ha='right',fontsize=10)
    
    plt.show()
    top_cpt_idxs = df_cut.sort_values('new_captains_num',ascending=False).head(top_num)['snap_idx'].tolist()
    display(f"The Top {top_num} Snapshot indexes for Captain Promotions:",top_cpt_idxs)
    return top_cpt_idxs
    
def check_table(table_name,show=True,engine=None):
    # Create engine if not provided
    if engine is None:
        from sqlalchemy import create_engine, text
        from urllib.parse import quote_plus
        pp = run_pp()
        safe_pw = quote_plus(pp)
        params_dict = get_params()
        conn_str = f"postgresql://{params_dict['user']}:{safe_pw}@{params_dict['host']}:{params_dict['port']}/{params_dict['dbname']}"
        engine = create_engine(conn_str)
    
    with engine.connect() as conn:
        from sqlalchemy import text
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        row_count = result.scalar()
        if show:
            print(f"Table {table_name} is accessible and has {row_count:,} rows.")
    return row_count

def check_column_completeness(df, column_name, show=True):
    """
    Check the completeness of a column in a DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        The DataFrame to check
    column_name : str
        Name of the column to check
    show : bool, default True
        Whether to print the results
    
    Returns:
    --------
    dict : Dictionary with counts and percentages
        - 'total_rows': Total number of rows
        - 'non_null_count': Number of non-null values
        - 'null_count': Number of null values (NaN, NaT, etc.)
        - 'non_null_pct': Percentage of non-null values
        - 'null_pct': Percentage of null values
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame. Available columns: {list(df.columns)}")
    
    total_rows = len(df)
    non_null_count = df[column_name].notna().sum()
    null_count = df[column_name].isna().sum()
    
    non_null_pct = (non_null_count / total_rows * 100) if total_rows > 0 else 0
    null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0
    
    results = {
        'total_rows': total_rows,
        'non_null_count': non_null_count,
        'null_count': null_count,
        'non_null_pct': non_null_pct,
        'null_pct': null_pct
    }
    
    if show:
        print(f"\n📊 Column Completeness Check: '{column_name}'")
        print(f"   Total rows: {total_rows:,}")
        print(f"   Non-null values: {non_null_count:,} ({non_null_pct:.2f}%)")
        print(f"   Null values (NaN/NaT/etc.): {null_count:,} ({null_pct:.2f}%)")
    
    return results
    
def table_into_df(table_name,nest,modin=True,show=True):
    # === Load the table into DataFrame ===
    row_count = check_table(table_name,show=show)
    action_p = (f"Reading the new table '{table_name}' with {row_count:,} rows into pandas DataFrame.")
    pandy = time_start(action_p,nest=nest+1,show=show)
    try:
        if modin:
            init_ray_cluster()
            import modin.pandas as mpd
            engine = create_engine(conn_str)
            df = mpd.read_sql(F"SELECT * FROM {table_name}",engine)
            import pandas as pd
            df_out = df._to_pandas()
            del df
            ray_cleanup()
            ray.shutdown()
            
        else:
            import pandas as pd
            engine = create_engine(conn_str)
            df_out = pd.read_sql(F"SELECT * FROM {table_name}",engine)
        time_stop(pandy,action = f"To read {row_count:,} rows..",nest=nest+1,show=show)
        return df_out

    except Exception as e:
        time_stop(pandy,action = f"To read {row_count:,} rows..")
        print(f"Failed to read {table_name}: {e}")

def cut_pids(df_in,cut_pid_list):
    df_out = df_in[~df_in['pid_pde'].isin(cut_pid_list)]
    return df_out

def create_df_final_uic_lookup(final_lu_table = 'final_uic_lookup', show=True):
    # WE rebuilt the UIC lookup DataFrame to include pid_pde (df_final_uic_lookup)!
    # Load it and add an 'fy' columns
    if 'df_ful' not in globals():
        print(f"DatFrame 'df_ful' is not present in globals()")
        ll = time_start("Load final_uic_lookup TABLE to DataFrame as df_ful..")
        df_ful = table_to_df('final_uic_lookup')
        time_stop(ll)
        if 'fy' not in df_ful.columns:
            print(f"Column 'fy' is not present in 'df_ful'")
            # Add an 'fy' column
            adfy = time_start("Add an 'fy column to df_ful DataFrame")
            df_ful = add_fy_col(df_ful)
            time_stop(adfy)
    # Now let's get the min and max snapshots
    df_ful_min_ssd = df_ful.snpsht_dt.min()
    df_ful_max_ssd = df_ful.snpsht_dt.max()
    if show:
        print(f'For the final UIC lookup DataFrame, \nMIN snapshot date: {df_ful_min_ssd}, MAX snapshot date: {df_ful_max_ssd}')
    return df_ful

def ray_cleanup(object_refs: list = None, verbose: bool = True):
    """
    Frees Ray object references and runs garbage collection.
    Does NOT shut down or re-sart Ray.
    Safe to use between pipeline steps if Ray session should
    rmeain alive.
    """
    import ray, gc
    if object_refs:
        for ref in object_refs:
            try:
                ray.internal.free(ref)
                if verbose:
                    print(f"Freed Ray object: {ref}")
            except Exception as e:
                if verbose:
                    print(f"Ray cleanup failed for object: {e}")
    if verbose:
        print("Running garbage collection...")
        gc.collect()
    if verbose:
        print("Memory cleanup complete.") 
        
        
def main(argv):
	
	
	return

if __name__ == '__main__':
	main(sys.argv)	