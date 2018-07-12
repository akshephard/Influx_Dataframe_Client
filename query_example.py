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




######################## MAIN ########################

def main():

    test_client = Influx_Dataframe_Client('/home/werd/lbnl_summer/wifi_data_push/wifi_scraping_config.ini')
    test_client.make_client()

    #df_result = test_client.query_data(query_string_test)
    #specific_query(self,database,field,measurement,tag,value):
    fields_list = ['AP_count']
    tags_list = ['building_number']
    values_list = ['67']
    database = 'lbnl_wifi_occ'
    measurement = 'wifi_data_correct'
    query_result = test_client.specific_query(database,measurement,fields=fields_list,tags=tags_list,values=values_list)

    print(query_result)

    return

if __name__ == "__main__":
    main()
