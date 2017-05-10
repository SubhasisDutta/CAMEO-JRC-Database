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

public class Sampling {

	public static void main(String[] args) throws IOException {
		
		
		try {
			File fileDir = new File("C:\\Users\\Sneha\\Documents\\study materials\\Independent Study\\features-train.txt");
			BufferedReader in = new BufferedReader(new InputStreamReader(new FileInputStream(fileDir), "UTF-8"));
			String str;
			FileWriter fstream,sstream;
			BufferedWriter out,out2;
			fstream = new FileWriter(
					"C:\\Users\\Sneha\\Documents\\study materials\\Independent Study\\formatted-train.txt");
			sstream = new FileWriter(
					"C:\\Users\\Sneha\\Documents\\study materials\\Independent Study\\formatted-test.txt");
			out = new BufferedWriter(fstream);
			out2= new BufferedWriter(sstream);
			while ((str = in.readLine()) != null) {
				String splits[] = new String[10];
				System.out.println(str);
				splits = str.split(",");			
				String lang = splits[7].trim();				
				if (lang.equals("0")) {
					
					out2.write(str);
					}
				else
				{
					out.write(str);
				}
				}
			
			in.close();
			out.close();
			out2.close();
			}
		
		 catch (UnsupportedEncodingException e) {
			System.out.println(e.getMessage());
		} catch (IOException e) {
			System.out.println(e.getMessage());
		} catch (Exception e) {
			System.out.println(e.getMessage());
		}
	}
}
		
		
	