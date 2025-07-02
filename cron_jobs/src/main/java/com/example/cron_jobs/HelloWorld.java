package com.example.cron_jobs;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class HelloWorld {
    
    @Scheduled(cron = "${cron.job}")
    public void printHello(){
        System.out.println("Hello World!");
    }
}
