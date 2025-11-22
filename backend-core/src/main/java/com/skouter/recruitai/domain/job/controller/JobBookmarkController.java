package com.skouter.recruitai.domain.job.controller;

import com.skouter.recruitai.domain.job.service.JobBookmarkService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 채용 공고 북마크 관련 API 엔드포인트
 * - 북마크 추가, 제거, 조회
 */
@RestController
@RequestMapping("/api/jobs/bookmarks")
@RequiredArgsConstructor
public class JobBookmarkController {

    private final JobBookmarkService jobBookmarkService;

    /**
     * 북마크 추가
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     * @return 성공 응답
     */
    @PostMapping
    public ResponseEntity<ApiResponse<Void>> addBookmark(
            @RequestParam Long userId,
            @RequestParam Long jobId) {
        jobBookmarkService.addBookmark(userId, jobId);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok());
    }

    /**
     * 북마크 제거
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     * @return 성공 응답
     */
    @DeleteMapping
    public ResponseEntity<ApiResponse<Void>> removeBookmark(
            @RequestParam Long userId,
            @RequestParam Long jobId) {
        jobBookmarkService.removeBookmark(userId, jobId);
        return ResponseEntity.ok(ApiResponse.ok());
    }

    /**
     * 북마크 여부 확인
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     * @return 북마크 여부
     */
    @GetMapping("/check")
    public ResponseEntity<ApiResponse<Boolean>> isBookmarked(
            @RequestParam Long userId,
            @RequestParam Long jobId) {
        boolean result = jobBookmarkService.isBookmarked(userId, jobId);
        return ResponseEntity.ok(ApiResponse.ok(result));
    }

    /**
     * 공고별 북마크 개수 조회
     *
     * @param jobId 공고 ID
     * @return 북마크 개수
     */
    @GetMapping("/count/{jobId}")
    public ResponseEntity<ApiResponse<Long>> getBookmarkCount(@PathVariable Long jobId) {
        long count = jobBookmarkService.getBookmarkCount(jobId);
        return ResponseEntity.ok(ApiResponse.ok(count));
    }
}
