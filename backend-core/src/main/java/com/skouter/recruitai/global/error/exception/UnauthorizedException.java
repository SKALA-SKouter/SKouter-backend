package com.skouter.recruitai.global.error.exception;

import com.skouter.recruitai.global.error.ErrorCode;

/**
 * 인증되지 않은 사용자가 보호된 리소스에 접근할 때 발생하는 예외
 */
public class UnauthorizedException extends BusinessException {

    /**
     * UnauthorizedException 생성자
     *
     * @param errorCode 에러 코드
     */
    public UnauthorizedException(ErrorCode errorCode) {
        super(errorCode);
    }

    /**
     * UnauthorizedException 생성자 (커스텀 메시지)
     *
     * @param errorCode 에러 코드
     * @param message 커스텀 메시지
     */
    public UnauthorizedException(ErrorCode errorCode, String message) {
        super(errorCode, message);
    }

    /**
     * 편의 메서드: 토큰이 만료됨
     *
     * @return UnauthorizedException
     */
    public static UnauthorizedException tokenExpired() {
        return new UnauthorizedException(ErrorCode.TOKEN_EXPIRED);
    }

    /**
     * 편의 메서드: 유효하지 않은 토큰
     *
     * @return UnauthorizedException
     */
    public static UnauthorizedException invalidToken() {
        return new UnauthorizedException(ErrorCode.INVALID_TOKEN);
    }

    /**
     * 편의 메서드: 인증되지 않음
     *
     * @return UnauthorizedException
     */
    public static UnauthorizedException unauthorized() {
        return new UnauthorizedException(ErrorCode.UNAUTHORIZED);
    }
}
