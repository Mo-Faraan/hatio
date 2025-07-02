package com.example.cron_jobs;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@SpringBootApplication
public class CronJobsApplication {

	public static void main(String[] args) {
		SpringApplication.run(CronJobsApplication.class, args);
	}

}
