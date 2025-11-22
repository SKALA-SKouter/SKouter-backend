package com.skouter.recruitai.global.error.exception;

import com.skouter.recruitai.global.error.ErrorCode;

/**
 * 유효하지 않은 값이 전달되었을 때 발생하는 예외
 */
public class InvalidValueException extends BusinessException {

    /**
     * InvalidValueException 생성자
     *
     * @param errorCode 에러 코드
     */
    public InvalidValueException(ErrorCode errorCode) {
        super(errorCode);
    }

    /**
     * InvalidValueException 생성자 (커스텀 메시지)
     *
     * @param errorCode 에러 코드
     * @param message 커스텀 메시지
     */
    public InvalidValueException(ErrorCode errorCode, String message) {
        super(errorCode, message);
    }

    /**
     * 편의 메서드: 비밀번호가 일치하지 않음
     *
     * @return InvalidValueException
     */
    public static InvalidValueException invalidPassword() {
        return new InvalidValueException(ErrorCode.INVALID_PASSWORD);
    }

    /**
     * 편의 메서드: 중복된 이메일
     *
     * @return InvalidValueException
     */
    public static InvalidValueException duplicateEmail() {
        return new InvalidValueException(ErrorCode.DUPLICATE_EMAIL);
    }
}
