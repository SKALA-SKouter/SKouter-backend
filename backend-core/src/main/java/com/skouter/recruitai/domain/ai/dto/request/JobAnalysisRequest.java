package com.skouter.recruitai.domain.ai.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 공고 분석 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobAnalysisRequest {

    /**
     * 공고 ID
     */
    private Long jobId;

    /**
     * 분석 타입 (keyword, sentiment, skills 등)
     */
    private String analysisType;

    /**
     * 추가 옵션
     */
    private String options;
}
