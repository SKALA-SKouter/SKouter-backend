package com.skouter.recruitai.domain.company.dto.response;

import com.skouter.recruitai.domain.company.entity.Company;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 기업 상세 정보 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompanyDetailResponse {

    /**
     * 기업 ID
     */
    private Long id;

    /**
     * 기업명
     */
    private String name;

    /**
     * 기업 설명
     */
    private String description;

    /**
     * 웹사이트 URL
     */
    private String website;

    /**
     * 로고 URL
     */
    private String logoUrl;

    /**
     * 산업
     */
    private String industry;

    /**
     * 기업 규모
     */
    private String scale;

    /**
     * 위치
     */
    private String location;

    /**
     * 생성일시
     */
    private LocalDateTime createdAt;

    /**
     * 수정일시
     */
    private LocalDateTime updatedAt;

    /**
     * Company 엔티티를 DTO로 변환
     *
     * @param company Company 엔티티
     * @return CompanyDetailResponse DTO
     */
    public static CompanyDetailResponse fromEntity(Company company) {
        return CompanyDetailResponse.builder()
                .id(company.getId())
                .name(company.getName())
                .description(company.getDescription())
                .website(company.getWebsite())
                .logoUrl(company.getLogoUrl())
                .industry(company.getIndustry())
                .scale(company.getScale())
                .location(company.getLocation())
                .createdAt(company.getCreatedAt())
                .updatedAt(company.getUpdatedAt())
                .build();
    }
}
