package com.skouter.recruitai.domain.company.dto.response;

import com.skouter.recruitai.domain.company.entity.CompanyNews;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 기업 뉴스 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompanyNewsResponse {

    /**
     * 뉴스 ID
     */
    private Long id;

    /**
     * 기업 ID
     */
    private Long companyId;

    /**
     * 제목
     */
    private String title;

    /**
     * 내용
     */
    private String content;

    /**
     * 출처
     */
    private String source;

    /**
     * 출처 URL
     */
    private String sourceUrl;

    /**
     * 요약
     */
    private String summary;

    /**
     * 발행일
     */
    private String publishedDate;

    /**
     * 생성일시
     */
    private LocalDateTime createdAt;

    /**
     * 수정일시
     */
    private LocalDateTime updatedAt;

    /**
     * CompanyNews 엔티티를 DTO로 변환
     *
     * @param news CompanyNews 엔티티
     * @return CompanyNewsResponse DTO
     */
    public static CompanyNewsResponse fromEntity(CompanyNews news) {
        return CompanyNewsResponse.builder()
                .id(news.getId())
                .companyId(news.getCompanyId())
                .title(news.getTitle())
                .content(news.getContent())
                .source(news.getSource())
                .sourceUrl(news.getSourceUrl())
                .summary(news.getSummary())
                .publishedDate(news.getPublishedDate())
                .createdAt(news.getCreatedAt())
                .updatedAt(news.getUpdatedAt())
                .build();
    }
}
