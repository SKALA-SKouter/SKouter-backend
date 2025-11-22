package com.skouter.recruitai.domain.job.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 채용 공고 생성 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobCreateRequest {

    /**
     * 기업 ID
     */
    private Long companyId;

    /**
     * 공고 제목
     */
    private String title;

    /**
     * 공고 내용
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
}
