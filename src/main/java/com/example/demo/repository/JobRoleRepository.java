package com.example.demo.repository;

import com.example.demo.entity.JobRole;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 직무 역할 데이터 접근
 */
@Repository
public interface JobRoleRepository extends JpaRepository<JobRole, Long> {
}
