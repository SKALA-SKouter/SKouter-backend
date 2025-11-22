package com.skouter.recruitai.global.common.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * 모든 API 응답을 통일된 포맷으로 제공하는 공통 응답 클래스
 * 성공/실패 여부, 데이터, 에러 정보를 포함합니다.
 *
 * @param <T> 실제 응답 데이터의 타입
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ApiResponse<T> {

    /**
     * 요청 성공 여부 (true: 성공, false: 실패)
     */
    private Boolean success;

    /**
     * 응답 데이터 (성공 시에만 포함)
     */
    private T data;

    /**
     * 에러 정보 (실패 시에만 포함)
     */
    private ErrorInfo error;

    /**
     * 성공 응답을 생성합니다.
     *
     * @param data 응답 데이터
     * @return ApiResponse 객체
     */
    public static <T> ApiResponse<T> ok(T data) {
        return ApiResponse.<T>builder()
                .success(true)
                .data(data)
                .build();
    }

    /**
     * 데이터 없이 성공 응답을 생성합니다.
     *
     * @return ApiResponse 객체
     */
    public static <T> ApiResponse<T> ok() {
        return ApiResponse.<T>builder()
                .success(true)
                .build();
    }

    /**
     * 실패 응답을 생성합니다.
     *
     * @param errorCode 에러 코드
     * @param message 에러 메시지
     * @return ApiResponse 객체
     */
    public static <T> ApiResponse<T> error(String errorCode, String message) {
        return ApiResponse.<T>builder()
                .success(false)
                .error(ErrorInfo.builder()
                        .code(errorCode)
                        .message(message)
                        .build())
                .build();
    }

    /**
     * 에러 정보를 담는 내부 클래스
     */
    @Getter
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ErrorInfo {
        /**
         * 에러 코드
         */
        private String code;

        /**
         * 에러 메시지
         */
        private String message;
    }
}
