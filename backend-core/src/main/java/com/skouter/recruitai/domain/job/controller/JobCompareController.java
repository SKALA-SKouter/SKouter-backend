package com.skouter.recruitai.domain.job.controller;

import com.skouter.recruitai.domain.job.dto.request.JobCompareRequest;
import com.skouter.recruitai.domain.job.dto.response.JobCompareResponse;
import com.skouter.recruitai.domain.job.service.JobCompareService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 채용 공고 비교 관련 API 엔드포인트
 * - 여러 공고 비교, 기술 스택 비교
 */
@RestController
@RequestMapping("/api/jobs/compare")
@RequiredArgsConstructor
public class JobCompareController {

    private final JobCompareService jobCompareService;

    /**
     * 여러 공고 비교
     *
     * @param request 비교 요청 DTO
     * @return 비교 결과
     */
    @PostMapping
    public ResponseEntity<ApiResponse<JobCompareResponse>> compareJobs(
            @RequestBody JobCompareRequest request) {
        JobCompareResponse response = jobCompareService.compareJobs(request.getJobIds());
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 두 개 공고 비교
     *
     * @param jobId1 첫 번째 공고 ID
     * @param jobId2 두 번째 공고 ID
     * @return 비교 결과
     */
    @GetMapping("/two")
    public ResponseEntity<ApiResponse<JobCompareResponse>> compareTwo(
            @RequestParam Long jobId1,
            @RequestParam Long jobId2) {
        JobCompareResponse response = jobCompareService.compareTwo(jobId1, jobId2);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기술 스택 비교
     *
     * @param request 비교 요청 DTO
     * @return 기술 스택 비교 결과
     */
    @PostMapping("/skills")
    public ResponseEntity<ApiResponse<Object>> compareSkills(
            @RequestBody JobCompareRequest request) {
        Object response = jobCompareService.compareSkillStacks(request.getJobIds());
        return ResponseEntity.ok(ApiResponse.ok(response));
    }
}
