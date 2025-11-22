package com.skouter.recruitai.global.error.exception;

import com.skouter.recruitai.global.error.ErrorCode;

/**
 * 비즈니스 로직 상의 예외를 나타내는 기본 예외 클래스
 * 모든 비즈니스 예외는 이 클래스를 상속받아야 합니다.
 */
public class BusinessException extends RuntimeException {

    private final ErrorCode errorCode;

    /**
     * BusinessException 생성자
     *
     * @param errorCode 에러 코드
     */
    public BusinessException(ErrorCode errorCode) {
        super(errorCode.getMessage());
        this.errorCode = errorCode;
    }

    /**
     * BusinessException 생성자 (커스텀 메시지)
     *
     * @param errorCode 에러 코드
     * @param message 커스텀 메시지
     */
    public BusinessException(ErrorCode errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }

    /**
     * BusinessException 생성자 (원인 포함)
     *
     * @param errorCode 에러 코드
     * @param cause 원인이 되는 예외
     */
    public BusinessException(ErrorCode errorCode, Throwable cause) {
        super(errorCode.getMessage(), cause);
        this.errorCode = errorCode;
    }

    /**
     * 에러 코드를 반환합니다.
     *
     * @return 에러 코드
     */
    public ErrorCode getErrorCode() {
        return errorCode;
    }
}
