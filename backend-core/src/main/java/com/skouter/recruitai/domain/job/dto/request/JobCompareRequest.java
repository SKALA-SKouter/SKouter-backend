package com.skouter.recruitai.domain.job.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * 채용 공고 비교 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobCompareRequest {

    /**
     * 비교할 공고 ID 목록
     */
    private List<Long> jobIds;

    /**
     * 비교 기준 (salary, location, skills 등)
     */
    private String compareBy;
}
