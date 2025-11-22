package com.skouter.recruitai.domain.job.service;

import com.skouter.recruitai.domain.job.dto.response.JobCompareResponse;
import com.skouter.recruitai.domain.job.repository.JobRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 공고 비교 서비스
 * - 여러 공고를 비교 분석
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class JobCompareService {

    private final JobRepository jobRepository;

    /**
     * 여러 공고 비교
     *
     * @param jobIds 비교할 공고 ID 목록
     * @return 공고 비교 응답
     */
    public JobCompareResponse compareJobs(List<Long> jobIds) {
        // TODO: 여러 공고를 비교 분석하는 로직 구현
        // 1. 공고들 조회
        // 2. 급여, 경력, 지역 등 비교 분석
        // 3. 결과 반환
        return null;
    }

    /**
     * 두 개 공고 비교
     *
     * @param jobId1 첫 번째 공고 ID
     * @param jobId2 두 번째 공고 ID
     * @return 공고 비교 응답
     */
    public JobCompareResponse compareTwo(Long jobId1, Long jobId2) {
        // TODO: 두 공고 비교 구현
        return null;
    }

    /**
     * 공고별 기술 스택 비교
     *
     * @param jobIds 비교할 공고 ID 목록
     * @return 기술 스택 비교 결과
     */
    public Object compareSkillStacks(List<Long> jobIds) {
        // TODO: 기술 스택 비교 분석
        return null;
    }
}
