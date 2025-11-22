package com.skouter.recruitai.domain.job.dto.response;

import com.skouter.recruitai.domain.job.entity.Job;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 채용 공고 상세 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobDetailResponse {

    /**
     * 공고 ID
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
     * 근무 지역
     */
    private String location;

    /**
     * 경력 수준
     */
    private String experienceLevel;

    /**
     * 급여
     */
    private String salary;

    /**
     * 마감일
     */
    private LocalDateTime deadline;

    /**
     * 활성 상태
     */
    private Boolean isActive;

    /**
     * 생성일시
     */
    private LocalDateTime createdAt;

    /**
     * 수정일시
     */
    private LocalDateTime updatedAt;

    /**
     * Job 엔티티를 DTO로 변환
     *
     * @param job Job 엔티티
     * @return JobDetailResponse DTO
     */
    public static JobDetailResponse fromEntity(Job job) {
        return JobDetailResponse.builder()
                .id(job.getId())
                .companyId(job.getCompanyId())
                .title(job.getTitle())
                .content(job.getContent())
                .location(job.getLocation())
                .experienceLevel(job.getExperienceLevel())
                .salary(job.getSalary())
                .deadline(job.getDeadline())
                .isActive(job.getIsActive())
                .createdAt(job.getCreatedAt())
                .updatedAt(job.getUpdatedAt())
                .build();
    }
}
