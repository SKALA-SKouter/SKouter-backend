package com.skouter.recruitai.domain.job.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

/**
 * 채용 공고 비교 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobCompareResponse {

    /**
     * 비교 항목
     */
    private String compareBy;

    /**
     * 공고별 비교 데이터
     */
    private Map<Long, Object> jobComparison;

    /**
     * 상세 분석
     */
    private String analysis;

    /**
     * 추천 항목
     */
    private List<String> recommendations;
}
