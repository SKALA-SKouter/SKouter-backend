package com.skouter.recruitai.domain.dashboard.controller;

import com.skouter.recruitai.domain.dashboard.dto.response.DashboardSummaryResponse;
import com.skouter.recruitai.domain.dashboard.service.DashboardService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 대시보드 관련 API 엔드포인트
 */
@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {

    private final DashboardService dashboardService;

    /**
     * 대시보드 요약 조회
     */
    @GetMapping("/summary")
    public ResponseEntity<ApiResponse<DashboardSummaryResponse>> getDashboardSummary(
            @RequestParam Long userId) {
        DashboardSummaryResponse response = dashboardService.getDashboardSummary(userId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 회사별 공고 통계
     */
    @GetMapping("/company-stats")
    public ResponseEntity<ApiResponse<Object>> getCompanyStats() {
        Object response = dashboardService.getCompanyJobStats();
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기술 스택 트렌드
     */
    @GetMapping("/skill-trends")
    public ResponseEntity<ApiResponse<Object>> getSkillTrends() {
        Object response = dashboardService.getSkillTrends();
        return ResponseEntity.ok(ApiResponse.ok(response));
    }
}
