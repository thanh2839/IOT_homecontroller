package com.example.boss.service.impl;

import java.util.Arrays;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.Collectors;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.example.boss.dto.UserDto;
import com.example.boss.entity.Role;
import com.example.boss.entity.User;
import com.example.boss.repository.RoleRepository;
import com.example.boss.repository.UserRepository;
import com.example.boss.service.UserService;

@Service
public class UserServiceImpl implements UserService {

    private UserRepository userRepository;
    private RoleRepository roleRepository;
    private PasswordEncoder passwordEncoder;

    public UserServiceImpl(UserRepository userRepository, RoleRepository roleRepository,
            PasswordEncoder passwordEncoder) {
        super();
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void saveUser(UserDto userDto) {
        User user = new User();
        user.setName(userDto.getName());
        user.setEmail(userDto.getEmail());
        user.setEmail(userDto.getEmail());
        user.setPassword(passwordEncoder.encode(userDto.getPassword()));
        user.setStatus(false);
        List<Role> roles = new ArrayList<>();
        for (String roleName : Arrays.asList("ROLE_USER")) {
            Role role = roleRepository.findByName(roleName);
            if (role == null) {
                role = createRole(roleName);
            }
            roles.add(role);
        }
        user.setRoles(roles);
        userRepository.save(user);

    }

    @Override
    public void updateUser(UserDto userDto, Long id) {
        User user = userRepository.findById(id).orElse(null);
        user.setName(userDto.getName());
        user.setEmail(userDto.getEmail());
        userRepository.save(user);
    }

    @Override
    public void changePassword(UserDto userDto, Long id) {
        User user = userRepository.findById(id).orElse(null);
        user.setPassword(passwordEncoder.encode(userDto.getPassword()));
        userRepository.save(user);
    }

    @Override
    public User findUserByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    @Override
    public User findUserById(Long id) {
        return userRepository.findById(id).orElse(null);
    }

    @Override
    public List<UserDto> findAllUsers() {
        List<User> users = userRepository.findAll();
        return users.stream()
                .map((user) -> mapToUserDto(user))
                .collect(Collectors.toList());
    }

    @Override
    public UserDto mapToUserDto(User user) {
        UserDto userDto = new UserDto();
        userDto.setId(user.getId());
        userDto.setName(user.getName());
        userDto.setEmail(user.getEmail());
        userDto.setStatus(user.getStatus());
        return userDto;
    }

    private Role createRole(String roleName) {
        Role role = new Role();
        role.setName(roleName);
        return roleRepository.save(role);
    }

    @Override
    public void deleteUser(Long id) {
        User user = userRepository.findById(id).orElse(null);
        user.getRoles().clear();
        userRepository.delete(user);
    }

}
