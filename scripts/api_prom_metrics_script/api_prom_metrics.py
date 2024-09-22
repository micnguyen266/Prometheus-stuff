# This python script is just an example and will need to be modified to work with other APIs

#!/bin/python3

import sys,json,urllib.request
response = urllib.request.urlopen('http://service.region.abccompany.com/apiv1/stats/current')
txtdata=response.read()
#Variable to test manually
#txtdata=open("/home/mnguyen/input.json").read()
data=json.loads(txtdata)
stats=data["stats"]
for suffix in ["ptime","working","wtime"]:
    metricname="service_qc_%s"%(suffix)
    print("#HELP %s is a custom qc metric"%(metricname))
    print("#TYPE %s Gauge"%(metricname))
    for check,data in stats.items():
        value=data[suffix]
        print("%s{check=\"%s\"} %s"%(metricname,check,value))
metricname="service_qc_queue"
print("#HELP %s is a custom qc metric"%(metricname))
print("#TYPE %s Gauge"%(metricname))
for check,data in stats.items():
    for priority in [1,2,3,4,5]:
        value=data["priority-%d"%(priority)]
        print("%s{check=\"%s\",priority=\"%d\"} %s"%(metricname,check,priority,value))