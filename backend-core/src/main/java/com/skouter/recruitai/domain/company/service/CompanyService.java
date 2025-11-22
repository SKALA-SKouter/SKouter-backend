package com.skouter.recruitai.domain.company.service;

import com.skouter.recruitai.domain.company.dto.request.CompanyMemoRequest;
import com.skouter.recruitai.domain.company.dto.response.CompanyDetailResponse;
import com.skouter.recruitai.domain.company.dto.response.CompanyListResponse;
import com.skouter.recruitai.domain.company.entity.Company;
import com.skouter.recruitai.domain.company.repository.CompanyRepository;
import com.skouter.recruitai.global.error.exception.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 기업 서비스
 * - 기업 정보 조회, 생성, 수정, 삭제 등 비즈니스 로직 처리
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class CompanyService {

    private final CompanyRepository companyRepository;

    /**
     * 기업 ID로 기업 상세 정보 조회
     *
     * @param companyId 기업 ID
     * @return 기업 상세 응답 DTO
     */
    public CompanyDetailResponse getCompanyDetail(Long companyId) {
        Company company = companyRepository.findById(companyId)
                .orElseThrow(EntityNotFoundException::companyNotFound);
        return CompanyDetailResponse.fromEntity(company);
    }

    /**
     * 모든 기업 목록 조회 (페이징)
     *
     * @param pageable 페이징 정보
     * @return 기업 목록 응답 DTO
     */
    public Page<CompanyListResponse> getAllCompanies(Pageable pageable) {
        return companyRepository.findAll(pageable)
                .map(CompanyListResponse::fromEntity);
    }

    /**
     * 기업명으로 기업 조회
     *
     * @param name 기업명
     * @return 기업 상세 응답 DTO
     */
    public CompanyDetailResponse getCompanyByName(String name) {
        Company company = companyRepository.findByName(name)
                .orElseThrow(EntityNotFoundException::companyNotFound);
        return CompanyDetailResponse.fromEntity(company);
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
     * @return 생성된 기업 상세 응답 DTO
     */
    @Transactional
    public CompanyDetailResponse createCompany(String name, String description,
                                                String website, String industry,
                                                String scale, String location) {
        Company company = Company.builder()
                .name(name)
                .description(description)
                .website(website)
                .industry(industry)
                .scale(scale)
                .location(location)
                .build();

        Company savedCompany = companyRepository.save(company);
        return CompanyDetailResponse.fromEntity(savedCompany);
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
     * @return 수정된 기업 상세 응답 DTO
     */
    @Transactional
    public CompanyDetailResponse updateCompany(Long companyId, String name,
                                                String description, String website,
                                                String industry, String scale,
                                                String location) {
        Company company = companyRepository.findById(companyId)
                .orElseThrow(EntityNotFoundException::companyNotFound);

        company.updateCompanyInfo(name, description, website, industry, scale, location);

        return CompanyDetailResponse.fromEntity(company);
    }

    /**
     * 기업 삭제
     *
     * @param companyId 기업 ID
     */
    @Transactional
    public void deleteCompany(Long companyId) {
        Company company = companyRepository.findById(companyId)
                .orElseThrow(EntityNotFoundException::companyNotFound);
        companyRepository.delete(company);
    }
}
