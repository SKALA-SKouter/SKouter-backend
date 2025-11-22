package com.skouter.recruitai.domain.job.dto.response;

import com.skouter.recruitai.domain.job.entity.Job;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 채용 공고 목록 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobListResponse {

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
     * Job 엔티티를 DTO로 변환
     *
     * @param job Job 엔티티
     * @return JobListResponse DTO
     */
    public static JobListResponse fromEntity(Job job) {
        return JobListResponse.builder()
                .id(job.getId())
                .companyId(job.getCompanyId())
                .title(job.getTitle())
                .location(job.getLocation())
                .experienceLevel(job.getExperienceLevel())
                .salary(job.getSalary())
                .build();
    }
}
