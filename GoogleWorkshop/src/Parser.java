import java.io.BufferedReader;
import java.io.FileReader;
import java.sql.SQLException;
import java.util.Map;
import java.util.TreeMap;

import db.ConnectionPool;

public class Parser {

	public static void main(String[] args) throws ClassNotFoundException, InstantiationException, IllegalAccessException, SQLException, Exception {
		String [] files = {"file2.html","file.html"};
		Map<Integer,Integer> data=FileParser(files);
		ConnectionPool connections=new ConnectionPool();
		
		ConnectionPool.insertCourses(data, 300487253);
		
	}

	public static Map<Integer, Integer> FileParser(String[] files)  {
		Map<Integer, Integer> courses = new TreeMap<Integer, Integer>();
		for (String file : files) {

			try (BufferedReader br = new BufferedReader(new FileReader(file))) {
				StringBuilder sb = new StringBuilder();
				String line = br.readLine();

				while (line != null) {
					if (line.contains("post_chart(") && !line.contains("function")) {
						String[] tags = line.split("\\>");
						for (String s : tags) {
							if (s.contains("post_chart")) {
								System.out.println(s);
								String[] pc = s.split("'");
								// System.out.println(pc[0]);
								int course_num = Integer.valueOf(pc[1]);
								System.out.println(pc[11]);
								int course_grade = Integer.valueOf(pc[11]);
								courses.put(course_num, course_grade);
							}
						}
						// sb.append(line);
						// sb.append(System.lineSeparator());
					}
					line = br.readLine();
				}
				
				// String everything = sb.toString();
				// System.out.println(everything);
				System.out.println(courses.toString());
			}
			catch (Exception e){
				//Do nothing
			}
			
		}
		return courses;
	}

}
