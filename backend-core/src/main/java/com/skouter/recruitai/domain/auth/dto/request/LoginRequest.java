package com.skouter.recruitai.domain.auth.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 로그인 요청 DTO
 * - 이메일과 비밀번호로 로그인
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LoginRequest {

    /**
     * 사용자 이메일
     */
    private String email;

    /**
     * 사용자 비밀번호
     */
    private String password;
}
