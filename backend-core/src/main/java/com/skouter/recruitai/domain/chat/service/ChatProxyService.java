package com.skouter.recruitai.domain.chat.service;

import com.skouter.recruitai.domain.chat.dto.request.ChatRequest;
import com.skouter.recruitai.domain.chat.dto.response.ChatResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * 챗봇 프록시 서비스
 * - FastAPI로 요청 전달 및 응답 반환
 */
@Service
@RequiredArgsConstructor
public class ChatProxyService {

    /**
     * 챗봇 메시지 전송
     *
     * @param request 채팅 요청
     * @return 채팅 응답
     */
    public ChatResponse sendMessage(ChatRequest request) {
        // TODO: FastAPI로 요청 전달
        return null;
    }

    /**
     * 대화 히스토리 조회
     *
     * @param sessionId 세션 ID
     * @return 대화 히스토리
     */
    public Object getChatHistory(String sessionId) {
        // TODO: 대화 히스토리 조회
        return null;
    }
}
