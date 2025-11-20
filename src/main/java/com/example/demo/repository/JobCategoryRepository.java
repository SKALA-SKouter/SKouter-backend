package com.example.demo.repository;

import com.example.demo.entity.JobCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 직무 카테고리 데이터 접근
 */
@Repository
public interface JobCategoryRepository extends JpaRepository<JobCategory, Long> {
}
