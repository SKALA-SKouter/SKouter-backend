package com.skouter.recruitai.global.client.fastapi;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

/**
 * FastAPI 클라이언트
 * - Spring Boot → FastAPI로 HTTP 요청 전송
 */
@Component
@RequiredArgsConstructor
public class FastApiClient {

    private final RestTemplate restTemplate;

    /**
     * FastAPI 헬스 체크
     */
    public boolean healthCheck() {
        // TODO: FastAPI 헬스 체크
        return true;
    }

    /**
     * 분석 요청 전송
     */
    public Object sendAnalysisRequest(Object request) {
        // TODO: FastAPI로 분석 요청 전송
        return null;
    }

    /**
     * 생성 요청 전송
     */
    public Object sendGenerationRequest(Object request) {
        // TODO: FastAPI로 생성 요청 전송
        return null;
    }
}
