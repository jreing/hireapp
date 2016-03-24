package db;

import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import javax.xml.bind.PropertyException;


public class Connector implements Runnable {

	private static final int MAX_BATCH_SIZE = 1000;
	private static final String DB_CONFIG_FILE = "Dbconfig.properties";
	private static final ConnectionProperties props;
//	private static final SearchResults results = ConnectionPool.results;
	public static final PropertyReader pr;

	public Connection connection;
	private boolean inUse = true;
	
	/**
	 * Creates a new property reader for DB_CONFIG_FILE file, 
	 * as well as creates a new connection property,
	 * based on the relevant information from DB_CONFIG_FILE.    
	 */
	static {
		try {
			pr = new PropertyReader(DB_CONFIG_FILE);
			props = new ConnectionProperties(pr);
		} catch (IOException | PropertyException e) {
			e.printStackTrace();
			throw new RuntimeException("Can't read connection properties");
		}
	}

	synchronized boolean isInUse() {
		return inUse;
	}

	synchronized void setInUse(boolean inUse) {
		this.inUse = inUse;
	}
	
	/**
	 * Waits till the current connection has been established.
	 * 
	 * @throws InterruptedException
	 */
	synchronized void waitTillConnectionHasBeenEstablished()
			throws InterruptedException {
		while (connection == null) {
			Thread.sleep(1);
		}
	}


	/**
	 * Closes the connection.
	 * 
	 * @throws SQLException
	 */
	synchronized void closeConnection() throws SQLException {
		try {
			this.connection.close();
		} catch (SQLException e) {
			throw new SQLException("Error closing Connection to DB: "
					+ e.getMessage());
		}
	}
	/**
	 * Inserts a list of entities to the specified table.
	 * 
	 * @param list	a polymorphic list of entities to insert to DB
	 * @param table	a table in DB
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws PropertyException
	 * @throws Exception
	 */
//	synchronized public void insertEntities(List<Entity> list, String table)
//			throws ClassNotFoundException, SQLException, PropertyException,
//			Exception {
//
//		PreparedStatement pstmt = null;
//		Statement stmt = null;
//		boolean tableExists = false;
//
//		try {
//			connection.setAutoCommit(false);
//
//			// check if table already exists
//			String query = "SELECT count(*) FROM information_schema.tables WHERE table_schema = '"
//					+ pr.getProp("schema")
//					+ "' AND table_name = '"
//					+ table
//					+ "'";
//			stmt = connection.createStatement();
//			ResultSet rs = stmt.executeQuery(query);
//			while (rs.next()) {
//				int count = rs.getInt("count(*)");
//				if (count > 0) {
//					tableExists = true;
//				}
//			}
//
//			// if table doesn't exist then create it
//			if (!tableExists) {
//				query = "CREATE TABLE " + table;
//				switch (table) {
//				case "city":
//					query += "(city_id INT, " + "country_code CHAR(2), "
//							+ "city_name VARCHAR(255), "
//							+ "latitude VARCHAR(15), "
//							+ "longitude VARCHAR(15), "
//							+ "country_id INT(11), "
//							+ "PRIMARY KEY (city_id));";
//					break;
//				case "country":
//					query += "(country_id INT, "
//							+ "country_name VARCHAR(255), "
//							+ "continent VARCHAR (20), "
//							+ "country_code CHAR(2), "
//							+ "PRIMARY KEY (country_id));";
//					break;
//				case "person":
//					query += "(id INT NOT NULL AUTO_INCREMENT, "
//							+ "name VARCHAR(255), " + "born_in VARCHAR (255), "
//							+ "died_in VARCHAR(255), "
//							+ "lives_in VARCHAR(255), "
//							+ "gender VARCHAR(15), " + "info LONG VARCHAR, "
//							+ "PRIMARY KEY (id));";
//
//				}
//				stmt.executeUpdate(query);
//			}
//
//			// prepare an insertion statement suitable for table
//			String fields = pr.getProp(table + "_attrs");
//			int numFields = fields.split(",").length;
//			String fields_table = "(" + fields + ")";
//
//			String values_table = " VALUES (";
//			for (int i = 0; i < numFields; i++) {
//				values_table += "?";
//				if (i != numFields - 1) {
//					values_table += ", ";
//				}
//			}
//			values_table += ")";
//
//			switch (table) {
//			case "city":
//				pstmt = connection.prepareStatement("INSERT INTO " + table
//						+ fields_table + values_table
//						+ " on DUPLICATE KEY UPDATE city_id=city_id");
//				break;
//			case "country":
//				pstmt = connection.prepareStatement("INSERT INTO " + table
//						+ fields_table + values_table
//						+ " on DUPLICATE KEY UPDATE country_id=country_id");
//				break;
//			case "person":
//				pstmt = connection.prepareStatement("INSERT INTO " + table
//						+ fields_table + values_table
//						+ " on DUPLICATE KEY UPDATE id=id");
//				break;
//			}
//
//			// go over the entities of the table and batch them into
//			// a batch of size MAX_BATCH_SIZE
//			int batchSize = 0;
//			for (int i = 0; i < list.size(); i++) {
//				// if a batch of size MAX_BATCH_SIZE is ready, commit it
//				if (batchSize == MAX_BATCH_SIZE) {
//					pstmt.executeBatch();
//					connection.commit();
//					batchSize = 0;
//				}
//
//				// set the appropriate values of entity
//				Entity entity = list.get(i);
//				switch (table) {
//				case "city":
//					pstmt.setInt(1, entity.getGeoPlaceRef());
//					pstmt.setString(2, ((City) entity).getCountry_code());
//					pstmt.setString(3, entity.getName());
//					pstmt.setString(4,
//							Double.toString(((City) entity).getLatitude()));
//					pstmt.setString(5,
//							Double.toString(((City) entity).getLongitude()));
//					break;
//				case "country":
//					pstmt.setInt(1, entity.getGeoPlaceRef());
//					pstmt.setString(2, entity.getName());
//					pstmt.setString(3, ((Country) entity).getContinent());
//					pstmt.setString(4, ((Country) entity).getCountryCode());
//					break;
//				case "person":
//
//					pstmt.setString(1, entity.getName());
//					pstmt.setString(2, ((Person) entity).getBirthPlace());
//					pstmt.setString(3, ((Person) entity).getDeathPlace());
//					pstmt.setString(4, ((Person) entity).getResidingPlace());
//					pstmt.setString(5, ((Person) entity).getGender());
//					pstmt.setString(6, list.get(i).getInfo());
//					break;
//				}
//
//				pstmt.addBatch();
//				batchSize++;
//			}
//
//			// execute last batch
//			pstmt.executeBatch();
//			connection.commit();
//		} catch (SQLException e) {
//			e.printStackTrace();
//		} finally {
//
//			// close resources
//			if (stmt != null) {
//				stmt.close();
//			}
//			if (pstmt != null) {
//				pstmt.close();
//			}
//
//			safelySetAutoCommit();
//
//		}
//	}
	
	/**
	 * Inserts a person entry to person table.
	 * 
	 * @param person 	a new person object to be inserted
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws InstantiationException
	 * @throws IllegalAccessException
	 * @throws Exception
	 */
	synchronized public void insertCourses(int course_id, int student_id, int grade)
			throws ClassNotFoundException, SQLException,
			InstantiationException, IllegalAccessException, Exception {
		
		PreparedStatement pstmt = null;
		try {
			// prepare an updating statement
			pstmt = connection.prepareStatement("INSERT INTO courses_students_grades "
					+ "SET course_id=?, student_id=?, grade=?");
						
			// set the updated values
			pstmt.setString(1, Integer.toString(course_id));
			pstmt.setString(2, Integer.toString(student_id));
			pstmt.setString(3, Integer.toString(grade));
			
			pstmt.executeUpdate();
		} catch (SQLException e) {
			e.printStackTrace();
		} finally {
			if (pstmt!=null){
				pstmt.close();
			}
		}
	}
	
	
	/**	 
	 * Updates the details of the people whose name is as updatedPerson's name,
	 * by updatedPerson's details.
	 * 
	 * @param updatedPerson	  the person with the updated details
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws PropertyException
	 * @throws Exception
	 */
//	synchronized public void updatePersonDetails(Person updatedPerson)
//			throws ClassNotFoundException, SQLException, PropertyException,
//			Exception {
//	
//		PreparedStatement pstmt = null;
//		try {
//			// prepare an updating statement
//			pstmt = connection.prepareStatement("UPDATE person "
//					+ "SET born_in=?, died_in=?, lives_in=? "
//					+ "WHERE name=?");
//						
//			// set the updated values
//			pstmt.setString(1, updatedPerson.getBirthPlace());
//			pstmt.setString(2, updatedPerson.getDeathPlace());
//			pstmt.setString(3, updatedPerson.getResidingPlace());
//			pstmt.setString(4, updatedPerson.getName());
//						
//			pstmt.executeUpdate();
//		} catch (SQLException e) {
//			e.printStackTrace();
//		} finally {
//			if (pstmt!=null){
//				pstmt.close();
//			}
//		}
//	}
	
	/**
	 * Searches for the people whose name contains the keyword requested by the user.
	 * 
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws Exception
	 */
//	synchronized void  searchPersonsByName() 
//			throws PropertyException, ClassNotFoundException, SQLException, Exception {
//		
//		results.persons = findPersonsByName(results.key);
//	}
//	
	/**
	 * Searches for the people who related to the place,
	 * whose name contains the keyword requested by the user.
	 * 
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws Exception
	 */
//	synchronized void  searchPersonsByPlace() 
//			throws PropertyException, ClassNotFoundException, SQLException, Exception {
//		
//		results.persons = findPersonsByPlace(results.key);
//	}
	
	/**
	 * Searches for nearby cities of a place related to the person selected by the user.
	 * This place is also selected among three options: birth place / death place / residing place.
	 * In addition, the closeness from this place is as well requested by the user.
	 * 
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws Exception
	 */
//	synchronized void searchNearbyCitiesByPerson() throws ClassNotFoundException,
//			SQLException, Exception {
//		// get the relevant place
//		String place = "";
//		switch (results.selectedPlace) {
//		case BIRTH_PLACE:
//			place = results.selected.getBirthPlace();
//			break;
//		case DEATH_PLACE:
//			place = results.selected.getDeathPlace();
//			break;
//		case RESIDING_PLACE:
//			place = results.selected.getResidingPlace();
//			break;
//		}
//		
//		results.cityResults = findNearbyCitiesByPlaceAndDist(place, results.distance);
//	}
	
	/** wrapper function that rebuilds DB
	 * @param conn
	 * @throws ClassNotFoundException
	 * @throws PropertyException
	 * @throws SQLException
	 * @throws IOException
	 * @throws Exception
	 */
//	public void rebuildDb() throws ClassNotFoundException,
//			PropertyException, SQLException, IOException, Exception {
//		
//		// go over all tables, make them and upload
//		for (String table : Connector.pr.getProp("dbtables").split(",")) {
//			insertEntities(YagoParser.buildListForTable(table), table);
//		}
//
//	}
		
	/**
	 * Opens a new connection with DB.
	 * 
	 * @throws Exception
	 */
	private void openConnection() throws Exception {
		// load the driver
		String driver = "com.mysql.jdbc.Driver";
		try {
			Class.forName(driver).newInstance();
		} catch (ClassNotFoundException e) {
			throw new ClassNotFoundException("Loading driver: " + driver
					+ "have failed: " + e.getMessage());
		}

		// create the connection
		try {
			this.connection = DriverManager.getConnection("jdbc:mysql://"
					+ props.hostAddr + ":" + props.port + "/"
					+ props.schemaName, props.username, props.password);
			System.out.println("connection has been established");
		} catch (SQLException e) {
			throw new SQLException("Error connecting to DB: " + e.getMessage());
		}
	}

	/**
	 * Attempts to close all the given resources.
	 * 
	 * @param resources
	 *            resources to close
	 */
	private void safelyCloseResources(AutoCloseable... resources)
			throws Exception {
		for (AutoCloseable resource : resources) {
			resource.close();
		}
	}

	/**
	 * Attempts to set the connection back to auto-commit.
	 * @throws SQLException 
	 */
	private void safelySetAutoCommit() throws SQLException {
		try {
			connection.setAutoCommit(true);
		} catch (SQLException e) {
			throw new SQLException("Error in setting the connection back to auto-commit: " + e.getMessage());
		}
	}
	
	/**
	 * @param keyword
	 * 			- the string to be searched in DB
	 * @return a list of all of the people whose name contains keyword in person table  
	 * @throws PropertyException
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws Exception
	 */
//	private List<Person> findPersonsByName(String keyword) 
//			throws PropertyException, ClassNotFoundException, SQLException, Exception {
//		String selectSQL = "SELECT * FROM person WHERE name LIKE '%" + keyword + "%'";
//		
//		return selectPersonsByQuery(selectSQL);
//
//	}
	
	/**
	 * @param keyword
	 * 			- the string to be searched in DB
	 * @return a list of all of the people who died or were born in the place,
	 * 		   whose name contains keyword in person table   
	 * @throws PropertyException
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws Exception
	 */
//	private List<Person> findPersonsByPlace(String keyword) 
//			throws PropertyException, ClassNotFoundException, SQLException, Exception {
//		String selectSQL = "SELECT * FROM person "
//				+ "WHERE born_in LIKE '%" + keyword + "%' OR died_in LIKE '%" + keyword + "%'"
//				+ "OR lives_in LIKE '%" + keyword + "%'";
//
//		return selectPersonsByQuery(selectSQL);
//	}
	
	/**
	 * @param selectSQL
	 * 			- the query to be applied on person table
	 * @return a list of all of the people who meet the conditions of selectSQL query
	 * @throws PropertyException
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws Exception
	 */
////	private List<Person> selectPersonsByQuery(String selectSQL) 
//			throws PropertyException, ClassNotFoundException, SQLException, Exception {
//		// open connection, if needed
//		if (this.connection == null) {
//			openConnection();
//		}
//
//		Statement stmt = null;
//		ResultSet rs = null;
//
//		List<Person> persons = new ArrayList<>();
//		try {
//			stmt = connection.createStatement();
//			rs = stmt.executeQuery(selectSQL + " LIMIT " + MAX_BATCH_SIZE);
//
//			while (rs.next() == true) {
//				Person person = new Person(rs.getString("name"));
//				
//				// set person fields
//				person.setBirthPlace(rs.getString("born_in"));
//				person.setDeathPlace(rs.getString("died_in"));
//				person.setResidingPlace(rs.getString("lives_in"));
//				person.setGender(rs.getString("gender"));
//				person.setInfo(rs.getString("info"));
//				
//				persons.add(person);
//			}
//		} catch (SQLException e) {
//			throw new SQLException("ERROR in execution a query - "
//					+ e.getMessage());
//		} finally {
//			safelyCloseResources(rs, stmt);
//		}
//
//		return persons;
//	}
	
	/**
	 * @param place		a source city
	 * @param distance	a distance in kilometers
	 * @return a list of the city names that far from place by at most dist km.
	 * @throws ClassNotFoundException
	 * @throws SQLException
	 * @throws Exception
	 */
////	private List<String> findNearbyCitiesByPlaceAndDist(String place, double dist)
////			throws ClassNotFoundException, SQLException, Exception {
////		// open connection, if needed
////		if (this.connection == null) {
////			openConnection();
////		}
////
////		Statement stmt = null;
////		ResultSet rs = null;
////
////		List<String> cities = new ArrayList<>();
//		try {
//			stmt = connection.createStatement();
//			rs = stmt.executeQuery(makeSelectQueryByPlaceAndDist(place, dist));
//
//			while (rs.next() == true) {
//				cities.add(rs.getString("city_name"));
//			}
//		} catch (SQLException e) {
//			throw new SQLException("ERROR in execution a query - "
//					+ e.getMessage());
//		} finally {
//			safelyCloseResources(rs, stmt);
//		}
//
//		return cities;
//	}
	
	/**
	 * @param place		a source city
	 * @param distance	a distance in kilometers
	 * @return a query that returns the cities in city table named tableName,
	 * 		   that far from place by at most dist km.
	 */
////	private String makeSelectQueryByPlaceAndDist(String place, double dist) {
////		String selectSQL = "SELECT distance.city_name "
////				+ "FROM " 
////					+ "(SELECT b.city_name, "
////						+ "111.1111 * DEGREES(ACOS(COS(RADIANS(a.latitude)) " 
////						+ "* COS(RADIANS(b.latitude)) "
////						+ "* COS(RADIANS(a.longitude - b.longitude)) " 
////						+ "+ SIN(RADIANS(a.latitude)) " 
//						+ "* SIN(RADIANS(b.latitude)))) AS distance_in_km "
//			        + "FROM city AS a, city AS b " 
//			        + "WHERE a.city_name = '" + place + "' "
//			        + ") AS distance "
//			  + "WHERE distance.distance_in_km <= " + dist;
//		
//		return selectSQL;
//	}

	public void run() {
		try {
			openConnection();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
}
