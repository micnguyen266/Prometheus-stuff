### Convert Kibana metrics to use in Prometheus

**Requirement:** We need a way to query the custom metric in Kibana and pass it to Prometheus for setting up alerts on that data.

**Method:** We can curl the Kibana API with the required query parameters the response will be in JSON. Store the JSON and parse it for relevant values. The custom metric is generated from the values parsed in JSON and stored in a file from where Prometheus picks them up.

**Steps Involved:**
1. Generate the query
2. Send the request using python 
3. Parse the JSON
4. Generate Prometheus metrics

In your server you will create 2 scripts. The scripts are in /etc/prometheus_scripts/kibana folder. There are 2 scripts kibana_prom_metrics.py and kibana.sh
The Python script named kibana_prom_metrics.py sends and receives the data. The Prometheus metrics are stored in redis_exception.prom for node_exporter to grab metrics from. While kibana.sh is used to run the python script every 5 min by cronjob.

**Generate the query** 
1. Navigate to the Kibana Dashboard and type the query you want to search. At the bottom of the visualization, there is a small caret you can click in order to view more details about the underlying query. 
2. Then you can click on the "Request" button in order to view the underlying query, which you can copy/paste and store it as we will be passing it using python. 
3. The other way of retrieving the query is using your browser and go to the Kibana dashboard, open the developer console and write your query while having the Network tab open. When you search for your query in the Kibana dashboard you will see the request appear in the developer console. There you can "right click" and select Copy as cURL, which will copy the curl command to your clipboard. Save the curl in your notepad.
4. Ensure you adjust all the attributes: "index", "gte","lte", "field": @timestamp,"interval" and "extended_bounds":{"min","max"}. For index using wildcard may help. Generally you want to keep the timestamp, interval and extended bounds the same.

**Send the request using python**
1. We are using python requests library to make HTTP requests. The Kibana APIs support the kbn-xsrf and Content-Type headers.
2. The parameters added to the base url.
3. We will need to pass some data to API server. We store this data variable as a dictionary. It contains the Kibana query which we copied from console.
4. We use requests.post() method since we are sending a POST request.
5. The data in this request corresponds to --data-raw parameter we received in curl.

**Parse the JSON**
1. The data is retrieved from the response object, we convert the response content into a JSON by using json() method. Finally, we extract the required information by parsing down the JSON type object.

**Generate Prometheus Metrics**
1. To add the data in prometheus we need to add metric to .prom file and store in a folder from where node_exporter scrapes the directory every 5 mins.

**Create kibana.sh script and have the cronjob run every 5 mins**
1. Create a shell script kibana.sh. This shell script runs the python script kibana_prom_metrics.py and outputs into a text file in /etc/prometheus_scripts/textfile_collector/redis_exception.prom for node_exporter to grab metrics from.
2. This goes in the crontab:
3. */5 * * * * /etc/prometheus_scripts/kibana/kibana.sh 
4. Assuming Node exporter is installed in the server and uses port 9100 which Prometheus scrapes on. Node exporter will collect custom metrics from this path: 
5. /etc/sysconfig/node_exporter 
6. OPTIONS="--collector.textfile.directory=/etc/prometheus_scripts/textfile_collector"

### Author

Michael Nguyen https://github.com/micnguyen266