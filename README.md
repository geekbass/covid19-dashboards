# Covid19 Data to Influx
COMING SOON

### Pre-reqs
- Python 3
```bash
pip install influxdb geohash2
```
- Docker

### Usage
Below is current usage today. This will be more automated in the future.

1) Create Influx and Grafana.
```bash
docker-compose up -d
```

2) Pull down the Data. 
```
git clone https://github.com/CSSEGISandData/COVID-19.git && \
mkdir -pv archives && \
cp COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/* ./archives/ && \
```

3) Run the script on all files from 03-22-20 and later. *Earlier files have a different format not prepared in the script*. This is going to take some time to complete. 
```bash
grep -r Last_Update archives/* | awk -F: '{print $1}' > valid.txt && \
for i in `cat valid.txt`; do python main.py $i ; done
```

4) Login to Grafana UI http://localhost:3000 with admin/admin to begin looking through the Dashboards.

### Data Updates
Johns Hopkins updates about every 24 hours. To update your data do the following. *As mentioned this will be much more automated in the near future. Follow these instructions for the time being.*
```bash
cd COVID-19/ && \
git pull origin master && \
cd .. && \
cp COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/* archives/

python main.py archives/$latest-file-2020.csv
```

### To Do
[ X ] Docs

[ X ] Automatic DB creation

[ ] Automated Pull down of new files and input to Influx

[ X ] Docker-compose

[ X ] Import Dashboard
