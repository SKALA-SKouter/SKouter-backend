package com.skouter.recruitai.global.error.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 에러 응답을 표현하는 DTO
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ErrorResponse {

    /**
     * 에러 코드
     */
    private String code;

    /**
     * 에러 메시지
     */
    private String message;

    /**
     * 요청 경로 (선택사항)
     */
    private String path;

    /**
     * 요청 시간 (선택사항)
     */
    private Long timestamp;
}
