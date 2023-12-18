package com.example.boss.controller;

import java.util.Collections;
import java.util.List;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;

import com.example.boss.dto.LogDto;
import com.example.boss.entity.User;
import com.example.boss.service.LogService;
import com.example.boss.service.UserService;

@Controller
public class LogController {
    private UserService userService;
    private LogService logService;

    public LogController(UserService userService, LogService logService) {
        this.userService = userService;
        this.logService = logService;
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

    @GetMapping("/user/logs")
    public String logs(Model model, Authentication auth) {
        User currentUser = currentUser(auth);
        List<LogDto> logs = logService.findLogsByUserId(currentUser.getId());
        Collections.reverse(logs);
        model.addAttribute("logs", logs);
        return "logs";
    }

}
