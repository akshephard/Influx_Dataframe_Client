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
import ast


from Influx_Dataframe_Client import Influx_Dataframe_Client
#To run this script clone the repo and use the command: python3 demo.py conf.ini


######################## MAIN ########################

def main():
    # read arguments passed at .py file call
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Need to specify config file, see example_server.ini")


    args = parser.parse_args()
    conf_file = args.config

    tags_list = ["ap_name","building_number","floor","room"]
    fields_list = ["AP_count","test_field"]
    database='pyTestDB'
    measurement='wifi_measurement'

    #make a single json dictionary in the format that InfluxDBClient expects
    json =   {
        'fields': {
            'AP_count': 1.0,
            'test_field': 1.0
            },
        'time': '2016-04-01 07:00:00+0000',
        'tags': {
            'floor': '1',
            'building_number': '100',
            'ap_name': 'ap135-100-103d-r177',
            'room': '03d'
            },
        'measurement': 'wifi_data9'
        }

    #take in csv file
    data = pd.read_csv('example.csv')
    print(data)


    # create client
    test_client = Influx_Dataframe_Client(conf_file)

    #demo all ways to write data into database using client

    test_client.write_csv('example.csv',tags_list,fields_list,measurement,database)
    test_client.write_json(json,database)
    test_client.write_dataframe(data,tags_list,fields_list,measurement,database)


    fields_list = ['AP_count']
    tags_list = ['building_number','floor']
    values_list = ['100','1']

    '''
    query below is equal to:
    SELECT *  FROM "wifi_measurement" WHERE time > '2016-03-01 06:00:00' AND time < '2016-04-02 08:00:00' AND "building_number" = '100' AND "floor" = '1'
    '''
    query_result = test_client.specific_query(database,measurement,start_time='2016-03-01 06:00:00', end_time='2016-04-02 08:00:00',tags=tags_list,values=values_list)

    #query below is equal to: Select * from MEASUREMENT_ARGUMENT using DATABASE_ARGUMENT
    query_result2 = test_client.specific_query(database,measurement)
    print(query_result)
    print(query_result2)

    return

if __name__ == "__main__":
    main()
