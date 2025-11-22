package com.skouter.recruitai.domain.company.repository;

import com.skouter.recruitai.domain.company.entity.Company;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 기업 저장소
 * - 기업 데이터 접근
 */
@Repository
public interface CompanyRepository extends JpaRepository<Company, Long> {

    /**
     * 기업명으로 기업 조회
     *
     * @param name 기업명
     * @return 기업 엔티티
     */
    Optional<Company> findByName(String name);

    /**
     * 기업명 존재 여부 확인
     *
     * @param name 기업명
     * @return 존재하면 true
     */
    boolean existsByName(String name);
}
