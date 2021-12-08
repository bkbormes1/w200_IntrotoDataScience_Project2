import pandas as pd

col_names = [
    "geonameid"
    , "name"
    , "asciiname"
    , "alternatenames"
    , "latitude"
    , "longitude"
    , "feature_class"
    , "feature_code"
    , "country_code"
    , "cc2"
    , "admin1_code"
    , "admin2_code"
    , "admin3_code"
    , "admin4_code"
    , "population"
    , "elevation"
    , "dem"
    , "timezone"
    , "modification_date"
]

# read text file as csv with "Tab" delimiter
long_lat_data = pd.read_csv('US.txt', names=col_names, sep = '\t')

# filter for City records only with feature_class == 'P'. Population greater than 0 filter helps clean duplicate city name values.
long_lat_data = long_lat_data[ (long_lat_data['feature_class'] == 'P') & (long_lat_data['population'] > 0)]

# subset dataframe for only relevant fields
long_lat_data = long_lat_data[['name', 'latitude', 'longitude', 'feature_class', 'feature_code', 'country_code']]

print(long_lat_data.shape)
print(long_lat_data.columns)
print(long_lat_data.head)