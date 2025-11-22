package com.skouter.recruitai.domain.job.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 기술 스택 엔티티
 * - 채용 공고에 필요한 기술 스택 정보
 */
@Entity
@Table(name = "skills", indexes = {
        @Index(name = "idx_name", columnList = "name"),
        @Index(name = "idx_job_id", columnList = "job_id")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Skill extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long jobId;

    @Column(nullable = false)
    private String name;

    @Column
    private String level;

    /**
     * 기술 스택 정보 업데이트
     *
     * @param name 기술명
     * @param level 필요 레벨
     */
    public void update(String name, String level) {
        if (name != null) this.name = name;
        if (level != null) this.level = level;
    }
}
