package com.skouter.recruitai.domain.company.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 기업 뉴스 엔티티
 * - 기업 관련 뉴스 정보 저장
 */
@Entity
@Table(name = "company_news", indexes = {
        @Index(name = "idx_company_id", columnList = "company_id"),
        @Index(name = "idx_published_date", columnList = "published_date")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompanyNews extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long companyId;

    @Column(nullable = false)
    private String title;

    @Column(columnDefinition = "LONGTEXT")
    private String content;

    @Column
    private String source;

    @Column
    private String sourceUrl;

    @Column
    private String summary;

    @Column
    private String publishedDate;

    /**
     * 뉴스 정보 업데이트
     *
     * @param title 제목
     * @param content 내용
     * @param summary 요약
     */
    public void updateNews(String title, String content, String summary) {
        if (title != null) this.title = title;
        if (content != null) this.content = content;
        if (summary != null) this.summary = summary;
    }
}
