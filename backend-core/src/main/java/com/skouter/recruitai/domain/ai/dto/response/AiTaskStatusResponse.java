package com.skouter.recruitai.domain.ai.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * AI 작업 상태 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AiTaskStatusResponse {

    /**
     * 작업 ID
     */
    private String taskId;

    /**
     * 작업 상태 (PENDING, RUNNING, COMPLETED, FAILED)
     */
    private String status;

    /**
     * 진행률 (0-100)
     */
    private Integer progress;

    /**
     * 에러 메시지
     */
    private String errorMessage;
}
