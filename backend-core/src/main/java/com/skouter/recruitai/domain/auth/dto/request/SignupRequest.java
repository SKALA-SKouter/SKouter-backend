package com.skouter.recruitai.domain.auth.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 회원가입 요청 DTO
 * - 이메일, 이름, 비밀번호로 회원가입
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class SignupRequest {

    /**
     * 사용자 이메일
     */
    private String email;

    /**
     * 사용자 이름
     */
    private String name;

    /**
     * 사용자 비밀번호
     */
    private String password;
}
