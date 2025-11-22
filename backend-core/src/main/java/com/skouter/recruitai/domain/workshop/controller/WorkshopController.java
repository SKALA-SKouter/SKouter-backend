package com.skouter.recruitai.domain.workshop.controller;

import com.skouter.recruitai.domain.workshop.dto.request.JobGenerateRequest;
import com.skouter.recruitai.domain.workshop.dto.response.JobGenerateResponse;
import com.skouter.recruitai.domain.workshop.dto.response.TemplateListResponse;
import com.skouter.recruitai.domain.workshop.service.TemplateService;
import com.skouter.recruitai.domain.workshop.service.WorkshopService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 공고 제작소 관련 API 엔드포인트
 */
@RestController
@RequestMapping("/api/workshop")
@RequiredArgsConstructor
public class WorkshopController {

    private final WorkshopService workshopService;
    private final TemplateService templateService;

    /**
     * 공고 생성
     */
    @PostMapping("/generate")
    public ResponseEntity<ApiResponse<JobGenerateResponse>> generateJob(
            @RequestBody JobGenerateRequest request) {
        Object result = workshopService.generateJob(request.getTemplateId(), request.getCompanyId());

        JobGenerateResponse response = JobGenerateResponse.builder()
                .taskId(java.util.UUID.randomUUID().toString())
                .status("PENDING")
                .build();

        return ResponseEntity.status(HttpStatus.ACCEPTED).body(ApiResponse.ok(response));
    }

    /**
     * 사용자 템플릿 목록 조회
     */
    @GetMapping("/templates")
    public ResponseEntity<ApiResponse<Object>> getTemplates(@RequestParam Long userId) {
        var templates = workshopService.getUserTemplates(userId);
        return ResponseEntity.ok(ApiResponse.ok(templates));
    }

    /**
     * 템플릿 생성
     */
    @PostMapping("/templates")
    public ResponseEntity<ApiResponse<TemplateListResponse>> createTemplate(
            @RequestParam String name,
            @RequestParam String content,
            @RequestParam(required = false) String description,
            @RequestParam Long userId) {
        var template = templateService.createTemplate(name, content, description, userId);

        TemplateListResponse response = TemplateListResponse.builder()
                .templateId(template.getId())
                .name(template.getName())
                .description(template.getDescription())
                .build();

        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok(response));
    }
}
