package com.skouter.recruitai.domain.chat.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 챗봇 메시지 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class ChatResponse {

    /**
     * 세션 ID
     */
    private String sessionId;

    /**
     * 응답 메시지
     */
    private String message;

    /**
     * 추천 정보
     */
    private Object recommendations;
}
