package com.skouter.recruitai.domain.ai.service;

import com.skouter.recruitai.domain.ai.dto.request.JobAnalysisRequest;
import com.skouter.recruitai.domain.ai.dto.request.JobGenerationRequest;
import com.skouter.recruitai.domain.ai.dto.request.JobEvaluateRequest;
import com.skouter.recruitai.domain.ai.dto.response.AiTaskResponse;
import com.skouter.recruitai.global.client.redis.RedisPublisher;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.UUID;

/**
 * AI 작업 서비스
 * - Redis를 통해 FastAPI로 AI 작업 요청 발행
 */
@Service
@Transactional
@RequiredArgsConstructor
public class AiTaskService {

    private final RedisPublisher redisPublisher;

    /**
     * 공고 분석 요청
     *
     * @param request 분석 요청 DTO
     * @return 작업 응답 (Task ID)
     */
    public AiTaskResponse requestAnalysis(JobAnalysisRequest request) {
        String taskId = UUID.randomUUID().toString();

        // Redis에 분석 요청 발행
        redisPublisher.publishAnalysisTask(taskId, request);

        return AiTaskResponse.builder()
                .taskId(taskId)
                .status("PENDING")
                .message("공고 분석 요청이 등록되었습니다.")
                .build();
    }

    /**
     * 공고 생성 요청
     *
     * @param request 생성 요청 DTO
     * @return 작업 응답 (Task ID)
     */
    public AiTaskResponse requestGeneration(JobGenerationRequest request) {
        String taskId = UUID.randomUUID().toString();

        // Redis에 생성 요청 발행
        redisPublisher.publishGenerationTask(taskId, request);

        return AiTaskResponse.builder()
                .taskId(taskId)
                .status("PENDING")
                .message("공고 생성 요청이 등록되었습니다.")
                .build();
    }

    /**
     * 공고 평가 요청
     *
     * @param request 평가 요청 DTO
     * @return 작업 응답 (Task ID)
     */
    public AiTaskResponse requestEvaluation(JobEvaluateRequest request) {
        String taskId = UUID.randomUUID().toString();

        // Redis에 평가 요청 발행
        redisPublisher.publishEvaluationTask(taskId, request);

        return AiTaskResponse.builder()
                .taskId(taskId)
                .status("PENDING")
                .message("공고 평가 요청이 등록되었습니다.")
                .build();
    }
}
