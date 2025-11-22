package com.skouter.recruitai.domain.dashboard.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 대시보드 요약 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class DashboardSummaryResponse {

    /**
     * 총 북마크 개수
     */
    private Long totalBookmarks;

    /**
     * 공고 총 개수
     */
    private Long totalJobs;

    /**
     * 회사 총 개수
     */
    private Long totalCompanies;

    /**
     * 인기 기술 스택
     */
    private Object popularSkills;

    /**
     * 최근 활동
     */
    private Object recentActivity;
}
