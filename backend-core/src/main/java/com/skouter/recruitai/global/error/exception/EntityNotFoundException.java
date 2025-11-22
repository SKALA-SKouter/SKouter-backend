package com.skouter.recruitai.global.error.exception;

import com.skouter.recruitai.global.error.ErrorCode;

/**
 * 요청한 엔티티를 찾을 수 없을 때 발생하는 예외
 */
public class EntityNotFoundException extends BusinessException {

    /**
     * EntityNotFoundException 생성자
     *
     * @param errorCode 에러 코드
     */
    public EntityNotFoundException(ErrorCode errorCode) {
        super(errorCode);
    }

    /**
     * EntityNotFoundException 생성자 (커스텀 메시지)
     *
     * @param errorCode 에러 코드
     * @param message 커스텀 메시지
     */
    public EntityNotFoundException(ErrorCode errorCode, String message) {
        super(errorCode, message);
    }

    /**
     * 편의 메서드: 사용자를 찾을 수 없음
     *
     * @return EntityNotFoundException
     */
    public static EntityNotFoundException userNotFound() {
        return new EntityNotFoundException(ErrorCode.USER_NOT_FOUND);
    }

    /**
     * 편의 메서드: 기업을 찾을 수 없음
     *
     * @return EntityNotFoundException
     */
    public static EntityNotFoundException companyNotFound() {
        return new EntityNotFoundException(ErrorCode.COMPANY_NOT_FOUND);
    }

    /**
     * 편의 메서드: 채용 공고를 찾을 수 없음
     *
     * @return EntityNotFoundException
     */
    public static EntityNotFoundException jobNotFound() {
        return new EntityNotFoundException(ErrorCode.JOB_NOT_FOUND);
    }
}
