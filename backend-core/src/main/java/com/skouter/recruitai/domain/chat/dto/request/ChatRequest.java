package com.skouter.recruitai.domain.chat.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 챗봇 메시지 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ChatRequest {

    /**
     * 세션 ID
     */
    private String sessionId;

    /**
     * 메시지 내용
     */
    private String message;

    /**
     * 사용자 ID
     */
    private Long userId;
}
