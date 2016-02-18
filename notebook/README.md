# Zeppelin Tutorial

### Introduction

This tutorial is based on the [Zeppelin tutorial](http://zeppelin-project.org/docs/tutorial/tutorial.html) but changed to show how to upload sample data to HDFS

### Launch Components

In the web console, launch

* HDFS
* Spark
* Zeppelin

### Upload sample data

* Navigate to the Hue UI in your browser
* Login as user demo (first time takes a while to initialize)
* Click the "File Browser" link at the top right
* Create a new folder called "zeppelin" then navigate to it
* Upload the bank.csv file in this directory

### Create a Zeppelin Notebook

Navigate to Zeppelin and create new notebook

### Set HDFS endpoint

In the web console, find the service endpoint for HDFS (usually hdfs://hdfs-namenode.spark.endpoints.cluster.local:9000)

In you Zeppelin notebook, set a variable with the HDFS endpoint and path to the bank.csv file:

`val dataPath = "hdfs://hdfs-namenode.spark.endpoints.cluster.local:9000/user/demo/zeppelin/bank.csv"`

It may take a while for Zeppelin to initialize itself

### Run the sample code

#### Create DataFrame from CSV data
```
import org.apache.commons.io.IOUtils
import java.net.URL
import java.nio.charset.Charset

// Zeppelin creates and injects sc (SparkContext) and sqlContext (HiveContext or SqlContext)
// So you don't need create them manually

// load bank data
val bankText = sc.textFile(dataPath)

case class Bank(age: Integer, job: String, marital: String, education: String, balance: Integer)

val bank = bankText.map(s => s.split(";")).filter(s => s(0) != "\"age\"").map(
    s => Bank(s(0).toInt,
            s(1).replaceAll("\"", ""),
            s(2).replaceAll("\"", ""),
            s(3).replaceAll("\"", ""),
            s(5).replaceAll("\"", "").toInt
        )
).toDF()
bank.registerTempTable("bank")
```
#### Run SQL on the data and chart it
```
%sql
select age, count(1) value
from bank
where age < 30
group by age
order by age

%sql
select age, count(1) value
from bank
where age < ${maxAge=30}
group by age
order by age

%sql
select age, count(1) value
from bank
where marital="${marital=single,single|divorced|married}"
group by age
```
