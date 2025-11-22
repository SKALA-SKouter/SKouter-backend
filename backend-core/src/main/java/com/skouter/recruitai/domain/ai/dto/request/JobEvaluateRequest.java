package com.skouter.recruitai.domain.ai.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 공고 평가 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobEvaluateRequest {

    /**
     * 공고 ID
     */
    private Long jobId;

    /**
     * 사용자 경력 수준
     */
    private String userExperienceLevel;

    /**
     * 사용자 기술 스택
     */
    private String userSkills;

    /**
     * 평가 기준 (difficulty, fit, salary 등)
     */
    private String evaluationCriteria;
}
