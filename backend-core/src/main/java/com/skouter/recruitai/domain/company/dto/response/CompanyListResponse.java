package com.skouter.recruitai.domain.company.dto.response;

import com.skouter.recruitai.domain.company.entity.Company;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 기업 목록 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompanyListResponse {

    /**
     * 기업 ID
     */
    private Long id;

    /**
     * 기업명
     */
    private String name;

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
     * 로고 URL
     */
    private String logoUrl;

    /**
     * Company 엔티티를 DTO로 변환
     *
     * @param company Company 엔티티
     * @return CompanyListResponse DTO
     */
    public static CompanyListResponse fromEntity(Company company) {
        return CompanyListResponse.builder()
                .id(company.getId())
                .name(company.getName())
                .industry(company.getIndustry())
                .scale(company.getScale())
                .location(company.getLocation())
                .logoUrl(company.getLogoUrl())
                .build();
    }
}
