package com.skouter.recruitai.domain.ai.service;

import com.skouter.recruitai.domain.ai.dto.response.AiTaskStatusResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

/**
 * AI 작업 상태 서비스
 * - Redis에서 작업 상태 조회
 */
@Service
@RequiredArgsConstructor
public class AiTaskStatusService {

    private final RedisTemplate<String, Object> redisTemplate;

    /**
     * 작업 상태 조회
     *
     * @param taskId 작업 ID
     * @return 작업 상태 응답
     */
    public AiTaskStatusResponse getTaskStatus(String taskId) {
        // TODO: Redis에서 작업 상태 조회
        // 1. Redis에서 taskId로 상태 조회
        // 2. 없으면 "NOT_FOUND" 상태 반환
        // 3. 있으면 해당 상태 반환

        return AiTaskStatusResponse.builder()
                .taskId(taskId)
                .status("PENDING")
                .progress(0)
                .build();
    }

    /**
     * 작업 결과 조회
     *
     * @param taskId 작업 ID
     * @return 작업 결과
     */
    public Object getTaskResult(String taskId) {
        // TODO: Redis에서 작업 결과 조회
        return null;
    }

    /**
     * 작업 취소
     *
     * @param taskId 작업 ID
     */
    public void cancelTask(String taskId) {
        // TODO: 작업 취소 로직 구현
    }
}
