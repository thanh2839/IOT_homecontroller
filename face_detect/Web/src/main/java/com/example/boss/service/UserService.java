package com.example.boss.service;

import java.util.List;

import com.example.boss.dto.UserDto;
import com.example.boss.entity.User;

public interface UserService {
    void saveUser(UserDto userDto);
    User findUserByEmail(String email);
    User findUserById(Long id);
    List<UserDto> findAllUsers();
	void updateUser(UserDto userDto, Long id);
	void changePassword(UserDto userDto, Long id);
	void deleteUser(Long id);
	UserDto mapToUserDto(User user);
}


