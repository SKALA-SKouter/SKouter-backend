package com.skouter.recruitai.domain.company.controller;

import com.skouter.recruitai.domain.company.dto.response.CompanyNewsResponse;
import com.skouter.recruitai.domain.company.service.CompanyNewsService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 기업 뉴스 관련 API 엔드포인트
 * - 기업 뉴스 조회, 생성, 수정, 삭제
 */
@RestController
@RequestMapping("/api/companies/{companyId}/news")
@RequiredArgsConstructor
public class CompanyNewsController {

    private final CompanyNewsService companyNewsService;

    /**
     * 기업별 뉴스 목록 조회
     *
     * @param companyId 기업 ID
     * @return 뉴스 목록
     */
    @GetMapping
    public ResponseEntity<ApiResponse<List<CompanyNewsResponse>>> getNewsByCompanyId(
            @PathVariable Long companyId) {
        List<CompanyNewsResponse> response = companyNewsService.getNewsByCompanyId(companyId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 뉴스 상세 정보 조회
     *
     * @param newsId 뉴스 ID
     * @return 뉴스 정보
     */
    @GetMapping("/{newsId}")
    public ResponseEntity<ApiResponse<CompanyNewsResponse>> getNewsDetail(
            @PathVariable Long newsId) {
        CompanyNewsResponse response = companyNewsService.getNewsDetail(newsId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기업 뉴스 생성
     *
     * @param companyId 기업 ID
     * @param title 제목
     * @param content 내용
     * @param source 출처
     * @param sourceUrl 출처 URL
     * @param summary 요약
     * @param publishedDate 발행일
     * @return 생성된 뉴스
     */
    @PostMapping
    public ResponseEntity<ApiResponse<CompanyNewsResponse>> createNews(
            @PathVariable Long companyId,
            @RequestParam String title,
            @RequestParam String content,
            @RequestParam(required = false) String source,
            @RequestParam(required = false) String sourceUrl,
            @RequestParam(required = false) String summary,
            @RequestParam(required = false) String publishedDate) {
        CompanyNewsResponse response = companyNewsService.createNews(
                companyId, title, content, source, sourceUrl, summary, publishedDate);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok(response));
    }

    /**
     * 뉴스 수정
     *
     * @param newsId 뉴스 ID
     * @param title 제목
     * @param content 내용
     * @param summary 요약
     * @return 수정된 뉴스
     */
    @PutMapping("/{newsId}")
    public ResponseEntity<ApiResponse<CompanyNewsResponse>> updateNews(
            @PathVariable Long newsId,
            @RequestParam(required = false) String title,
            @RequestParam(required = false) String content,
            @RequestParam(required = false) String summary) {
        CompanyNewsResponse response = companyNewsService.updateNews(newsId, title, content, summary);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 뉴스 삭제
     *
     * @param newsId 뉴스 ID
     * @return 성공 응답
     */
    @DeleteMapping("/{newsId}")
    public ResponseEntity<ApiResponse<Void>> deleteNews(@PathVariable Long newsId) {
        companyNewsService.deleteNews(newsId);
        return ResponseEntity.ok(ApiResponse.ok());
    }
}
