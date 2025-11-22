package com.skouter.recruitai.domain.analytics.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 분석 서비스
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class AnalyticsService {

    /**
     * 전체 분석 데이터 조회
     */
    public Object getAnalyticsData() {
        // TODO: 분석 데이터 조회
        return null;
    }
}
