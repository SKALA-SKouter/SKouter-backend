package com.skouter.recruitai.domain.workshop.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 공고 생성 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobGenerateRequest {

    /**
     * 템플릿 ID
     */
    private Long templateId;

    /**
     * 기업 ID
     */
    private Long companyId;

    /**
     * 추가 정보
     */
    private String additionalInfo;
}
