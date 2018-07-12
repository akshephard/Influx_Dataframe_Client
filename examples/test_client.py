import time
import json
import pandas as pd
import math
from influxdb import InfluxDBClient
from influxdb import DataFrameClient
from datetime import datetime, timedelta
from pytz import timezone
import datetime######################## MAIN ########################
import pytz
import hashlib
import argparse
import configparser
import subprocess
import numpy as np
from datetime import datetime
from tabulate import tabulate
import os
import sys


from Influx_Dataframe_Client import Influx_Dataframe_Client


def time_transform(timestamp):

    d = timestamp.to_pydatetime()
    #print(d.strftime('%Y-%m-%dT%H:%M:%SZ'))
    localtz = timezone('US/Pacific')
    d = localtz.localize(d)
    d = d.astimezone(timezone('UTC'))
    return d


def parse_ap(s):
    return s.split('-')

def get_building(s):
    return s[1]

def get_floor(s):
    x=0
    if (len(s[2]) > 3):
        while(len(s[2]) > x and s[2][x].isalpha()):
            if(x == (len(s[2]) -1)):
                return 99
            else:
                x += 1
        return s[2][x]
    else:
        return 1

def get_room(s):
    x=0
    if (len(s[2]) > 3):
        while(len(s[2]) > x and s[2][x].isalpha()):
            if(x == (len(s[2]) -1)):
                return 99
            else:
                x += 1
        x += 1
        return s[2][x:]
    else:
        return s[2]




######################## MAIN ########################

def main(conf_file="/home/werd/lbnl_summer/wifi_data_push/wifi_local_config.ini"):
    # read arguments passed at .py file call
    parser = argparse.ArgumentParser()
    parser.add_argument("pickle", help="pickle file")

    args = parser.parse_args()
    pickle_file = args.pickle


    # read from config file
    conf_file = conf_file
    Config = configparser.ConfigParser()
    Config.read(conf_file)

    measurement = Config.get("DB_config","measurement")
    tags = Config.get("wifi_metadata", "tags")
    tags = tags.split(',')
    fields = Config.get("wifi_metadata", "fields")
    fields=fields.split(',')



    # get and summarize wifi data
    data = pd.read_pickle(pickle_file)

    #get dataframe in right format before creating json
    #puts all of the columns associated with a timestamp together
    data = data.stack()
    data = data.reset_index()

    #change time in correct format
    #time_transform changes from x to Unix Epoch time
    #time can also be in x format, make sure that final datatype is string or int
    data.iloc[:,0] = data.iloc[:,0].head().apply(time_transform)

    #rename columns so that the proper keys will appear in the json list
    #containing all the individual measurement, also make sure time is int not float
    data.columns = ['time', 'ap_name', 'AP_count']
    #print(data.head())
    data['parse_ap_name'] = data.iloc[:,1].head().apply(parse_ap)
    data['building_number'] = data['parse_ap_name'].head().apply(get_building)
    data['floor'] = data['parse_ap_name'].head().apply(get_floor)
    data['room'] = data['parse_ap_name'].head().apply(get_room)
    data['test_field'] = 1.0


    print(data.head())
    #remove all of the rows which have NaN
    #optional depending on if your data contains NaN
    data.dropna(inplace=True)

    query_string = 'SHOW DATABASES'
    query_string_data =  'SELECT * FROM wifi_data8'


    # create client
    test_client = Influx_Dataframe_Client('/home/werd/lbnl_summer/wifi_data_push/wifi_local_config.ini')
    test_client.make_client()
    #print(measurement)
    test_client.write_data(data.head(),tags,fields,measurement)
    test_result = test_client.query(query_string,None)
    #df_result = test_client.query_data(query_string_test)
    #specific_query(self,database,field,measurement,tag,value):
    fields_list = ['AP_count','test_field']
    tags_list = ['building_number','floor']
    values_list = ['100','1']
    #values_list = ['100']
    #example queries with both time formats one in strong and the other in epoch
    #if the fields parameter is left out it defaults to the following:
    # SELECT * FROM measurement_name
    query_result = test_client.specific_query('wifi_data9',measurement,fields=fields_list,start_time=1459493000000000000, end_time=1459495000000000000,tags=tags_list,values=values_list)
    query_result2 = test_client.specific_query('wifi_data9',measurement,start_time='2016-03-01 06:00:00', end_time='2016-04-02 08:00:00',tags=tags_list,values=values_list)

    print(query_result)
    print(query_result2)

    test_client.list_DB()
    test_client.list_retention_policies()

    return

if __name__ == "__main__":
    main()
