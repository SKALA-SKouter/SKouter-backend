package com.example.demo.dto.request;

import lombok.Data;

/**
 * 회사 티어 설정 요청 DTO
 */
@Data
public class CompanyTierRequest {
    private Long companyId;
    private Integer tier;
}
