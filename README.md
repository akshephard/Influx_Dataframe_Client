# Influx_Dataframe_Client
This project seeks to make an easy way to write and query an influxDB server where the input and output for writes/queries are
Pandas DataFrame

The user must specify a yaml config file in order to instantiate the object. An [example](https://github.com/akshephard/Influx_Dataframe_Client/blob/master/local_server.yaml) is included 
in the repo. Modify this file to fit your needs. It contains the settins required for connecting to a remote database and
query and write dataframes.

A pandas dataframe that contains the following data:
```
                       time              ap_name  AP_count             parse_ap_name building_number floor room  test_field
0 2016-04-01 07:00:00+00:00  ap135-100-103d-r177       1.0  [ap135, 100, 103d, r177]             100     1  03d         1.0
1 2016-04-01 07:00:00+00:00   ap135-100-121-r177       3.0   [ap135, 100, 121, r177]             100     1  121         1.0
2 2016-04-01 07:00:00+00:00   ap135-100-139-r177       6.0   [ap135, 100, 139, r177]             100     1  139         1.0
3 2016-04-01 07:00:00+00:00   ap135-100-140-r177       5.0   [ap135, 100, 140, r177]             100     1  140         1.0
4 2016-04-01 07:00:00+00:00  ap135-100-149b-r177       1.0  [ap135, 100, 149b, r177]             100     1  49b         1.0
```
The same dataframe can also be given as where the index is the time:
```
                           AP_count              ap_name building_number floor room  test_field
2016-04-01 07:00:00+00:00         1  ap135-100-103d-r177             100     1  03d           1
2016-04-01 07:00:00+00:00         5   ap135-100-150-r177             100     1  150           1
2016-04-01 07:00:00+00:00         3   ap135-100-121-r177             100     1  121           1
2016-04-01 07:00:00+00:00         5   ap135-100-140-r177             100     1  140           1
2016-04-01 07:00:00+00:00         1  ap135-100-149b-r177             100     1  49b           1
```

This wiill be converted to a list of JSON dictionaries which are formatted in the way that the `write_points()` function from the
influxDB python client expects JSON data.


```
[
  {
    'fields': {
        'AP_count': 1.0,
        'test_field': 1.0
        },
    'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
    'tags': {
        'floor': '1',
        'building_number': '100',
        'ap_name': 'ap135-100-103d-r177',
        'room': '03d'
        },
    'measurement': 'wifi_data9'
    },
  {
    'fields': {
        'AP_count': 3.0,
        'test_field': 1.0
        },
    'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
    'tags': {
        'floor': 1,
        'building_number': '100',
        'ap_name': 'ap135-100-121-r177',
        'room': '121'
        },
    'measurement': 'wifi_data9'
    },
  {
    'fields': {
        'AP_count': 6.0,
        'test_field': 1.0
        },
    'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
    'tags': {
        'floor': 1,
        'building_number': '100',
        'ap_name': 'ap135-100-139-r177',
        'room': '139'
        },
  'measurement': 'wifi_data9'
    },
  {
    'fields': {
        'AP_count': 5.0,
        'test_field': 1.0
        },
    'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
    'tags': {
        'floor': 1,
        'building_number': '100',
        'ap_name': 'ap135-100-140-r177',
        'room': '140'
        },
    'measurement': 'wifi_data9'},
  {
    'fields': {
        'AP_count': 1.0,
        'test_field': 1.0
        },
    'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
    'tags': {
        'floor': '1',
        'building_number': '100',
        'ap_name': 'ap135-100-149b-r177',
        'room': '49b'
        },
    'measurement': 'wifi_data9'
    }
 ]
```
