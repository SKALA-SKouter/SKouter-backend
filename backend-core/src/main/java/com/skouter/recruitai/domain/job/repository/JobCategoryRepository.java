package com.skouter.recruitai.domain.job.repository;

import com.skouter.recruitai.domain.job.entity.JobCategory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 채용 공고 카테고리 저장소
 * - 공고 카테고리 데이터 접근
 */
@Repository
public interface JobCategoryRepository extends JpaRepository<JobCategory, Long> {

    /**
     * 공고 ID로 카테고리 목록 조회
     *
     * @param jobId 공고 ID
     * @return 카테고리 목록
     */
    List<JobCategory> findByJobId(Long jobId);

    /**
     * 카테고리명으로 검색
     *
     * @param category 카테고리명
     * @return 카테고리 목록
     */
    List<JobCategory> findByCategory(String category);

    /**
     * 공고 ID로 카테고리 삭제
     *
     * @param jobId 공고 ID
     */
    void deleteByJobId(Long jobId);
}
