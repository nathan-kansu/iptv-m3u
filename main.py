import duckdb

duckdb.connect()
channels = duckdb.sql("" \
"SELECT id, name, network, country, categories  " \
"FROM 'data/channels.csv' as channels " \
"WHERE channels.closed IS NULL " \
"AND channels.network NOT LIKE '%Pluto%'" \
"AND channels.categories IS NOT NULL " \
"ORDER BY channels.country ASC"
);

print(channels)
