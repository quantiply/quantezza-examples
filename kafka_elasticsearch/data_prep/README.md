### How To Prepare the Shakespeare Data for Kafka REST proxy

```
wget https://raw.githubusercontent.com/Kshi-Kshi/elasticsearch-sandbox/master/kibana-10_minute_walk_through/shakespeare.json
awk 'NR % 2 == 0' shakespeare.json > shakespeare_clean.json
./encode_for_proxy.py < shakespeare_clean.json > shakespeare_kafka_rest.json
```