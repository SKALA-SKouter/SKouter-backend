package com.skouter.recruitai.global.error;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 애플리케이션에서 사용되는 모든 에러 코드를 정의하는 enum
 * HTTP 상태 코드와 에러 메시지를 함께 관리합니다.
 */
@Getter
@AllArgsConstructor
public enum ErrorCode {

    // 공통 에러
    INTERNAL_SERVER_ERROR("INTERNAL_SERVER_ERROR", "내부 서버 오류가 발생했습니다.", 500),
    INVALID_REQUEST("INVALID_REQUEST", "유효하지 않은 요청입니다.", 400),

    // 인증 관련 에러
    UNAUTHORIZED("UNAUTHORIZED", "인증되지 않은 사용자입니다.", 401),
    FORBIDDEN("FORBIDDEN", "접근 권한이 없습니다.", 403),
    INVALID_TOKEN("INVALID_TOKEN", "유효하지 않은 토큰입니다.", 401),
    TOKEN_EXPIRED("TOKEN_EXPIRED", "토큰이 만료되었습니다.", 401),

    // 엔티티 관련 에러
    ENTITY_NOT_FOUND("ENTITY_NOT_FOUND", "요청한 리소스를 찾을 수 없습니다.", 404),
    USER_NOT_FOUND("USER_NOT_FOUND", "사용자를 찾을 수 없습니다.", 404),
    COMPANY_NOT_FOUND("COMPANY_NOT_FOUND", "기업을 찾을 수 없습니다.", 404),
    JOB_NOT_FOUND("JOB_NOT_FOUND", "채용 공고를 찾을 수 없습니다.", 404),

    // 비즈니스 로직 에러
    DUPLICATE_EMAIL("DUPLICATE_EMAIL", "이미 가입된 이메일입니다.", 409),
    INVALID_PASSWORD("INVALID_PASSWORD", "비밀번호가 일치하지 않습니다.", 400),
    INVALID_VALUE("INVALID_VALUE", "유효하지 않은 값입니다.", 400),

    // AI 관련 에러
    AI_SERVICE_UNAVAILABLE("AI_SERVICE_UNAVAILABLE", "AI 서비스를 현재 사용할 수 없습니다.", 503),
    INVALID_AI_REQUEST("INVALID_AI_REQUEST", "유효하지 않은 AI 요청입니다.", 400);

    /**
     * 에러 코드
     */
    private final String code;

    /**
     * 에러 메시지
     */
    private final String message;

    /**
     * HTTP 상태 코드
     */
    private final int httpStatus;
}
