package com.skouter.recruitai.domain.workshop.repository;

import com.skouter.recruitai.domain.workshop.entity.JobTemplate;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 공고 템플릿 저장소
 */
@Repository
public interface TemplateRepository extends JpaRepository<JobTemplate, Long> {

    List<JobTemplate> findByUserId(Long userId);

    List<JobTemplate> findByNameContaining(String name);
}
