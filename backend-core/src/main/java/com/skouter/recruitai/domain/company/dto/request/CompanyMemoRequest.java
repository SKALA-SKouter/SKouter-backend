package com.skouter.recruitai.domain.company.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 기업 메모 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompanyMemoRequest {

    /**
     * 메모 내용
     */
    private String content;
}
