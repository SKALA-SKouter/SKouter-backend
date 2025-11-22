package com.skouter.recruitai.domain.auth.token;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

/**
 * JWT 제공자
 * - JWT 토큰 생성, 검증, 파싱
 */
@Component
@RequiredArgsConstructor
public class JwtProvider {

    /**
     * JWT 토큰 생성
     *
     * @param userId 사용자 ID
     * @return JWT 토큰
     */
    public String generateToken(Long userId) {
        // TODO: JWT 토큰 생성 로직
        return null;
    }

    /**
     * JWT 토큰 검증
     *
     * @param token JWT 토큰
     * @return 유효하면 true
     */
    public boolean validateToken(String token) {
        // TODO: JWT 토큰 검증 로직
        return true;
    }

    /**
     * JWT 토큰에서 사용자 ID 추출
     *
     * @param token JWT 토큰
     * @return 사용자 ID
     */
    public Long extractUserId(String token) {
        // TODO: JWT 토큰에서 사용자 ID 추출
        return null;
    }

    /**
     * RefreshToken 생성
     *
     * @param userId 사용자 ID
     * @return RefreshToken
     */
    public String generateRefreshToken(Long userId) {
        // TODO: RefreshToken 생성 로직
        return null;
    }
}
