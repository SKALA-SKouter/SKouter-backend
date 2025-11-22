package com.skouter.recruitai.domain.workshop.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 공고 생성 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobGenerateResponse {

    /**
     * 작업 ID
     */
    private String taskId;

    /**
     * 작업 상태
     */
    private String status;

    /**
     * 생성된 공고 ID
     */
    private Long jobId;
}
