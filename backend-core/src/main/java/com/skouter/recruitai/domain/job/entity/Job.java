package com.skouter.recruitai.domain.job.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * 채용 공고 엔티티
 * - 채용 공고 정보 저장
 */
@Entity
@Table(name = "jobs", indexes = {
        @Index(name = "idx_company_id", columnList = "company_id"),
        @Index(name = "idx_title", columnList = "title")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Job extends BaseEntity {

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
    private String location;

    @Column
    private String experienceLevel;

    @Column
    private String salary;

    @Column
    private LocalDateTime deadline;

    @Column
    private Boolean isActive;

    /**
     * 공고 정보 업데이트
     *
     * @param title 제목
     * @param content 내용
     * @param location 위치
     * @param experienceLevel 경력 수준
     * @param salary 급여
     * @param deadline 마감일
     */
    public void updateJob(String title, String content, String location,
                          String experienceLevel, String salary, LocalDateTime deadline) {
        if (title != null) this.title = title;
        if (content != null) this.content = content;
        if (location != null) this.location = location;
        if (experienceLevel != null) this.experienceLevel = experienceLevel;
        if (salary != null) this.salary = salary;
        if (deadline != null) this.deadline = deadline;
    }
}
