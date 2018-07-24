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

def main(conf_file="/home/werd/lbnl_summer/Influx_Dataframe_Client/measurement_details.ini"):
    # read arguments passed at .py file call
    parser = argparse.ArgumentParser()
    parser.add_argument("pickle", help="pickle file")

    args = parser.parse_args()
    pickle_file = args.pickle


    # read from config file
    conf_file = conf_file
    Config = configparser.ConfigParser()
    Config.read(conf_file)
    database = Config.get("measurement_details","database")
    measurement = Config.get("measurement_details","measurement")
    tags = Config.get("measurement_details", "tags")
    tags = tags.split(',')
    fields = Config.get("measurement_details", "fields")
    fields=fields.split(',')

    print(database)
    print(measurement)
    print(tags)
    print(fields)

    # import dataframe from pickle file
    whole_data = pd.read_pickle(pickle_file)
    data = whole_data.head()



    fields = ['Value']
    tags = ['Meter_Name']
    measurement = 'Building_Meter'

    # import dataframe from pickle file
    whole_data = pd.read_pickle(pickle_file)
    data = whole_data.head()

    #print(data)

    #remove all of the rows which have NaN
    #optional depending on if your data contains NaN
    data.dropna(inplace=True)



    # create client
    test_client = Influx_Dataframe_Client('/home/werd/lbnl_summer/Influx_Dataframe_Client/local_server.ini')


    test_client.write_data(data,tags,fields,measurement,database)


    test_client.list_DB()
    test_client.list_retention_policies()
    return

if __name__ == "__main__":
    main()
