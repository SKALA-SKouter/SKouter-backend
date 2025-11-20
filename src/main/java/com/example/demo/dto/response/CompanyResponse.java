package com.example.demo.dto.response;

import lombok.Data;

/**
 * 회사 정보 응답 DTO
 */
@Data
public class CompanyResponse {
    private Long id;
    private String name;
    private String address;
    private String industry;
    private String description;
}
