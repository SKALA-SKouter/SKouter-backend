package com.skouter.recruitai.domain.auth.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 토큰 응답 DTO
 * - 새로운 토큰 정보 반환
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class TokenResponse {

    /**
     * AccessToken
     */
    private String accessToken;

    /**
     * RefreshToken
     */
    private String refreshToken;
}
