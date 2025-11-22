package com.skouter.recruitai.domain.ai.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * AI 작업 응답 DTO
 * - 작업 ID와 상태 반환
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AiTaskResponse {

    /**
     * 작업 ID
     */
    private String taskId;

    /**
     * 작업 상태
     */
    private String status;

    /**
     * 메시지
     */
    private String message;
}
