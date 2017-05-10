import java.io.File;
import java.io.*;
import java.io.FileWriter;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class UnicodeGenerator {

	public static void main(String[] args) throws IOException {
		
		// TODO Auto-generated method stub
		Map<String, List<Integer>> map = new HashMap<String, List<Integer>>();
		Map<String, List<Double>> featureMap = new HashMap<String, List<Double>>();
		Map<String, String> langMap = new HashMap<String, String>();
		try {
			File fileDir = new File("C:\\Users\\Sneha\\Documents\\study materials\\Independent Study\\entities.txt");
			BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(fileDir), "UTF-8"));
			String str;
			while ((str = in.readLine()) != null) {

				
				String splits[] = new String[50];
				
				splits = str.split("\t");
				//System.out.println(splits[1]);
				String name = splits[3];
			//	System.out.println("hello");
				name = name.toLowerCase();
				
				if (!map.containsKey(name)) {
					
					for (int i = 0; i < name.length(); i++) {
						int a = Character.codePointAt(name, i);
						if (map.get(name) == null) {
							map.put(name, new ArrayList<Integer>());
							langMap.put(name, null);
						}
						map.get(name).add(new Integer(a));
						langMap.put(name,splits[2]);
					
					}
				}

			}
			in.close();
		} catch (UnsupportedEncodingException e) {
			System.out.println(e.getMessage());
		} catch (IOException e) {
			System.out.println(e.getMessage());
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
		for (Map.Entry<String, List<Integer>> entry : map.entrySet()) {
			System.out.println(entry.getKey() + " : " + entry.getValue());
		}
		
		FileWriter fstream;
		BufferedWriter out;
		fstream = new FileWriter(
				"C:\\Users\\Sneha\\Documents\\study materials\\Independent Study\\values-entities.txt");
		out = new BufferedWriter(fstream);
		Iterator<Entry<String, List<Integer>>> it = map.entrySet().iterator();
		while (it.hasNext()) {

			// the key/value pair is stored here in pairs
			Map.Entry<String, List<Integer>> pairs = it.next();
			out.write(pairs.getKey() + " " + pairs.getValue());
			out.newLine();
			

		}
		out.close();	

		Iterator<Entry<String, List<Integer>>> it1 = map.entrySet().iterator();
		while (it1.hasNext()) {

			// the key/value pair is stored here in pairs
			Map.Entry<String, List<Integer>> pairs = it1.next();
			List<Integer> values = new ArrayList<Integer>();
			values = pairs.getValue();
			String name = pairs.getKey();
			double mean = getMean(values);
			// System.out.println("Mean="+mean);
			double median = getMedian(values);
			// System.out.println("Median: " + median);
			double range = getRange(values);
			// System.out.println("Range: " + range);
			double min = getMin(values);
			// System.out.println("min: " + min);
			double max = getMax(values);
		

			if (!featureMap.containsKey(name)) {
				
				featureMap.put(name, new ArrayList<Double>(Arrays.asList(mean, median, range, min, max)));
			} else {
				featureMap.get(name).add(mean);
				featureMap.get(name).add(median);
				featureMap.get(name).add(range);
				featureMap.get(name).add(min);
				featureMap.get(name).add(max);
				
			}
		}
		FileWriter fwtrain,fwtest;
		BufferedWriter fbwtrain,fbwtest;
		fwtrain = new FileWriter(
				"C:\\Users\\Sneha\\Documents\\study materials\\Independent Study\\features-train.txt");
		fwtest = new FileWriter(
				"C:\\Users\\Sneha\\Documents\\study materials\\Independent Study\\features-test.txt");
		fbwtest = new BufferedWriter(fwtest);
		fbwtrain = new BufferedWriter(fwtrain);
		Iterator<Entry<String, List<Double>>> it2 = featureMap.entrySet().iterator();
		Iterator<Entry<String, String>> it3 = langMap.entrySet().iterator();
		while (it2.hasNext() && it3.hasNext()) {
			Map.Entry<String, List<Double>> pairs1 = it2.next();
			Map.Entry<String, String> pairs2 = it3.next();
			String key = (pairs1.getKey() == pairs2.getKey()) ? pairs1.getKey() : null;
			String lang = pairs2.getValue();
			if(lang=="u"){
				fbwtest.write(pairs1.getKey() + pairs1.getValue() + lang);
				fbwtest.newLine();
			}
			else{
			fbwtrain.write(pairs1.getKey() + pairs1.getValue() + lang);

			fbwtrain.newLine();
			}		
		}
		// lastly, close the file and end
		fbwtrain.close();
		fbwtest.close();
	}

	public static double getMean(List<Integer> numberList) {
		double total = 0.0;
		for (int d : numberList) {
			total += d;
		}

		return total / (numberList.size());
	}

	public static double getRange(List<Integer> numberList) {
		double initMin = numberList.get(0);
		double initMax = numberList.get(0);
		for (int i = 1; i < numberList.size(); i++) {
			if (numberList.get(i) < initMin)
				initMin = numberList.get(i);
			if (numberList.get(i) > initMax)
				initMax = numberList.get(i);
		}

		return initMax - initMin;
	}

	public static double getMedian(List<Integer> numberList) {
		Collections.sort(numberList);
		double median = 0;
		double pos1 = Math.floor((numberList.size() - 1.0) / 2.0);
		double pos2 = Math.ceil((numberList.size() - 1.0) / 2.0);
		if (pos1 == pos2) {
			median = numberList.get((int) pos1);
		} else {
			median = (numberList.get((int) pos1) + numberList.get((int) pos2)) / 2.0;
		}

		return median;
	}

	public static double getMin(List<Integer> numberList) {
		Collections.sort(numberList);
		int min = numberList.get(0);
		return min;
	}

	public static double getMax(List<Integer> numberList) {
		Collections.sort(numberList);
		int max = numberList.get(numberList.size() - 1);
		return max;
	}

	public static double getMode(List<Integer> numberList) {

		int[] count = new int[101];
		if (numberList.size() > 0) {
			// count the occurrences
			for (int i = 1; i <= numberList.size(); i++) {
				count[numberList.get(i)]++;
			}

			// go backwards and find the count with the most occurrences
			int index = count.length - 1;
			for (int i = count.length - 2; i >= 0; i--) {
				if (count[i] >= count[index])
					index = i;
			}
			//System.out.println("mde: " + index);
			return index;
		} else
			return -1;
	}

	public int compare(Integer i, Integer j) {
		return i - j;
	}
}
