package com.skouter.recruitai.domain.workshop.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 템플릿 목록 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TemplateListResponse {

    /**
     * 템플릿 ID
     */
    private Long templateId;

    /**
     * 템플릿 이름
     */
    private String name;

    /**
     * 템플릿 설명
     */
    private String description;
}
