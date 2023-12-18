package com.example.boss.controller;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import com.example.boss.dto.UserDto;
import com.example.boss.entity.User;
import com.example.boss.service.DoorService;
import com.example.boss.service.EmailSenderService;
import com.example.boss.service.LogService;
import com.example.boss.service.UserService;

import org.springframework.web.bind.annotation.PostMapping;

@RestController
@RequestMapping("/api")
public class APIController {
    private UserService userService;
    private LogService logService;
    private DoorService doorService;
    private EmailSenderService emailSenderService;

    public APIController(UserService userService, DoorService doorService, LogService logService,
            EmailSenderService emailSenderService) {
        this.userService = userService;
        this.doorService = doorService;
        this.logService = logService;
        this.emailSenderService = emailSenderService;
    }

    @ModelAttribute("currentUser")
    public User currentUser(Authentication auth) {
        if (auth == null) {
            return new User();
        }
        User currentUser = userService.findUserByEmail(auth.getName());
        return currentUser;
    }

    @ModelAttribute("isAdmin")
    public Boolean isAdmin(Authentication auth) {
        if (auth == null) {
            return false;
        }
        for (GrantedAuthority authority : auth.getAuthorities()) {
            if (authority.getAuthority().equals("ROLE_ADMIN")) {
                return true;
            }
        }
        return false;
    }

    @PostMapping("/logFace")
    public String saveFile(@RequestParam("file") MultipartFile file, @RequestParam("status") String status,
            Authentication auth) {
        User user = currentUser(auth);
        if (user.getName() != null) {
            System.out.println(status);
            Boolean check = null;
            if ("Real".equals(status))
                check = true;
            else if ("Fake".equals(status))
                check = false;
            logService.saveLog(check, file, user);
            if (check == null || !check) {
                emailSenderService.sendMail(user.getEmail(), "Cảnh báo IOT",
                        "Phát hiện truy cập cửa IOT không thành công");
            }
            return "Save log success";
        }
        return "Access denied";
    }

    @GetMapping("/open-door")
    public String openDoor(Authentication auth) {
        User user = currentUser(auth);
        if (user.getName() != null) {
            doorService.open("True");
            return "Opened";
        }
        return "Access denied";

    }

    @GetMapping("/close-door")
    public String closeDoor(Authentication auth) {
        User user = currentUser(auth);
        if (user.getName() != null) {
            doorService.open("False");
            return "Closed";
        }
        return "Access denied";
    }

    @GetMapping("/getStatus")
    public String getStatus(Authentication auth) {
        User user = currentUser(auth);
        if (user.getName() != null) {
            return String.valueOf(user.getStatus());
        }
        return "Access denied";
    }

    @PostMapping("/status")
    public String setStatus(@RequestParam("status") boolean status,
            Authentication auth) {
        User user = currentUser(auth);
        if (user.getName() != null) {
            user.setStatus(status);
            UserDto userDto = userService.mapToUserDto(user);
            userService.updateUser(userDto, user.getId());
            doorService.sendStatus(userDto);
            return "Status updated";
        }
        return "Access denied";
    }

}
