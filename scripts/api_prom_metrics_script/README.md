### Pull API metrics to use in Prometheus

1. The purpose of this project is to make an API call to gather metrics and convert them to Prometheus readable metrics.
We would need to create 2 scripts in your server.

2. In /etc/prometheus_scripts/qcstats there will be 2 scripts api_prom_metrics.py and qc.sh

3. First there is a Python script called api_prom_metrics.py. This sends a request to the qc API to get the current stats metrics and then the script converts it into Prometheus readable metrics.

4. Second there is a shell script qc.sh. This shell script runs the python script api_prom_metrics.py and outputs into a text file in /etc/prometheus_scripts/textfile_collector/service_qc.prom for node_exporter to grab metrics from.

5. The cronjob runs qc.sh script every 5 mins. 

6. This goes in the crontab
7. */5 * * * * /etc/prometheus_scripts/qcstats/qc.sh 
8. Assuming Node exporter is installed in the server and uses port 9100 which Prometheus scrapes on.
Node exporter will collect custom metrics from this path 
9. /etc/sysconfig/node_exporter 
10. OPTIONS="--collector.textfile.directory=/etc/prometheus_scripts/textfile_collector"

### Author

Michael Nguyen https://github.com/micnguyen266