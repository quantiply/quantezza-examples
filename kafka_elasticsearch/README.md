# Kafka + Elasticsearch Example

### Introduction

This example is derived from this [Kibana tutorial](https://www.elastic.co/guide/en/kibana/current/getting-started.html) but modified to load data into Kafka first before Elasticsearch.

### Prerequisites

* curl
* [elasticdump](https://www.npmjs.com/package/elasticdump) (optional)

### Launch Components

From the Quantiply Data Foundry web, console, launch:

* ZooKeeper
* Kafka
* Elasticsearch

#### Set environment

From the UI, get the endpoints for Kafka Rest proxy and Elasticsearch HTTP API and set them in env.sh then source it.

`. env.sh`

### Create Elasticsearch mapping

```
curl -XPUT $ES_URL/_template/shakespeare -d '
{
	"template": "shakespeare*",
	"aliases": {
		"shakespeare": {}
	},
	"mappings": {
		"_default_": {
			"properties": {
				"speaker": {
					"type": "string",
					"index": "not_analyzed"
				},
				"play_name": {
					"type": "string",
					"index": "not_analyzed"
				},
				"line_id": {
					"type": "integer"
				},
				"speech_number": {
					"type": "integer"
				}
			}
		}
	}
}
';
```

### Load Data Into Kafka

```
curl -v -X POST -H "Content-Type: application/vnd.kafka.binary.v1+json" \
     --data-binary @shakespeare_kafka_rest.json "$KAFKA_URL/topics/shakespeare"
```

### Launch Elasticsearch Loader

From the UI, launch the Rico Elasticsearch Loader and enter these values for the parameters:

* Kafka topic: shakespeare
* Elasticsearch index prefix: shakespeare
* Elasticsearch document type: lines

### Load Kibana Dashboard

```
elasticdump --input=kibana/mapping.json --output=$ES_URL/.kibana --type=mapping
elasticdump --input=kibana/data.json --output=$ES_URL/.kibana --type=data
```

## Load Kibana in browser and open the "Shakespeare" dashboard
