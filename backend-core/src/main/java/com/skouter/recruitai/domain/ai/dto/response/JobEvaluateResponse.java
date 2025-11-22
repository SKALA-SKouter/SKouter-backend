package com.skouter.recruitai.domain.ai.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 공고 평가 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobEvaluateResponse {

    /**
     * 공고 ID
     */
    private Long jobId;

    /**
     * 적합도 점수 (0-100)
     */
    private Integer fitScore;

    /**
     * 난이도 평가
     */
    private String difficulty;

    /**
     * 추천 여부
     */
    private Boolean isRecommended;

    /**
     * 평가 분석 내용
     */
    private String analysis;

    /**
     * 개선 제안
     */
    private String suggestions;
}
