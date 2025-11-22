package com.skouter.recruitai.domain.ai.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 공고 생성 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobGenerationRequest {

    /**
     * 회사 ID
     */
    private Long companyId;

    /**
     * 직무 설명
     */
    private String jobDescription;

    /**
     * 필수 기술 스택
     */
    private String requiredSkills;

    /**
     * 템플릿 ID
     */
    private Long templateId;

    /**
     * 추가 지시사항
     */
    private String additionalInstructions;
}
