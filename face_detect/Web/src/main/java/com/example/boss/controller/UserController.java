package com.example.boss.controller;

import java.util.List;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.example.boss.dto.UserDto;
import com.example.boss.entity.User;
import com.example.boss.service.UserService;

@Controller
public class UserController {

    private UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
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

    @GetMapping("/users")
    public String users(Model model) {
        List<UserDto> users = userService.findAllUsers();
        model.addAttribute("users", users);
        return "users";
    }

    @GetMapping("/user/{id}")
    public String user(Model model, @PathVariable("id") Long id, Authentication auth) {
        User user = userService.findUserById(id);
        User currentUser = currentUser(auth);
        if (currentUser.getId() == id || isAdmin(auth)) {
            model.addAttribute("user", user);
            return "user-edit";
        }
        return "index";
    }

    @PostMapping("/user/save")
    public String updateProfile(Model model, UserDto userDto, @RequestParam(name = "id") Long id, Authentication auth) {
        userService.updateUser(userDto, id);
        return "redirect:/user/" + String.valueOf(id);
    }

    @GetMapping("/user/{id}/changePassword")
    public String showChangePasswordForm(Model model, UserDto userDto, Authentication auth) {
        User user = userService.findUserById(userDto.getId());
        User currentUser = currentUser(auth);
        if (currentUser.getId() == userDto.getId()) {
            model.addAttribute("user", user);
            return "change-password";
        }
        return "index";

    }

    @PostMapping("/user/changePassword")
    public String changePassword(Model model, UserDto userDto, @RequestParam(name = "id") Long id,
            Authentication auth) {
        userService.changePassword(userDto, id);
        return "redirect:/user/" + String.valueOf(id);
    }

    @PostMapping("/user/delete/{id}")
    public String deleteUser(Model model, @PathVariable("id") Long id, Authentication auth) {
        User currentUser = currentUser(auth);
        if (currentUser.getId() != id && !isAdmin(auth)) {
            return "redirect:/";
        }

        if (isAdmin(auth)) {
            userService.deleteUser(id);
            return "redirect:/users";
        }
        userService.deleteUser(id);
        return "redirect:/logout";
    }

}
