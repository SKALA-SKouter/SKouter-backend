package com.example.demo.exception;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

/**
 * 에러 코드 정의
 */
@Getter
@RequiredArgsConstructor
public enum ErrorCode {
    USER_NOT_FOUND("사용자를 찾을 수 없습니다."),
    INVALID_PASSWORD("비밀번호가 일치하지 않습니다."),
    DUPLICATE_EMAIL("이미 존재하는 이메일입니다."),
    JOB_POST_NOT_FOUND("채용공고를 찾을 수 없습니다."),
    COMPANY_NOT_FOUND("회사를 찾을 수 없습니다."),
    UNAUTHORIZED("인증이 필요합니다."),
    FORBIDDEN("권한이 없습니다.");

    private final String message;
}
