package com.skouter.recruitai.global.client.redis;

import com.skouter.recruitai.domain.ai.dto.request.JobAnalysisRequest;
import com.skouter.recruitai.domain.ai.dto.request.JobGenerationRequest;
import com.skouter.recruitai.domain.ai.dto.request.JobEvaluateRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

/**
 * Redis 메시지 발행자
 * - Spring Boot → FastAPI로 메시지 발행
 */
@Component
@RequiredArgsConstructor
public class RedisPublisher {

    private final RedisTemplate<String, Object> redisTemplate;

    /**
     * 공고 분석 작업 발행
     */
    public void publishAnalysisTask(String taskId, JobAnalysisRequest request) {
        // TODO: Redis에 분석 작업 발행
        // redisTemplate.convertAndSend("job:analysis", ...);
    }

    /**
     * 공고 생성 작업 발행
     */
    public void publishGenerationTask(String taskId, JobGenerationRequest request) {
        // TODO: Redis에 생성 작업 발행
    }

    /**
     * 공고 평가 작업 발행
     */
    public void publishEvaluationTask(String taskId, JobEvaluateRequest request) {
        // TODO: Redis에 평가 작업 발행
    }
}
