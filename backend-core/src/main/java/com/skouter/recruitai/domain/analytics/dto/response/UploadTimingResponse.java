package com.skouter.recruitai.domain.analytics.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 공고 업로드 시기 분석 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UploadTimingResponse {

    /**
     * 요일별 업로드 통계
     */
    private Object dayOfWeekStats;

    /**
     * 시간대별 업로드 통계
     */
    private Object hourStats;

    /**
     * 월별 업로드 추이
     */
    private Object monthlyTrend;
}
