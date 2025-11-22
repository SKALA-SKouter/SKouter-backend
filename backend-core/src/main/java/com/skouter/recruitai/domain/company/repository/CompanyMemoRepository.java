package com.skouter.recruitai.domain.company.repository;

import com.skouter.recruitai.domain.company.entity.CompanyMemo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 기업 메모 저장소
 * - 기업 메모 데이터 접근
 */
@Repository
public interface CompanyMemoRepository extends JpaRepository<CompanyMemo, Long> {

    /**
     * 기업 ID와 사용자 ID로 메모 조회
     *
     * @param companyId 기업 ID
     * @param userId 사용자 ID
     * @return 메모 엔티티
     */
    Optional<CompanyMemo> findByCompanyIdAndUserId(Long companyId, Long userId);

    /**
     * 기업 ID로 메모 목록 조회
     *
     * @param companyId 기업 ID
     * @return 메모 엔티티 목록
     */
    List<CompanyMemo> findByCompanyId(Long companyId);

    /**
     * 사용자 ID로 메모 목록 조회
     *
     * @param userId 사용자 ID
     * @return 메모 엔티티 목록
     */
    List<CompanyMemo> findByUserId(Long userId);
}
