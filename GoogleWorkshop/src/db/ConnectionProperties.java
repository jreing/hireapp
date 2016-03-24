package db;

import javax.xml.bind.PropertyException;

public class ConnectionProperties {
	
	final String schemaName;
	final String hostAddr;
	final String port;
	final String username;
	final String password;
	
	public ConnectionProperties(PropertyReader pr) throws PropertyException{
		this.username = pr.getProp("user");
		this.password = pr.getProp("password");
		this.schemaName = pr.getProp("schema");
		this.hostAddr = pr.getProp("hostAddr");
		this.port = pr.getProp("con_port");
	}

}
