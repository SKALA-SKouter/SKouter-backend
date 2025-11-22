package com.skouter.recruitai.domain.job.repository;

import com.skouter.recruitai.domain.job.entity.Skill;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 기술 스택 저장소
 * - 기술 스택 데이터 접근
 */
@Repository
public interface SkillRepository extends JpaRepository<Skill, Long> {

    /**
     * 공고 ID로 기술 스택 목록 조회
     *
     * @param jobId 공고 ID
     * @return 기술 스택 목록
     */
    List<Skill> findByJobId(Long jobId);

    /**
     * 기술명으로 검색
     *
     * @param name 기술명
     * @return 기술 스택 목록
     */
    List<Skill> findByName(String name);

    /**
     * 공고 ID로 기술 스택 삭제
     *
     * @param jobId 공고 ID
     */
    void deleteByJobId(Long jobId);
}
