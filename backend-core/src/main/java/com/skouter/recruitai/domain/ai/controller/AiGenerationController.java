package com.skouter.recruitai.domain.ai.controller;

import com.skouter.recruitai.domain.ai.dto.request.JobGenerationRequest;
import com.skouter.recruitai.domain.ai.dto.response.AiTaskResponse;
import com.skouter.recruitai.domain.ai.service.AiTaskService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * AI 생성 관련 API 엔드포인트
 * - 공고 생성, 자동 작성 등
 */
@RestController
@RequestMapping("/api/ai/generation")
@RequiredArgsConstructor
public class AiGenerationController {

    private final AiTaskService aiTaskService;

    /**
     * 공고 생성 요청
     *
     * @param request 생성 요청 DTO
     * @return 작업 응답 (Task ID)
     */
    @PostMapping
    public ResponseEntity<ApiResponse<AiTaskResponse>> requestGeneration(
            @RequestBody JobGenerationRequest request) {
        AiTaskResponse response = aiTaskService.requestGeneration(request);
        return ResponseEntity.status(HttpStatus.ACCEPTED).body(ApiResponse.ok(response));
    }

    /**
     * 템플릿 기반 공고 생성
     *
     * @param templateId 템플릿 ID
     * @param companyId 기업 ID
     * @return 작업 응답 (Task ID)
     */
    @PostMapping("/from-template")
    public ResponseEntity<ApiResponse<AiTaskResponse>> generateFromTemplate(
            @RequestParam Long templateId,
            @RequestParam Long companyId) {
        JobGenerationRequest request = JobGenerationRequest.builder()
                .templateId(templateId)
                .companyId(companyId)
                .build();

        AiTaskResponse response = aiTaskService.requestGeneration(request);
        return ResponseEntity.status(HttpStatus.ACCEPTED).body(ApiResponse.ok(response));
    }
}
