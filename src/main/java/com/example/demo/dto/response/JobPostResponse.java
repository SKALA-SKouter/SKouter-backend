package com.example.demo.dto.response;

import lombok.Data;
import java.time.LocalDateTime;

/**
 * 채용공고 응답 DTO
 */
@Data
public class JobPostResponse {
    private Long id;
    private String title;
    private String companyName;
    private String content;
    private String location;
    private String experienceLevel;
    private String salary;
    private LocalDateTime deadline;
    private LocalDateTime createdAt;
}
