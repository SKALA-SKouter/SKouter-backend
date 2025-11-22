package com.skouter.recruitai.domain.job.controller;

import com.skouter.recruitai.domain.job.dto.request.JobCreateRequest;
import com.skouter.recruitai.domain.job.dto.response.JobDetailResponse;
import com.skouter.recruitai.domain.job.dto.response.JobListResponse;
import com.skouter.recruitai.domain.job.service.JobService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import com.skouter.recruitai.global.common.response.PageResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 채용 공고 관련 API 엔드포인트
 * - 공고 조회, 생성, 수정, 삭제
 */
@RestController
@RequestMapping("/api/jobs")
@RequiredArgsConstructor
public class JobController {

    private final JobService jobService;

    /**
     * 공고 상세 정보 조회
     *
     * @param jobId 공고 ID
     * @return 공고 상세 정보
     */
    @GetMapping("/{jobId}")
    public ResponseEntity<ApiResponse<JobDetailResponse>> getJobDetail(@PathVariable Long jobId) {
        JobDetailResponse response = jobService.getJobDetail(jobId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 모든 공고 목록 조회 (페이징)
     *
     * @param pageable 페이징 정보
     * @return 공고 목록
     */
    @GetMapping
    public ResponseEntity<ApiResponse<PageResponse<JobListResponse>>> getAllJobs(Pageable pageable) {
        Page<JobListResponse> page = jobService.getAllJobs(pageable);
        PageResponse<JobListResponse> response = PageResponse.of(page);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기업별 공고 목록 조회
     *
     * @param companyId 기업 ID
     * @param pageable 페이징 정보
     * @return 공고 목록
     */
    @GetMapping("/company/{companyId}")
    public ResponseEntity<ApiResponse<PageResponse<JobListResponse>>> getJobsByCompanyId(
            @PathVariable Long companyId, Pageable pageable) {
        Page<JobListResponse> page = jobService.getJobsByCompanyId(companyId, pageable);
        PageResponse<JobListResponse> response = PageResponse.of(page);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 공고 제목으로 검색
     *
     * @param title 검색 키워드
     * @param pageable 페이징 정보
     * @return 검색 결과
     */
    @GetMapping("/search")
    public ResponseEntity<ApiResponse<PageResponse<JobListResponse>>> searchJobs(
            @RequestParam String title, Pageable pageable) {
        Page<JobListResponse> page = jobService.searchJobsByTitle(title, pageable);
        PageResponse<JobListResponse> response = PageResponse.of(page);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 공고 생성
     *
     * @param request 공고 생성 요청 DTO
     * @return 생성된 공고
     */
    @PostMapping
    public ResponseEntity<ApiResponse<JobDetailResponse>> createJob(
            @RequestBody JobCreateRequest request) {
        JobDetailResponse response = jobService.createJob(
                request.getCompanyId(),
                request.getTitle(),
                request.getContent(),
                request.getLocation(),
                request.getExperienceLevel(),
                request.getSalary(),
                request.getDeadline());
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok(response));
    }

    /**
     * 공고 수정
     *
     * @param jobId 공고 ID
     * @param request 공고 수정 요청 DTO
     * @return 수정된 공고
     */
    @PutMapping("/{jobId}")
    public ResponseEntity<ApiResponse<JobDetailResponse>> updateJob(
            @PathVariable Long jobId,
            @RequestBody JobCreateRequest request) {
        JobDetailResponse response = jobService.updateJob(
                jobId,
                request.getTitle(),
                request.getContent(),
                request.getLocation(),
                request.getExperienceLevel(),
                request.getSalary(),
                request.getDeadline());
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 공고 삭제
     *
     * @param jobId 공고 ID
     * @return 성공 응답
     */
    @DeleteMapping("/{jobId}")
    public ResponseEntity<ApiResponse<Void>> deleteJob(@PathVariable Long jobId) {
        jobService.deleteJob(jobId);
        return ResponseEntity.ok(ApiResponse.ok());
    }
}
