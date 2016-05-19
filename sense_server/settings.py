import os

TIMEZONE = os.environ.get("TZ", "Asia/Shanghai")

DATABASE = "mysql://root:password@192.168.2.193/senseapi"

ELASTIC_SEARCH_HOST = "192.168.2.193"
ELASTIC_SEARCH_PORT = 9200
