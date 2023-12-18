package com.example.boss.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.boss.entity.Log;

public interface LogRepository extends JpaRepository<Log, Long> {
    List<Log> findByUserId(Long userId);
}