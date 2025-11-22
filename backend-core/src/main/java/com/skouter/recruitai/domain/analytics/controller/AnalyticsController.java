package com.skouter.recruitai.domain.analytics.controller;

import com.skouter.recruitai.domain.analytics.dto.response.HistoryResponse;
import com.skouter.recruitai.domain.analytics.dto.response.SkillsResponse;
import com.skouter.recruitai.domain.analytics.dto.response.UploadTimingResponse;
import com.skouter.recruitai.domain.analytics.service.TrendAnalysisService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 분석 관련 API 엔드포인트
 */
@RestController
@RequestMapping("/api/analytics")
@RequiredArgsConstructor
public class AnalyticsController {

    private final TrendAnalysisService trendAnalysisService;

    /**
     * 공고 업로드 시기 분석
     */
    @GetMapping("/upload-timing")
    public ResponseEntity<ApiResponse<UploadTimingResponse>> getUploadTiming() {
        UploadTimingResponse response = trendAnalysisService.analyzeUploadTiming();
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 공고 히스토리
     */
    @GetMapping("/history")
    public ResponseEntity<ApiResponse<HistoryResponse>> getHistory() {
        HistoryResponse response = trendAnalysisService.getHistory();
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기술 스택 분석
     */
    @GetMapping("/skills")
    public ResponseEntity<ApiResponse<SkillsResponse>> getSkillsAnalysis() {
        SkillsResponse response = trendAnalysisService.analyzeSkills();
        return ResponseEntity.ok(ApiResponse.ok(response));
    }
}
