package com.example.boss.service;

import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import com.example.boss.dto.LogDto;
import com.example.boss.entity.Log;
import com.example.boss.entity.User;

public interface LogService {
    void saveLog(Boolean status, MultipartFile image, User user);
    LogDto mapToLogDto(Log log);
    List<LogDto> findLogsByUserId(Long id);
}
