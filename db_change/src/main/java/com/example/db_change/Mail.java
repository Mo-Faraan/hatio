package com.example.db_change;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Component;
import org.springframework.mail.javamail.JavaMailSenderImpl;
import java.util.Properties;



public class Mail {

   // @Autowired
   // private JavaMailSender javaMailSender;

   // @Value("${spring.mail.username}") 
   // private String sender;

   // public String sendSimpleMail() {
   //    try {
   //       SimpleMailMessage mailMessage = new SimpleMailMessage();

   //       mailMessage.setFrom(sender);
   //       mailMessage.setTo("mdfarhantm29@gmail.com");
   //       mailMessage.setText("hdbchdbh");
   //       mailMessage.setSubject("hsdbchcb");

   //       javaMailSender.send(mailMessage);
   //       return "Mail Sent Successfully...";
   //    } catch (Exception e) {
   //       System.out.println(e);
   //       return "Error while Sending Mail";
   //    }
   // }
/*
To use JavaMailSender manually (without Spring components/beans), you need to instantiate and configure it yourself.
Below is an example of how you can do this using JavaMailSenderImpl.
*/


public void sendSimpleMail() {
   JavaMailSenderImpl mailSender = new JavaMailSenderImpl();
   mailSender.setHost("smtp.gmail.com"); // Set your SMTP host
   mailSender.setPort(587); // Set your SMTP port
   mailSender.setUsername("farhantest29@gmail.com"); // Set your email
   mailSender.setPassword("xpyp jntd tjgs hrzq"); // Set your password

   Properties props = mailSender.getJavaMailProperties();
   props.put("mail.transport.protocol", "smtp");
   props.put("mail.smtp.auth", "true");
   props.put("mail.smtp.starttls.enable", "true");
   props.put("mail.debug", "true");

   try {
      SimpleMailMessage mailMessage = new SimpleMailMessage();
      mailMessage.setFrom("your_email@example.com");
      mailMessage.setTo("mdfarhantm29@gmail.com");
      mailMessage.setText("hdbchdbh");
      mailMessage.setSubject("hsdbchcb");

      mailSender.send(mailMessage);
      System.out.println("Mail Sent Successfully...");
   } catch (Exception e) {
      System.out.println(e);
      System.out.println("Error while Sending Mail");
   }
}
}
   