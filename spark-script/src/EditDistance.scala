import org.apache.spark._
import org.apache.spark.SparkContext._
import org.apache.log4j._
import scala.math.max
import scala.math.min
import scala.io.Source
import scala.math._

object cameo {
  
  var jrc : org.apache.spark.rdd.RDD[(String,String)] = null
  var cameo : org.apache.spark.rdd.RDD[(String,String)] = null
  var res : org.apache.spark.rdd.RDD[(String,String)] = null
  var st : String = ""
  def minimum(i1: Int, i2: Int, i3: Int)=min(min(i1, i2), i3)
  
   def distance(s1:String, s2:String)={
      val dist=Array.tabulate(s2.length+1, s1.length+1){(j,i)=>if(j==0) i else if (i==0) j else 0}
 
      for(j<-1 to s2.length; i<-1 to s1.length)
         dist(j)(i)=if(s2(j-1)==s1(i-1)) dist(j-1)(i-1)
           else minimum(dist(j-1)(i)+1, dist(j)(i-1)+1, dist(j-1)(i-1)+1)
 
      dist(s2.length)(s1.length)
   }
  
  def loadjrc() : Map[String,String]={
    val file = Source.fromFile("../jrc.csv").getLines()
    var map_jrc : Map[String,String] = Map()
    for(line <- file){
      if(line.split("|").length ==4){
        var l = line.split("|")
        map_jrc += (l(3)->line)
      }
    }
    
    return map_jrc
  }
  
  def fun(v:String) : String={
    for(tup <- jrc){
      if(distance(tup._1.toString(),v)<=3){
       st = st + "<"+tup._2+">"
        
      }
      
    }
    val sss = st
    st = ""
    return sss
    
  }
  
  def main(args : Array[String]){
    Logger.getLogger("org").setLevel(Level.ERROR)
  val sc = new SparkContext("local[*]","mut_frds")
  var jrc_raw = sc.textFile("../jrc.csv")
  //var jrc_b = sc.broadcast(loadjrc)
  jrc_raw = jrc_raw.filter(x=>(x.split('|').length == 4)) 
  jrc = jrc_raw.map(x=>(x.split('|')(3),x))
  var cameo_raw = sc.textFile("../cameo.csv")
  cameo_raw = cameo_raw.filter(x=>(x.split('|').length ==4))
  cameo = cameo_raw.map(x=>(x.split('|')(3),x))
  res = cameo.map(x=>(x._1,fun(x._1)))
  res.saveAsTextFile("../result_distance")
  
  }
  }

