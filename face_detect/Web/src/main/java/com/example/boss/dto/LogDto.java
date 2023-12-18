package com.example.boss.dto;

import java.time.LocalDateTime;

public class LogDto {
    private Long id;
    private Boolean status;
    private LocalDateTime createdDate;
    private String image;
    public LogDto() {
    }
    public LogDto(Long id, Boolean status, LocalDateTime createdDate, String image) {
        this.id = id;
        this.status = status;
        this.createdDate = createdDate;
        this.image = image;
    }
    public Long getId() {
        return id;
    }
    public void setId(Long id) {
        this.id = id;
    }
    public Boolean getStatus() {
        return status;
    }
    public void setStatus(Boolean status) {
        this.status = status;
    }
    public LocalDateTime getCreatedDate() {
        return createdDate;
    }
    public void setCreatedDate(LocalDateTime createdDate) {
        this.createdDate = createdDate;
    }
    public String getImage() {
        return image;
    }
    public void setImage(String image) {
        this.image = image;
    }
    
}
