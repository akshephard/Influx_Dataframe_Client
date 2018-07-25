# Influx_Dataframe_Client
This project seeks to make an easy way to write and query an influxDB server where the input and output for writes/queries are
Pandas DataFrame

The user must specify a config file in order to instantiate the object. An example() is included in the repo.

`
                       time              ap_name  AP_count             parse_ap_name
0 2016-04-01 07:00:00+00:00  ap135-100-103d-r177       1.0  [ap135, 100, 103d, r177]
1 2016-04-01 07:00:00+00:00   ap135-100-121-r177       3.0   [ap135, 100, 121, r177]
2 2016-04-01 07:00:00+00:00   ap135-100-139-r177       6.0   [ap135, 100, 139, r177]
3 2016-04-01 07:00:00+00:00   ap135-100-140-r177       5.0   [ap135, 100, 140, r177]
4 2016-04-01 07:00:00+00:00  ap135-100-149b-r177       1.0  [ap135, 100, 149b, r177]
`
`
[
  {'fields': {'AP_count': 1.0, 'test_field': 1.0},
  'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
  'tags': {'floor': '1', 'building_number': '100', 'ap_name': 'ap135-100-103d-r177', 'room': '03d'},
  'measurement': 'wifi_data9'},
  {'fields': {'AP_count': 3.0, 'test_field': 1.0},
  'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
  'tags': {'floor': 1, 'building_number': '100', 'ap_name': 'ap135-100-121-r177', 'room': '121'},
  'measurement': 'wifi_data9'},
  {'fields': {'AP_count': 6.0, 'test_field': 1.0},
  'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
  'tags': {'floor': 1, 'building_number': '100', 'ap_name': 'ap135-100-139-r177', 'room': '139'},
  'measurement': 'wifi_data9'},
  {'fields': {'AP_count': 5.0, 'test_field': 1.0},
  'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
  'tags': {'floor': 1, 'building_number': '100', 'ap_name': 'ap135-100-140-r177', 'room': '140'},
  'measurement': 'wifi_data9'},
  {'fields': {'AP_count': 1.0, 'test_field': 1.0},
  'time': Timestamp('2016-04-01 07:00:00+0000', tz='UTC'),
  'tags': {'floor': '1', 'building_number': '100', 'ap_name': 'ap135-100-149b-r177', 'room': '49b'},
  'measurement': 'wifi_data9'}
 ]
`
