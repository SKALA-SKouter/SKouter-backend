package com.skouter.recruitai.global.client.fastapi.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * AI 분석 요청 DTO
 * - FastAPI로 전송하는 분석 요청
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AiAnalysisRequest {

    /**
     * 작업 ID
     */
    private String taskId;

    /**
     * 공고 ID
     */
    private Long jobId;

    /**
     * 분석 타입
     */
    private String analysisType;

    /**
     * 공고 내용
     */
    private String jobContent;

    /**
     * 추가 옵션
     */
    private String options;
}
