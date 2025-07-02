package com.example.db_change;

import java.time.LocalDateTime;

import org.springframework.stereotype.Component;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
public class NotifLog{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int changeId;

    private long registrationId;
    private  String tableName;
    private String operation;
    private String rowId;
    private LocalDateTime modifiedAt;

    @PrePersist
    protected void onCreate() {
        this.modifiedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        this.modifiedAt = LocalDateTime.now();
    }
    



    
}
