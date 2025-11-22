package com.skouter.recruitai.domain.job.repository;

import com.skouter.recruitai.domain.job.entity.Job;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 채용 공고 저장소
 * - 채용 공고 데이터 접근
 */
@Repository
public interface JobRepository extends JpaRepository<Job, Long> {

    /**
     * 기업 ID로 채용 공고 목록 조회
     *
     * @param companyId 기업 ID
     * @param pageable 페이징 정보
     * @return 채용 공고 페이지
     */
    Page<Job> findByCompanyId(Long companyId, Pageable pageable);

    /**
     * 채용 공고 제목으로 검색
     *
     * @param title 제목
     * @param pageable 페이징 정보
     * @return 채용 공고 페이지
     */
    Page<Job> findByTitleContaining(String title, Pageable pageable);

    /**
     * 활성화된 채용 공고 목록 조회
     *
     * @param isActive 활성 상태
     * @param pageable 페이징 정보
     * @return 채용 공고 페이지
     */
    Page<Job> findByIsActive(Boolean isActive, Pageable pageable);

    /**
     * 기업과 제목으로 검색
     *
     * @param companyId 기업 ID
     * @param title 제목
     * @return 채용 공고 목록
     */
    List<Job> findByCompanyIdAndTitleContaining(Long companyId, String title);
}
