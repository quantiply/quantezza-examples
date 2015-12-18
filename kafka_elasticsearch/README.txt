

#https://www.elastic.co/guide/en/kibana/current/getting-started.html

ES_URL=http://es-http-workthistime.apps.dev.aws.qtz.io
KAFKA_URL=http://kafka-proxy-workthistime.apps.dev.aws.qtz.io

curl -XPUT $ES_URL/shakespeare -d '
{
 "mappings" : {
  "_default_" : {
   "properties" : {
    "speaker" : {"type": "string", "index" : "not_analyzed" },
    "play_name" : {"type": "string", "index" : "not_analyzed" },
    "line_id" : { "type" : "integer" },
    "speech_number" : { "type" : "integer" }
   }
  }
 }
}
';

wget https://raw.githubusercontent.com/Kshi-Kshi/elasticsearch-sandbox/master/kibana-10_minute_walk_through/shakespeare.json
awk 'NR % 2 == 0' shakespeare.json > shakespeare_clean.json
./encode_for_proxy.py < shakespeare_clean.json > shakespeare_encoded.json

curl -v -X POST -H "Content-Type: application/vnd.kafka.binary.v1+json" \
     --data-binary @shakespeare_encoded.json "$KAFKA_URL/topics/shakespeare"
