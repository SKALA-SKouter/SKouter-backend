package com.skouter.recruitai.domain.company.controller;

import com.skouter.recruitai.domain.company.dto.response.CompanyDetailResponse;
import com.skouter.recruitai.domain.company.dto.response.CompanyListResponse;
import com.skouter.recruitai.domain.company.service.CompanyService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import com.skouter.recruitai.global.common.response.PageResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 기업 관련 API 엔드포인트
 * - 기업 정보 조회, 생성, 수정, 삭제
 */
@RestController
@RequestMapping("/api/companies")
@RequiredArgsConstructor
public class CompanyController {

    private final CompanyService companyService;

    /**
     * 기업 상세 정보 조회
     *
     * @param companyId 기업 ID
     * @return 기업 상세 정보
     */
    @GetMapping("/{companyId}")
    public ResponseEntity<ApiResponse<CompanyDetailResponse>> getCompanyDetail(
            @PathVariable Long companyId) {
        CompanyDetailResponse response = companyService.getCompanyDetail(companyId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기업명으로 기업 조회
     *
     * @param name 기업명
     * @return 기업 상세 정보
     */
    @GetMapping("/name/{name}")
    public ResponseEntity<ApiResponse<CompanyDetailResponse>> getCompanyByName(
            @PathVariable String name) {
        CompanyDetailResponse response = companyService.getCompanyByName(name);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 모든 기업 목록 조회 (페이징)
     *
     * @param pageable 페이징 정보
     * @return 기업 목록
     */
    @GetMapping
    public ResponseEntity<ApiResponse<PageResponse<CompanyListResponse>>> getAllCompanies(
            Pageable pageable) {
        Page<CompanyListResponse> page = companyService.getAllCompanies(pageable);
        PageResponse<CompanyListResponse> response = PageResponse.of(page);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기업 정보 생성
     *
     * @param name 기업명
     * @param description 설명
     * @param website 웹사이트
     * @param industry 산업
     * @param scale 규모
     * @param location 위치
     * @return 생성된 기업 정보
     */
    @PostMapping
    public ResponseEntity<ApiResponse<CompanyDetailResponse>> createCompany(
            @RequestParam String name,
            @RequestParam(required = false) String description,
            @RequestParam(required = false) String website,
            @RequestParam(required = false) String industry,
            @RequestParam(required = false) String scale,
            @RequestParam(required = false) String location) {
        CompanyDetailResponse response = companyService.createCompany(
                name, description, website, industry, scale, location);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok(response));
    }

    /**
     * 기업 정보 수정
     *
     * @param companyId 기업 ID
     * @param name 기업명
     * @param description 설명
     * @param website 웹사이트
     * @param industry 산업
     * @param scale 규모
     * @param location 위치
     * @return 수정된 기업 정보
     */
    @PutMapping("/{companyId}")
    public ResponseEntity<ApiResponse<CompanyDetailResponse>> updateCompany(
            @PathVariable Long companyId,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String description,
            @RequestParam(required = false) String website,
            @RequestParam(required = false) String industry,
            @RequestParam(required = false) String scale,
            @RequestParam(required = false) String location) {
        CompanyDetailResponse response = companyService.updateCompany(
                companyId, name, description, website, industry, scale, location);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 기업 삭제
     *
     * @param companyId 기업 ID
     * @return 성공 응답
     */
    @DeleteMapping("/{companyId}")
    public ResponseEntity<ApiResponse<Void>> deleteCompany(@PathVariable Long companyId) {
        companyService.deleteCompany(companyId);
        return ResponseEntity.ok(ApiResponse.ok());
    }
}
