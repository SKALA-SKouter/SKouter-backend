package com.skouter.recruitai.domain.analytics.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 기술 스택 분석 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SkillsResponse {

    /**
     * 인기 기술 스택 TOP 10
     */
    private List<Object> topSkills;

    /**
     * 기술별 공고 수
     */
    private Object skillCounts;

    /**
     * 기술 트렌드
     */
    private Object skillTrends;
}
