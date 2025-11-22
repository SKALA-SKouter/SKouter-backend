package com.skouter.recruitai.domain.ai.controller;

import com.skouter.recruitai.domain.ai.dto.request.JobAnalysisRequest;
import com.skouter.recruitai.domain.ai.dto.response.AiTaskResponse;
import com.skouter.recruitai.domain.ai.dto.response.AiTaskStatusResponse;
import com.skouter.recruitai.domain.ai.service.AiTaskService;
import com.skouter.recruitai.domain.ai.service.AiTaskStatusService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * AI 분석 관련 API 엔드포인트
 * - 공고 분석, 뉴스 요약 등
 */
@RestController
@RequestMapping("/api/ai/analysis")
@RequiredArgsConstructor
public class AiAnalysisController {

    private final AiTaskService aiTaskService;
    private final AiTaskStatusService aiTaskStatusService;

    /**
     * 공고 분석 요청
     *
     * @param request 분석 요청 DTO
     * @return 작업 응답 (Task ID)
     */
    @PostMapping
    public ResponseEntity<ApiResponse<AiTaskResponse>> requestAnalysis(
            @RequestBody JobAnalysisRequest request) {
        AiTaskResponse response = aiTaskService.requestAnalysis(request);
        return ResponseEntity.status(HttpStatus.ACCEPTED).body(ApiResponse.ok(response));
    }

    /**
     * 분석 작업 상태 조회
     *
     * @param taskId 작업 ID
     * @return 작업 상태
     */
    @GetMapping("/status/{taskId}")
    public ResponseEntity<ApiResponse<AiTaskStatusResponse>> getAnalysisStatus(
            @PathVariable String taskId) {
        AiTaskStatusResponse response = aiTaskStatusService.getTaskStatus(taskId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 분석 결과 조회
     *
     * @param taskId 작업 ID
     * @return 분석 결과
     */
    @GetMapping("/result/{taskId}")
    public ResponseEntity<ApiResponse<Object>> getAnalysisResult(@PathVariable String taskId) {
        Object result = aiTaskStatusService.getTaskResult(taskId);
        return ResponseEntity.ok(ApiResponse.ok(result));
    }

    /**
     * 분석 작업 취소
     *
     * @param taskId 작업 ID
     * @return 성공 응답
     */
    @DeleteMapping("/{taskId}")
    public ResponseEntity<ApiResponse<Void>> cancelAnalysis(@PathVariable String taskId) {
        aiTaskStatusService.cancelTask(taskId);
        return ResponseEntity.ok(ApiResponse.ok());
    }
}
