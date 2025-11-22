package com.skouter.recruitai.domain.analytics.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 공고 히스토리 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class HistoryResponse {

    /**
     * 총 공고 수
     */
    private Long totalJobs;

    /**
     * 신규 공고 수
     */
    private Long newJobs;

    /**
     * 종료된 공고 수
     */
    private Long closedJobs;

    /**
     * 히스토리 목록
     */
    private List<Object> historyList;
}
