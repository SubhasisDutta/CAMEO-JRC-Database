package com;

import java.io.IOException;
import java.util.HashMap;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

public class WithEdit {
	public static class CAMEOMap extends Mapper<LongWritable, Text, Text, Text> {
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			String[] cols = value.toString().split("\\|");

			if (cols.length == 4) {
				context.write(new Text(cols[3]), new Text("CAMEO|" + cols[0] + ", " + cols[1] + ", " + cols[2]));
			}
		}
	}

	public static class JRCMap extends Mapper<LongWritable, Text, Text, Text> {
		@Override
		public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

			String[] cols1 = value.toString().split("\\|");

			if (cols1.length == 4)
				context.write(new Text(cols1[3]), new Text("JRC|" + cols1[0] + ", " + cols1[1] + ", " + cols1[2]));
		}
	}

	public static class Reduce extends Reducer<Text, Text, Text, Text> {

		HashMap<String, String> cameoh = new HashMap<String, String>();
		HashMap<String, String> jrch = new HashMap<String, String>();

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

			for (String s : cameoh.keySet()) {
				int dist = 0;
				for (String j : jrch.keySet()) {
					dist = minDistance(s, j);
					if (dist < 3) {
						context.write(new Text(s), new Text(j + ", " + jrch.get(j) + ", " + dist));
					}
				}
			}
		}

	    static int minDistance(String word1, String word2) {
	        int m = word1.length();
	        int n = word2.length();
	        
	        int[][] cost = new int[m + 1][n + 1];
	        for(int i = 0; i <= m; i++)
	            cost[i][0] = i;
	        for(int i = 1; i <= n; i++)
	            cost[0][i] = i;
	        
	        for(int i = 0; i < m; i++) {
	            for(int j = 0; j < n; j++) {
	                if(word1.charAt(i) == word2.charAt(j))
	                    cost[i + 1][j + 1] = cost[i][j];
	                else {
	                    int a = cost[i][j];
	                    int b = cost[i][j + 1];
	                    int c = cost[i + 1][j];
	                    cost[i + 1][j + 1] = a < b ? (a < c ? a : c) : (b < c ? b : c);
	                    cost[i + 1][j + 1]++;
	                }
	            }
	        }
	        return cost[m][n];
	    }
		
		
		
		
		
		static int editDist(String str1, String str2, int m, int n) {
			// If first string is empty, the only option is to
			// insert all characters of second string into first
			if (m == 0)
				return n;

			// If second string is empty, the only option is to
			// remove all characters of first string
			if (n == 0)
				return m;

			// If last characters of two strings are same, nothing
			// much to do. Ignore last characters and get count for
			// remaining strings.
			if (str1.charAt(m - 1) == str2.charAt(n - 1))
				return editDist(str1, str2, m - 1, n - 1);

			// If last characters are not same, consider all three
			// operations on last character of first string, recursively
			// compute minimum cost for all three operations and take
			// minimum of three values.
			return 1 + min(editDist(str1, str2, m, n - 1), // Insert
					editDist(str1, str2, m - 1, n), // Remove
					editDist(str1, str2, m - 1, n - 1) // Replace
			);
		}

		static int min(int x, int y, int z) {
			if (x < y && x < z)
				return x;
			if (y < x && y < z)
				return y;
			else
				return z;
		}

	}

	// Driver program
	public static void main(String[] args) throws Exception {

		long startTime = System.currentTimeMillis();
		Configuration conf = new Configuration();
		conf.setInt("mapreduce.task.timeout", 6000000);
		String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();

		if (otherArgs.length != 3) {
			System.err.println("Usage: CountYelpBusiness <in> <out>");
			System.exit(2);
		}

		Job job = Job.getInstance(conf, "CAMEO-JRC");
		job.setJarByClass(WithEdit.class);

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
		if (job.waitForCompletion(true)) {
			long endTime = System.currentTimeMillis();
			long totalTime = endTime - startTime;
			System.out.println("Time taken:" + totalTime + " milliseconds");
			System.exit(0);
		}

	}

}
