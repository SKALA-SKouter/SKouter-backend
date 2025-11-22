package com.skouter.recruitai.domain.analytics.service;

import com.skouter.recruitai.domain.analytics.dto.response.HistoryResponse;
import com.skouter.recruitai.domain.analytics.dto.response.SkillsResponse;
import com.skouter.recruitai.domain.analytics.dto.response.UploadTimingResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 트렌드 분석 서비스
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class TrendAnalysisService {

    /**
     * 공고 업로드 시기 분석
     */
    public UploadTimingResponse analyzeUploadTiming() {
        // TODO: 공고 업로드 시기 분석
        return null;
    }

    /**
     * 공고 히스토리 조회
     */
    public HistoryResponse getHistory() {
        // TODO: 공고 히스토리 조회
        return null;
    }

    /**
     * 기술 스택 분석
     */
    public SkillsResponse analyzeSkills() {
        // TODO: 기술 스택 분석
        return null;
    }
}
