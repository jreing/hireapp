package db;

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;


public class ConnectionPool {

	public static final List<Connector> conns = new ArrayList<>();
	// public static final SearchResults results = new SearchResults();

	private static Connector getConnection() {
		for (Connector conn : conns) {
			if (!conn.isInUse()) {
				conn.setInUse(true);
				return conn;
			}
		}
		Connector conn = new Connector();
		new Thread(conn).start();
		conns.add(conn);
		return conn;
	}

	public static void closeAll() throws SQLException {
		for (Connector conn : conns) {
			conn.closeConnection();
		}
	}

	// public static synchronized void searchPersonsByName() throws
	// PropertyException, ClassNotFoundException, SQLException, Exception{
	// Connector conn = getConnection();
	// conn.searchPersonsByName();
	// conn.setInUse(false);
	// }
	//
	// public static synchronized void searchPersonsByPlace() throws
	// PropertyException, ClassNotFoundException, SQLException, Exception{
	// Connector conn = getConnection();
	// conn.searchPersonsByPlace();
	// conn.setInUse(false);
	// }
	//
	// public static synchronized void rebuildDataBase() throws
	// ClassNotFoundException, PropertyException, SQLException, IOException,
	// Exception{
	// Connector conn = getConnection();
	// conn.rebuildDb();
	// conn.setInUse(false);
	// }

	public static synchronized void insertCourses(Map<Integer, Integer> map, int student_id) throws ClassNotFoundException, InstantiationException, IllegalAccessException, SQLException, Exception
			 {
		Connector conn = getConnection();
		conn.waitTillConnectionHasBeenEstablished();
		try {
			
			for (Entry<Integer, Integer> e : map.entrySet()) {
				System.out.println("Trying to enter data" + e.getKey() + e.getValue());
				conn.insertCourses(e.getKey(), student_id, e.getValue());
				System.out.println("Data entered");
			}

//		} catch (Exception e) {
//			System.out.println("error"+e.getMessage());
		} finally {
			conn.setInUse(false);
		}

	}

}
