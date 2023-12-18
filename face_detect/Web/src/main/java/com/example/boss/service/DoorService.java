package com.example.boss.service;

import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.stereotype.Service;

import com.example.boss.dto.UserDto;

@Service
public class DoorService {

    private SimpMessagingTemplate messagingTemplate;

    public DoorService(SimpMessagingTemplate messagingTemplate) {
        this.messagingTemplate = messagingTemplate;
    }

    public void open(String status) {
        messagingTemplate.convertAndSend("/topic/true", status);
    }
    public void sendStatus(UserDto userDto) {
        messagingTemplate.convertAndSend("/topic/status", userDto);
    }
}

