package com.skouter.recruitai.domain.auth.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 인증 응답 DTO
 * - 사용자 정보 및 토큰 정보 반환
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AuthResponse {

    /**
     * 사용자 ID
     */
    private Long userId;

    /**
     * 사용자 이메일
     */
    private String email;

    /**
     * 사용자 이름
     */
    private String name;

    /**
     * AccessToken
     */
    private String accessToken;

    /**
     * RefreshToken
     */
    private String refreshToken;
}
