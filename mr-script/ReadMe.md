Contain script to Join CAMEO and JRC using Mapreduce.

Developed by: Chandrika Cherukuri  


# Run
hadoop jar ~/edit.jar com.match /<path>/jrc_data.csv /<path>/cameo_data.csv /<path>/output2
 
 
hdfs dfs -cat /<path>/output2/* 