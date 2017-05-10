import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.log4j._
import scala.math.max
import scala.math.min
import scala.io.Source
import scala.math._

object direct_join {
  var jrc : org.apache.spark.rdd.RDD[(String,String)] = null
  var cameo : org.apache.spark.rdd.RDD[(String,String)] = null
  var res : org.apache.spark.rdd.RDD[(String,String)] = null
  
  def main(args : Array[String]){
  Logger.getLogger("org").setLevel(Level.ERROR)
  val sc = new SparkContext("local[*]","mut_frds")
  var jrc_raw = sc.textFile("../jrc.csv")
  jrc_raw = jrc_raw.filter(x=>(x.split('|').length == 4)) 
  jrc = jrc_raw.map(x=>(x.split('|')(3),x))
  var cameo_raw = sc.textFile("../cameo.csv")
  cameo_raw = cameo_raw.filter(x=>(x.split('|').length ==4))
  cameo = cameo_raw.map(x=>(x.split('|')(3),x))
  val jo = cameo.join(jrc)
  jo.saveAsTextFile("../result_direct_join")
  }
  
}