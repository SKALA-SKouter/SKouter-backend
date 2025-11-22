package com.skouter.recruitai.domain.dashboard.service;

import com.skouter.recruitai.domain.dashboard.dto.response.DashboardSummaryResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 대시보드 서비스
 * - 요약 통계 조회
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class DashboardService {

    /**
     * 대시보드 요약 조회
     *
     * @param userId 사용자 ID
     * @return 대시보드 요약
     */
    public DashboardSummaryResponse getDashboardSummary(Long userId) {
        // TODO: 북마크 개수, 공고 통계, 기술 스택 트렌드 등 조회
        return null;
    }

    /**
     * 회사별 공고 통계
     *
     * @return 회사별 공고 개수
     */
    public Object getCompanyJobStats() {
        // TODO: 회사별 공고 통계 조회
        return null;
    }

    /**
     * 기술 스택 트렌드
     *
     * @return 기술 스택 트렌드 데이터
     */
    public Object getSkillTrends() {
        // TODO: 기술 스택 트렌드 조회
        return null;
    }
}
