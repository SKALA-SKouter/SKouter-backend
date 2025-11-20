package com.example.demo.dto.request;

import lombok.Data;
import java.time.LocalDateTime;

/**
 * 채용공고 생성 요청 DTO
 */
@Data
public class JobPostCreateRequest {
    private String title;
    private Long companyId;
    private String content;
    private String location;
    private String experienceLevel;
    private String salary;
    private LocalDateTime deadline;
}
