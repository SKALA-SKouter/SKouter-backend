package com.skouter.recruitai.domain.workshop.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 공고 템플릿 엔티티
 */
@Entity
@Table(name = "job_templates", indexes = {
        @Index(name = "idx_name", columnList = "name")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobTemplate extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(columnDefinition = "LONGTEXT")
    private String content;

    @Column
    private String description;

    @Column
    private Long userId;

    /**
     * 템플릿 정보 업데이트
     */
    public void update(String name, String content, String description) {
        if (name != null) this.name = name;
        if (content != null) this.content = content;
        if (description != null) this.description = description;
    }
}
