# This python script is just an example of counting Redis exceptions and will need to be modified to work with your custom Kibana queries.

import requests
import json
from datetime import datetime, timedelta
import time
from dateutil import parser

# convert the current system time to epochs millis
# the current_time and thirty_min_ago time is passed in data variable
current_time = int(round(time.time() * 1000))
thirty_min_ago = int((datetime.now() - timedelta(minutes=30)).timestamp() * 1000)
#print(current_time,thirty_min_ago)
#headers as passed in curl
url = 'http://elasticsearch.consul:9200/elasticsearch/_msearch'
headers = {
    'authority': 'stats.abccompany.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json;charset=UTF-8',
    'kbn-xsrf': 'reporting',
}
params = (
    ('timeout', '0'),
    ('ignore_unavailable', 'true'),
    ('preference', '1111222233334'),
)
# data to be sent to api
# previously set to "index":["_all"]
data = '{"index":["logs-prod*"],"ignore_unavailable":true}\n{"size":500,"sort":[{"@timestamp":{"order":"
desc","unmapped_type":"boolean"}}],"query":{"filtered":{"query":{"query_string":{"query":"exception:
\'ServiceStack.Redis.RedisResponseException\'","analyze_wildcard":true}},"filter":{"bool":{"must":[{"range":
{"@timestamp":{"gte":'+str(thirty_min_ago)+',"lte":'+str(current_time)+',"format":"epoch_millis"}}}],"must_not":
[]}}}},"highlight":{"pre_tags":["@kibana-highlighted-field@"],"post_tags":["@/kibana-highlighted-field@"],"
fields":{"*":{}},"require_field_match":false,"fragment_size":2147483647},"aggs":{"2":{"date_histogram":
{"field":"@timestamp","interval":"15m","time_zone":"America/New_York","min_doc_count":0,"extended_bounds":
{"min":'+str(thirty_min_ago)+',"max":'+str(current_time)+'}}}},"fields":["*","_source"],"script_fields":{},"
fielddata_fields":["date","@timestamp"]}\n'
## sending post request and saving response as response object
# send the request to kibana using consul url as to bypass okta
response = requests.post(url, headers=headers, params=params,  data=data)
#store the Json response
jsonResponse = response.json()
data_load = jsonResponse['responses'][0]['aggregations']['2']['buckets']
#Generate metrics for Prometheus
metricname="count_service_redis_exception"
print("#HELP %s is a custom kibana metric"%(metricname))
print("#TYPE %s Gauge"%(metricname))
# for i in data_load:
#   parsed_date = parser.parse(i['key_as_string'])
#     print( i["key_as_string"],i["doc_count"])
#   z = str(i['doc_count'])
#    print{' + "Date=" + i["key_as_string"] + ""+ ""+ "doc_count=" +z + "}")
#    print("%s{date=\"%s\"} %s"%(metricname,parsed_date,z))
total_count=jsonResponse['responses'][0]["hits"]["total"]
print("%s{error=\"service_redisexception\"} %s"%(metricname,total_count))