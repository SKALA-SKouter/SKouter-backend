package com.skouter.recruitai.global.client.redis;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

/**
 * Redis 구독자
 * - FastAPI → Spring Boot로부터의 메시지 수신
 */
@Component
@RequiredArgsConstructor
public class RedisSubscriber {

    /**
     * 작업 완료 메시지 처리
     */
    public void handleTaskCompleted(String taskId, Object result) {
        // TODO: 작업 완료 메시지 처리
    }

    /**
     * 작업 실패 메시지 처리
     */
    public void handleTaskFailed(String taskId, String error) {
        // TODO: 작업 실패 메시지 처리
    }
}
