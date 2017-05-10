 var jrc : org.apache.spark.rdd.RDD[(String,String)] = null
 var cameo : org.apache.spark.rdd.RDD[(String,String)] = null
 var res : org.apache.spark.rdd.RDD[(String,String)] = null

 var jrc_raw = sc.textFile("/pxc162330/jrc_data.csv")
 jrc_raw = jrc_raw.filter(x=>(x.split('|').length == 4))
 jrc = jrc_raw.map(x=>(x.split('|')(3),x))
 var cameo_raw = sc.textFile("/pxc162330/cameo_data.csv")
 cameo_raw = cameo_raw.filter(x=>(x.split('|').length ==4))
 cameo = cameo_raw.map(x=>(x.split('|')(3),x))
 val jo = cameo.join(jrc)
 jo.saveAsTextFile("/pxc162330/directjoin_out")