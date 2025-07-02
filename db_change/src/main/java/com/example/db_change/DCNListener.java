// package com.example.db_change;

// import java.sql.DriverManager;
// import java.sql.ResultSet;
// import java.sql.SQLException;
// import java.sql.Statement;
// import java.util.Properties;

// import org.springframework.beans.factory.annotation.Autowired;
// import org.springframework.beans.factory.annotation.Value;
// import org.springframework.boot.context.event.ApplicationReadyEvent;
// import org.springframework.context.event.EventListener;
// import org.springframework.stereotype.Component;

// import jakarta.annotation.PreDestroy;
// import oracle.jdbc.OracleConnection;
// import oracle.jdbc.OracleStatement;
// import oracle.jdbc.dcn.DatabaseChangeEvent;
// import oracle.jdbc.dcn.DatabaseChangeListener;
// import oracle.jdbc.dcn.DatabaseChangeRegistration;
// import oracle.jdbc.dcn.QueryChangeDescription;
// import oracle.jdbc.dcn.RowChangeDescription;
// import oracle.jdbc.dcn.TableChangeDescription;
 
// @Component
// public class DCNListener {
 
//     @Value("${spring.datasource.url}")
//     private String dbUrl;
 
//     @Value("${spring.datasource.username}")
//     private String dbUser;

//     @Value("${spring.datasource.password}")
//     private String dbPassword;
 
//     private OracleConnection conn;
//     private DatabaseChangeRegistration dcr;
 
//     @EventListener(ApplicationReadyEvent.class)
//     public void registerDCN() {
//         try {
//             conn = (OracleConnection) DriverManager.getConnection(dbUrl, dbUser, dbPassword);

//             // For clearing out zombie registrations - if exists :
//             try (Statement stmt = conn.createStatement()){
//                 ResultSet rs = stmt.executeQuery("select regid,callback from USER_CHANGE_NOTIFICATION_REGS");
//                 while(rs.next()){
//                     long regid = rs.getLong(1);
//                     String callback = rs.getString(2);
//                     System.out.println("Reg id = " + regid);
//                     System.out.println("Callback = " + callback);
//                     ((OracleConnection)conn).unregisterDatabaseChangeNotification(regid,callback);
//                 }
//             } catch (SQLException e) {
//                 System.out.println(e);
//             }

//             Properties prop = new Properties();
//             prop.setProperty(OracleConnection.DCN_NOTIFY_ROWIDS, "true");   //Includes Row level details in the notification
//             prop.setProperty(OracleConnection.DCN_QUERY_CHANGE_NOTIFICATION, "true"); // Helps to selevctively monitor specific columns or rows. Without this only table level changes will be monitored
//             dcr = conn.registerDatabaseChangeNotification(prop);

//             dcr.addListener(new DatabaseChangeListener() {
//                 @Override
//                 public void onDatabaseChangeNotification(DatabaseChangeEvent event) {
//                     System.out.println("\nDatabase event receieved : \n");
//                     QueryChangeDescription[] queryChanges = event.getQueryChangeDescription();
//                     if (queryChanges == null) {
//                         return;
//                     }
//                     for (QueryChangeDescription queryChange : queryChanges) {
//                         TableChangeDescription[] tableChanges = queryChange.getTableChangeDescription(); 
//                         if (tableChanges != null) {
//                             for (TableChangeDescription tableChange : tableChanges) {
//                                 String tableName = tableChange.getTableName();
//                                 RowChangeDescription[] rowChanges = tableChange.getRowChangeDescription();
//                                 if (rowChanges != null) {
//                                     for (RowChangeDescription rowChange : rowChanges) {
//                                         String rowid = rowChange.getRowid().stringValue();
//                                         System.out.println("Changed Table: "+ tableName);
//                                         System.out.println("Changed ROWID: " + rowid);
//                                     }
//                                 }
//                             }
//                         }
//                     }
//                 }
//             });
            
//             try {
//                 Statement stmt = conn.createStatement();
//                 ((OracleStatement) stmt).setDatabaseChangeRegistration(dcr);
//                 stmt.execute("SELECT IS_ACTIVE FROM CONFIG"); 
//             } catch (Exception e) {
//                 e.printStackTrace();
//             }

//             System.out.println("\nDCN registration complete. Listening for changes.");
//             System.out.println("Registration ID: " + dcr.getRegId());

//         } catch (SQLException e) {
//             e.printStackTrace(); 
//         }
//     }

//     @PreDestroy
//     public void unregisterDCN() {
//         try {
//             if (conn != null && dcr != null) {
//                 conn.unregisterDatabaseChangeNotification(dcr);
//                 System.out.println("DCN unregistered successfully.");
//                 conn.close();
//             }
//         } catch (SQLException e) {
//             e.printStackTrace();
//         }
//     }
// }