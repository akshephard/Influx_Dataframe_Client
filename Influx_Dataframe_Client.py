import configparser
import pandas as pd
from influxdb import InfluxDBClient
from influxdb import DataFrameClient

'''
When making queries, identifiers may be put into Double quotes depending on the
characters they contain. String literals i.e. tag values must be in single quotes!

class influxdb.InfluxDBClient(host=u'localhost',
 port=8086, username=u'root', password=u'root',
 database=None, ssl=False, verify_ssl=False,
 timeout=None, retries=3, use_udp=False,
 udp_port=4444, proxies=None)

class influxdb.DataFrameClient(host=u'localhost',
 port=8086, username=u'root', password=u'root',
 database=None, ssl=False, verify_ssl=False,
 timeout=None, retries=3, use_udp=False,
 udp_port=4444, proxies=None)

Take dataframe like the following example:
time                AP_count ap_name             building_number floor room
----                -------- -------             --------------- ----- ----
1459494000000000000 1        ap135-100-103d-r177 100             1     03d
1459494000000000000 1        ap135-100-149b-r177 100             1     49b
1459494000000000000 5        ap135-100-140-r177  100             1     140
1459494000000000000 6        ap135-100-139-r177  100             1     139
1459494000000000000 3        ap135-100-121-r177  100             1     121

Where AP_count is a field, ap_name, building_number, floor, and room are all tags
time is the timestamp associated with each row

Each columnn in dataframe grab column name first and parse name
add all points as a list of dictionaries of json
Each column of the dataframe is turned into a json dictionary and added to a list
of json dictionaries which can be given to InfluxDBClient

i.e.


            pushData = [
                    {
                        "measurement": measurement,
                        "tags": {
                            tags: current_ap_name,
                            "building_number": 90,
                            "floor": 2,
                            "room": 50
                        },
                        "time": pushTime,
                        "fields": {
                            fields: ap_value
                        }
                    },
                    {
                        "measurement": measurement,
                        "tags": {
                            tags: current_ap_name,
                            "building_number": 90,
                            "floor": 2,
                            "room": 50
                        },
                        "time": pushTime,
                        "fields": {
                            fields: ap_value
                        }
                    }
                ]

'''
def transform_to_dict(s, tags):
    #print(s)
    dic = {}
    for tag in tags:
        dic[tag] = s[tag]

    return dic



class Influx_Dataframe_Client(object):
    host = ""
    port = ""
    username = ""
    password = ""
    database = ""
    ssl= ""
    verify_ssl = ""
    client = None
    df_client = None
    data = None

    # The class "constructor" - It's actually an initializer
    def __init__(self, config_file):
        # read from config file
        Config = configparser.ConfigParser()
        Config.read(config_file)
        self.host = Config.get("DB_config", "host")
        self.username = Config.get("DB_config", "username")
        self.password = Config.get("DB_config", "password")
        self.database = Config.get("DB_config", "database")
        self.protocol = Config.get("DB_config", "protocol")
        #self.measurement = Config.get("DB_config","measurement")
        self.port = Config.get("DB_config", "port")
        self.use_ssl = Config.get("DB_config", "use_ssl")
        self.verify_ssl = Config.get("DB_config", "verify_ssl")
        print(self.use_ssl)
        print(self.verify_ssl)
        #self.tags = Config.get("wifi_metadata", "tags")
        #self.tags = self.tags.split(',')
        #self.fields = Config.get("wifi_metadata", "fields")
        #self.fields=self.fields.split(',')

    # setup client both InfluxDBClient and DataFrameClient
    # DataFrameClient is for queries and InfluxDBClient is for writes
    def make_client(self):

        self.client = InfluxDBClient(self.host, 8086, self.username, self.password, self.database,
                                self.use_ssl, self.verify_ssl)
        self.df_client = DataFrameClient(self.host, 8086, self.username, self.password, self.database,
                                self.use_ssl, self.verify_ssl)
        '''
        self.client = InfluxDBClient(self.host, 8086, self.username, self.password, self.database,
                                True, True)
        self.df_client = DataFrameClient(self.host, 8086, self.username, self.password, self.database,
                                True, True)
        '''

    def expose_influx_client(self):
        #Expose InfluxDBClient to user so they utilize all functions of InfluxDBClient
        return self.client

    def expose_data_client(self):
        #Expose DataFrameClient to user so they can utilize all functions of DataFrameClient
        return self.df_client

    def build_json(self,data, tags, fields, measurement):

        #print(data.head())
        data['measurement'] = measurement
        #print(data.head())
        data["tags"] = data.apply(transform_to_dict, tags=tags, axis=1)
        data["fields"] = data.apply(transform_to_dict, tags=fields, axis=1)
        #print( data[["measurement","time", "tags", "fields"]].head())
        #build a list of dictionaries containing json data to give to client
        #only take relevant columns from dataframe
        json = data[["measurement","time", "tags", "fields"]].to_dict("records")
        #print(json)
        #print(data.head())
        return json

    def post_to_DB(self,json):
        ret = self.client.write_points(json,batch_size=16384)
        return ret

    def write_data(self,data,tags,fields,measurement):
        json = self.build_json(data,tags,fields,measurement)
        self.post_to_DB(json)

    def list_DB(self):
        '''
        Returns a list of all the names of the databases on the influxDB server
        '''
        list_to_return = []
        DB_dict_list = self.client.get_list_database()

        for x in range(len(DB_dict_list)):
            list_to_return.append(DB_dict_list[x]['name'])

        return list_to_return

    def list_retention_policies(self):
        '''
        Returns a list of dictionaries with all the databases
        on the influxDB server and their associated retention policies
        '''
        DB_list = self.list_DB()
        dict_list = []
        for x in range(len(DB_list)):
            temp_dict = {}
            temp_dict[DB_list[x]] = self.client.get_list_retention_policies(DB_list[x])
            dict_list.append(temp_dict)
        return dict_list

    def query_data(self,query):
        df = self.df_client.query(query, database='wifi_data8',chunked=True, chunk_size=256)
        return df

    def query(self, query, use_database = None):
        query_result = self.client.query(query, use_database)
        return query_result

    def specific_query(self,database,measurement,fields=None,start_time=None,end_time=None,tags=None,values=None):
        '''
        This function returns a dataframe with the results of the specified query

        '''
        tag_string = ""
        time_string = ""
        df = {}
        #Create base query with fields and measurement
        query_string = "SELECT "
        if (fields == None):
            query_string = query_string + '* '
        else:
            for x in range(len(fields)):
                if (x > 0):
                    query_string = query_string + " ,"
                query_string = query_string + "\"" + fields[x] + "\""
        query_string = query_string + " FROM \"" + measurement + "\""

        #Create time portion of query if it is specified
        if (start_time != None or end_time != None ):
            if (start_time != None):
                #Must have a start_time for our query
                #Check to see format of time that was specified
                time_string = time_string + "time > "
                if(isinstance(start_time, str)): # Need quotes for date format
                    time_string = time_string + "\'" + start_time + '\''
                if(isinstance(start_time, int)): # No quotes for epoch time
                    time_string = time_string + str(start_time)

            if (end_time != None):
                #Must have a end_time for our query
                #Check to see format of time that was specified
                if (time_string != ""):
                    time_string = time_string + " AND "
                time_string = time_string + "time < "
                if(isinstance(start_time, str)): # Need quotes for date format
                    time_string = time_string + "\'" + end_time + '\''
                if(isinstance(start_time, int)): # No quotes for epoch time
                    time_string = time_string + str(end_time)

        #Create tag portion of query if it is specified
        if (tags != None and values != None):
            try:
                if (len(tags) != len(values)):
                    print("Tags and values do not match raise exception later!")
                    raise BaseException
                else:
                    tag_string = ""
                    for x in range(len(tags)):
                        if (x > 0):
                            tag_string = tag_string + ' AND '
                        tag_string = tag_string + '\"' + tags[x] + "\" = \'" + values[x] + "\'"
            except BaseException:
                print("Tags and values do not match")
                return pd.DataFrame()

        #Add optional parts of query
        if (time_string != "" or tag_string != ""):
            query_string = query_string + " WHERE "
            if (time_string != ""):
                query_string = query_string + time_string
            if (tag_string != ""):
                if (time_string != ""):
                    query_string = query_string + " AND "
                query_string = query_string + tag_string

        print(query_string)
        df = self.df_client.query(query_string, database=self.database,chunked=True, chunk_size=256)

        if (measurement in df):
            return df[measurement]
        else:
            #Must have an empty result make empty dataframe
            df = pd.DataFrame()
        return df
