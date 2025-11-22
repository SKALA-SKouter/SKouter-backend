package com.skouter.recruitai.domain.job.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 채용 공고 카테고리 엔티티
 * - 채용 공고의 카테고리 분류 정보
 */
@Entity
@Table(name = "job_categories", indexes = {
        @Index(name = "idx_job_id", columnList = "job_id"),
        @Index(name = "idx_category", columnList = "category")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobCategory extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long jobId;

    @Column(nullable = false)
    private String category;

    /**
     * 카테고리 업데이트
     *
     * @param category 새로운 카테고리명
     */
    public void update(String category) {
        if (category != null) this.category = category;
    }
}
