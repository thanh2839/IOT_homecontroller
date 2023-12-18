package com.example.boss.service.impl;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.example.boss.dto.LogDto;
import com.example.boss.entity.Log;
import com.example.boss.entity.User;
import com.example.boss.repository.LogRepository;
import com.example.boss.service.LogService;
import com.example.boss.util.ImageUtil;

@Service
public class LogServiceImpl implements LogService {

    private LogRepository logRepository;

    public LogServiceImpl(LogRepository logRepository) {
        super();
        this.logRepository = logRepository;
    }

    @Override
    public void saveLog(Boolean status, MultipartFile image, User user) {
        Log log = new Log();
        log.setCreatedDate(LocalDateTime.now());
        log.setStatus(status);
        log.setImage(ImageUtil.compressImage(image));
        log.setUser(user);
        logRepository.save(log);
    }

    @Override
    public List<LogDto> findLogsByUserId(Long id) {
        List<Log> logs = logRepository.findByUserId(id);
        return logs.stream()
                .map((log) -> mapToLogDto(log))
                .collect(Collectors.toList());
    }
    @Override
    public LogDto mapToLogDto(Log log) {
        LogDto logDto = new LogDto();
        logDto.setId(log.getId());
        logDto.setCreatedDate(log.getCreatedDate());
        logDto.setStatus(log.getStatus());
        logDto.setImage(ImageUtil.decompressImage(log.getImage()));
        return logDto;
    }
}
