
# Launch HDFS
# Launch Launch Spark
# Launch Zeppelin

wget https://s3.amazonaws.com/apache-zeppelin/tutorial/bank/bank.csv



import org.apache.commons.io.IOUtils
import java.net.URL
import java.nio.charset.Charset

// Zeppelin creates and injects sc (SparkContext) and sqlContext (HiveContext or SqlContext)
// So you don't need create them manually

// load bank data
val bankText = sc.textFile("hdfs://hdfs-namenode.demo.endpoints.cluster.local:9000/user/batman/zeppellin/bank.csv")


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
