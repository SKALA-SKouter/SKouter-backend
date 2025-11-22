package com.skouter.recruitai.domain.company.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 기업 엔티티
 * - 기업 정보 저장
 */
@Entity
@Table(name = "companies", indexes = {
        @Index(name = "idx_name", columnList = "name")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Company extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column
    private String description;

    @Column
    private String website;

    @Column
    private String logoUrl;

    @Column
    private String industry;

    @Column
    private String scale;

    @Column
    private String location;

    /**
     * 기업 정보 업데이트
     *
     * @param name 기업명
     * @param description 설명
     * @param website 웹사이트
     * @param industry 산업
     * @param scale 규모
     * @param location 위치
     */
    public void updateCompanyInfo(String name, String description, String website,
                                   String industry, String scale, String location) {
        if (name != null) this.name = name;
        if (description != null) this.description = description;
        if (website != null) this.website = website;
        if (industry != null) this.industry = industry;
        if (scale != null) this.scale = scale;
        if (location != null) this.location = location;
    }
}
