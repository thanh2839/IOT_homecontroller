package com.example.boss.controller;



import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import com.example.boss.dto.UserDto;
import com.example.boss.entity.User;
import com.example.boss.service.UserService;

import jakarta.validation.Valid;


@Controller
public class AuthController {

    private UserService userService;

    public AuthController(UserService userService) {
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
   
    
    @GetMapping("/")
    public String home(){
        return "index";
    }

   
    @GetMapping("/login")
    public String login(){
        return "login";
    }
   
    
    @GetMapping("/register")
    public String showRegistrationForm(Model model){
      
        UserDto user = new UserDto();
        model.addAttribute("user", user);
        return "register";
    }

    @PostMapping("/register/save")
    public String registration(@Valid @ModelAttribute("user") UserDto userDto,
                               BindingResult result,
                               Model model){
        User existingUser = userService.findUserByEmail(userDto.getEmail());

        if(existingUser != null && existingUser.getEmail() != null && !existingUser.getEmail().isEmpty()){
            result.rejectValue("email", null,
                    "There is already an account registered with the same email");
        }

        if(result.hasErrors()){
            model.addAttribute("user", userDto);
            return "/register";
        }

        userService.saveUser(userDto);
        return "login";
    }

    
}