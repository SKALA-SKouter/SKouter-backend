package com.skouter.recruitai.global.client.fastapi.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * AI 분석 응답 DTO
 * - FastAPI로부터 받는 분석 결과
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AiAnalysisResponse {

    /**
     * 작업 ID
     */
    private String taskId;

    /**
     * 작업 상태
     */
    private String status;

    /**
     * 분석 결과
     */
    private Object result;

    /**
     * 에러 메시지
     */
    private String errorMessage;
}
