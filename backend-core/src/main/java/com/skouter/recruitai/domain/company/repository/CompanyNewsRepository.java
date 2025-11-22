package com.skouter.recruitai.domain.company.repository;

import com.skouter.recruitai.domain.company.entity.CompanyNews;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 기업 뉴스 저장소
 * - 기업 뉴스 데이터 접근
 */
@Repository
public interface CompanyNewsRepository extends JpaRepository<CompanyNews, Long> {

    /**
     * 기업 ID로 뉴스 목록 조회
     *
     * @param companyId 기업 ID
     * @return 뉴스 엔티티 목록
     */
    List<CompanyNews> findByCompanyIdOrderByPublishedDateDesc(Long companyId);

    /**
     * 기업 ID와 제목으로 뉴스 조회
     *
     * @param companyId 기업 ID
     * @param title 제목
     * @return 뉴스 목록
     */
    List<CompanyNews> findByCompanyIdAndTitleContaining(Long companyId, String title);
}
