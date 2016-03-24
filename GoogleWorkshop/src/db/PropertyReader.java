package db;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import javax.xml.bind.PropertyException;

public class PropertyReader {
	
	Properties props;
	
	PropertyReader(String fileName) throws IOException{
		props = readDbConfigFile(fileName);
	}
	
	private static Properties readDbConfigFile(String fileName) throws IOException{	
		Properties prop = new Properties();
		InputStream input = null;
			
		try{	
			input = new FileInputStream(fileName);
			
			// load a properties file
			prop.load(input);
	 
		} 
		catch (IOException ex) {
			if (input != null) {
				input.close();
			}
			throw new IOException("Error occured reading file: " + fileName + ". Error: " + ex.getMessage());
		}
		return prop;
	}
	
	public String getProp(String propRequested) throws PropertyException{
		propRequested = propRequested.replace("\"", "").replace(" ", "");
		String res = props.getProperty(propRequested);
		if (res == null){
			throw new PropertyException("Error reading Configs. No property string for: " + propRequested + " was found!");
		}
		return res;
	}

}
