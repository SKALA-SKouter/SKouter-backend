package com.skouter.recruitai.global.error;

import com.skouter.recruitai.global.common.response.ApiResponse;
import com.skouter.recruitai.global.error.exception.BusinessException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;

import java.util.HashMap;
import java.util.Map;

/**
 * 전역 예외 처리를 담당하는 핸들러
 * 모든 컨트롤러에서 발생하는 예외를 여기서 처리하고 통일된 형식으로 응답합니다.
 */
@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    /**
     * 비즈니스 로직 예외 처리
     *
     * @param e BusinessException
     * @param request WebRequest
     * @return ApiResponse 형식의 에러 응답
     */
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ApiResponse<Void>> handleBusinessException(
            BusinessException e,
            WebRequest request) {
        log.warn("비즈니스 예외 발생: {} - {}", e.getErrorCode().getCode(), e.getMessage());

        ErrorCode errorCode = e.getErrorCode();
        ApiResponse<Void> response = ApiResponse.error(
                errorCode.getCode(),
                e.getMessage()
        );

        return ResponseEntity
                .status(errorCode.getHttpStatus())
                .body(response);
    }

    /**
     * 요청 값 검증 실패 처리
     *
     * @param e MethodArgumentNotValidException
     * @param request WebRequest
     * @return ApiResponse 형식의 에러 응답
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ApiResponse<Map<String, String>>> handleValidationException(
            MethodArgumentNotValidException e,
            WebRequest request) {
        log.warn("요청 검증 실패: {}", e.getMessage());

        Map<String, String> errors = new HashMap<>();
        e.getBindingResult()
                .getAllErrors()
                .forEach(error -> {
                    String fieldName = ((FieldError) error).getField();
                    String errorMessage = error.getDefaultMessage();
                    errors.put(fieldName, errorMessage);
                });

        ApiResponse<Map<String, String>> response = ApiResponse.<Map<String, String>>builder()
                .success(false)
                .error(ApiResponse.ErrorInfo.builder()
                        .code(ErrorCode.INVALID_REQUEST.getCode())
                        .message("요청 검증에 실패했습니다.")
                        .build())
                .data(errors)
                .build();

        return ResponseEntity
                .status(HttpStatus.BAD_REQUEST)
                .body(response);
    }

    /**
     * 처리되지 않은 모든 예외 처리
     *
     * @param e Exception
     * @param request WebRequest
     * @return ApiResponse 형식의 에러 응답
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ApiResponse<Void>> handleGenericException(
            Exception e,
            WebRequest request) {
        log.error("예상치 못한 예외 발생", e);

        ErrorCode errorCode = ErrorCode.INTERNAL_SERVER_ERROR;
        ApiResponse<Void> response = ApiResponse.error(
                errorCode.getCode(),
                errorCode.getMessage()
        );

        return ResponseEntity
                .status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body(response);
    }
}
