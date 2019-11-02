import os
from elasticsearch import Elasticsearch

# HOST and PORT settings
HOST = '0.0.0.0'
PORT = 8081

# Elastic settings
es_host = 'localhost'
es_port = 9200


es = Elasticsearch([
	{
		'host': es_host,
		'port': es_port
	}
])

ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
