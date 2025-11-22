package com.skouter.recruitai.domain.chat.controller;

import com.skouter.recruitai.domain.chat.dto.request.ChatRequest;
import com.skouter.recruitai.domain.chat.dto.response.ChatResponse;
import com.skouter.recruitai.domain.chat.service.ChatProxyService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 챗봇 관련 API 엔드포인트
 */
@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
public class ChatController {

    private final ChatProxyService chatProxyService;

    /**
     * 챗봇 메시지 전송
     */
    @PostMapping
    public ResponseEntity<ApiResponse<ChatResponse>> sendMessage(
            @RequestBody ChatRequest request) {
        ChatResponse response = chatProxyService.sendMessage(request);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 대화 히스토리 조회
     */
    @GetMapping("/history/{sessionId}")
    public ResponseEntity<ApiResponse<Object>> getChatHistory(
            @PathVariable String sessionId) {
        Object response = chatProxyService.getChatHistory(sessionId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }
}
