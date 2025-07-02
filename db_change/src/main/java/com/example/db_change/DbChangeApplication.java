package com.example.db_change;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DbChangeApplication {
	
	public static void main(String[] args) {
		SpringApplication.run(DbChangeApplication.class, args);
		Mail mail = new Mail();
		mail.sendSimpleMail();
	}

}
