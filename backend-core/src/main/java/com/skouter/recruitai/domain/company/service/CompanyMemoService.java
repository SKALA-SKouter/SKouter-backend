package com.skouter.recruitai.domain.company.service;

import com.skouter.recruitai.domain.company.entity.CompanyMemo;
import com.skouter.recruitai.domain.company.repository.CompanyMemoRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 기업 메모 서비스
 * - 기업 메모 조회, 생성, 수정, 삭제 등 비즈니스 로직 처리
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class CompanyMemoService {

    private final CompanyMemoRepository companyMemoRepository;

    /**
     * 사용자의 기업 메모 조회
     *
     * @param companyId 기업 ID
     * @param userId 사용자 ID
     * @return 메모 엔티티
     */
    public CompanyMemo getMemo(Long companyId, Long userId) {
        return companyMemoRepository.findByCompanyIdAndUserId(companyId, userId)
                .orElse(null);
    }

    /**
     * 기업별 모든 메모 조회
     *
     * @param companyId 기업 ID
     * @return 메모 엔티티 목록
     */
    public List<CompanyMemo> getMemosByCompanyId(Long companyId) {
        return companyMemoRepository.findByCompanyId(companyId);
    }

    /**
     * 사용자의 모든 메모 조회
     *
     * @param userId 사용자 ID
     * @return 메모 엔티티 목록
     */
    public List<CompanyMemo> getMemosByUserId(Long userId) {
        return companyMemoRepository.findByUserId(userId);
    }

    /**
     * 메모 생성 또는 업데이트
     *
     * @param companyId 기업 ID
     * @param userId 사용자 ID
     * @param content 메모 내용
     * @return 메모 엔티티
     */
    @Transactional
    public CompanyMemo saveMemo(Long companyId, Long userId, String content) {
        CompanyMemo memo = companyMemoRepository.findByCompanyIdAndUserId(companyId, userId)
                .orElse(CompanyMemo.builder()
                        .companyId(companyId)
                        .userId(userId)
                        .content(content)
                        .build());

        if (memo.getId() != null) {
            memo.updateContent(content);
        } else {
            memo = CompanyMemo.builder()
                    .companyId(companyId)
                    .userId(userId)
                    .content(content)
                    .build();
        }

        return companyMemoRepository.save(memo);
    }

    /**
     * 메모 삭제
     *
     * @param memoId 메모 ID
     */
    @Transactional
    public void deleteMemo(Long memoId) {
        companyMemoRepository.deleteById(memoId);
    }
}
