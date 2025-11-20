package com.example.demo.repository;

import com.example.demo.entity.JobPostSkill;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 채용공고-스킬 데이터 접근
 */
@Repository
public interface JobPostSkillRepository extends JpaRepository<JobPostSkill, Long> {
}
