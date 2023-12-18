package com.example.boss.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.boss.entity.Role;

public interface RoleRepository extends JpaRepository<Role, Long> {
	Role findByName(String name);
}
