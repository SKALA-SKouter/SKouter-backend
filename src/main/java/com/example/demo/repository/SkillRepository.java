package com.example.demo.repository;

import com.example.demo.entity.Skill;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 스킬 데이터 접근
 */
@Repository
public interface SkillRepository extends JpaRepository<Skill, Long> {
}
