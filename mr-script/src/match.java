package com;

import java.io.IOException;
import java.time.Duration;
import java.time.Instant;
import java.util.HashMap;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class match {
	public static class CAMEOMap extends Mapper<LongWritable, Text, Text, Text> {
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			String[] cols = value.toString().split("\\|");

			if (cols.length == 4) {
				context.write(new Text(cols[3]), new Text("CAMEO|" + cols[0] +", "+ cols[1] +", "+ cols[2]));
			}
		}
	}

	public static class JRCMap extends Mapper<LongWritable, Text, Text, Text> {
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			String[] cols1 = value.toString().split("\\|");

			if (cols1.length == 4)
				context.write(new Text(cols1[3]), new Text("JRC|" + cols1[0] +", "+ cols1[1] +", "+ cols1[2]));
		}
	}

	public static class Reduce extends Reducer<Text, Text, Text, Text> {

		HashMap<String, String> cameoh = new HashMap<String, String>();
		HashMap<String, String> jrch = new HashMap<String, String>();

		String cam = "";
		String jrc = "";

		public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
			for (Text t : values) {

				if (t.toString().charAt(0) == 'C') {
					cameoh.put(key.toString(), t.toString());
				} else if (t.toString().charAt(0) == 'J') {
					jrch.put(key.toString(), t.toString());
				}
			}

		}

		@Override
		protected void cleanup(Context context) throws IOException, InterruptedException {

			if (!cameoh.isEmpty()) {
				for (String s : cameoh.keySet()) {
					if (jrch.containsKey(s)) {
						context.write(new Text(s), new Text(cameoh.get(s) + (String) jrch.get(s)));
					}
				}
			}

		}

	}

	// Driver program
	public static void main(String[] args) throws Exception {
		
		
		long startTime = System.currentTimeMillis();
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();

		if (otherArgs.length != 3) {
			System.err.println("Usage: CountYelpBusiness <in> <out>");
			System.exit(2);
		}

		Job job = Job.getInstance(conf, "CAMEO-JRC");
		job.setJarByClass(match.class);

		// job.setMapperClass(CAMEOMap.class);
		// job.setMapperClass(JRCMap.class);

		job.setReducerClass(Reduce.class);

		job.setOutputKeyClass(Text.class);

		// set output value type
		job.setMapOutputValueClass(Text.class);
		job.setOutputValueClass(Text.class);

		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);

		MultipleInputs.addInputPath(job, new Path(args[0]), TextInputFormat.class, CAMEOMap.class);
		MultipleInputs.addInputPath(job, new Path(args[1]), TextInputFormat.class, JRCMap.class);

		// set the HDFS path of the input data
		// FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		// FileInputFormat.addInputPath(job, new Path(otherArgs[1]));
		// set the HDFS path for the output
		FileOutputFormat.setOutputPath(job, new Path(otherArgs[2]));

		// Wait till job completion
		if(job.waitForCompletion(true)){
			long endTime   = System.currentTimeMillis();
			long totalTime = endTime - startTime;
			System.out.println("Time taken:"+ totalTime+" milliseconds");
			System.exit(0);
		}
		
	}

}
