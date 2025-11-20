package com.example.demo.dto.request;

import lombok.Data;

/**
 * 채용공고 검색 요청 DTO
 */
@Data
public class JobSearchRequest {
    private String keyword;
    private String location;
    private String experienceLevel;
    private String[] skills;
    private int page = 0;
    private int size = 20;
}
