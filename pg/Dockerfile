FROM postgres:9.6

# To deploy a fresh db:
#  COPY init.sql /docker-entrypoint-initdb.d 

# To restore a backup:
COPY 0000-2018-01-12.sql /docker-entrypoint-initdb.d

# Apply migrations
COPY migrations/0001-20180201.sql /docker-entrypoint-initdb.d
