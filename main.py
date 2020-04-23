import pandas as pd
from influxdb import InfluxDBClient
import sys
import geohash2

''' 
TO DO:
- Initial Import Function
- Download the Latest CSV Function
- Import the new Data to Influx 
- main function - Check every so often or Cronjob? 
'''

''' Influx Configs '''
client = InfluxDBClient('localhost', 8086, 'telegraf', 'secretpassword', 'covid')

''' Read the CSV File | Usage: python main.py 04-20-20.csv '''
df = pd.read_csv(sys.argv[1])

# Convert the Last_Update column to time object and resolve the Date Format change
try:
    df['Last_Update'] = pd.to_datetime(df['Last_Update'], format='%Y-%m-%d %H:%M:%S')
except ValueError:
    df['Last_Update'] = pd.to_datetime(df['Last_Update'], format='%m/%d/%y %H:%M')

# Convert the Last_Update column to time format needed for Influxdb client
df['Last_Update'] = df['Last_Update'].dt.strftime('%Y-%m-%dT%H:%M:%SZ')

''' Convert to InlfuxDB Format ''' 
for index, row in df.iterrows():
    # Send fields in json format
    data = [
            {
                "measurement": "covid",
                "time": row['Last_Update'],
                "tags": {
                    "county": row['Admin2'],
                    "province_state": row['Province_State'],
                    "country_region": row['Country_Region'],
                    "latitude": row['Lat'],
                    "longitude": row['Long_'],
                    "combined_key": row['Combined_Key'],
                    "geohash": geohash2.encode(float(row['Lat']),float(row['Long_']))
                },
                "fields": {
                    "confirmed": row['Confirmed'],
                    "deaths": row['Deaths'],
                    "recovered": row['Recovered'],
                    "active": row['Active'],
                    "combined_key": row['Combined_Key']
                }
            }
        ]

    print(data)
    client.write_points(data)

