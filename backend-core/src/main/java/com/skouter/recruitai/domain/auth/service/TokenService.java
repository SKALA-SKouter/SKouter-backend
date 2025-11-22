package com.skouter.recruitai.domain.auth.service;

import com.skouter.recruitai.domain.auth.token.RefreshToken;
import com.skouter.recruitai.domain.auth.token.RefreshTokenRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 토큰 서비스
 * - RefreshToken 저장, 삭제, 조회 등 토큰 관련 데이터 처리
 */
@Service
@Transactional
@RequiredArgsConstructor
public class TokenService {

    private final RefreshTokenRepository refreshTokenRepository;

    /**
     * RefreshToken 저장 (또는 업데이트)
     *
     * @param userId 사용자 ID
     * @param token RefreshToken 값
     */
    public void saveRefreshToken(Long userId, String token) {
        // 기존 토큰이 있으면 삭제
        refreshTokenRepository.deleteByUserId(userId);

        // 새 토큰 저장
        RefreshToken refreshToken = RefreshToken.builder()
                .userId(userId)
                .token(token)
                .build();

        refreshTokenRepository.save(refreshToken);
    }

    /**
     * RefreshToken 삭제
     *
     * @param userId 사용자 ID
     */
    public void deleteRefreshToken(Long userId) {
        refreshTokenRepository.deleteByUserId(userId);
    }

    /**
     * RefreshToken 조회
     *
     * @param userId 사용자 ID
     * @return RefreshToken 값, 없으면 null
     */
    public String getRefreshToken(Long userId) {
        return refreshTokenRepository.findByUserId(userId)
                .map(RefreshToken::getToken)
                .orElse(null);
    }

    /**
     * RefreshToken 유효성 검증
     *
     * @param userId 사용자 ID
     * @param token RefreshToken 값
     * @return 유효하면 true, 아니면 false
     */
    public boolean validateRefreshToken(Long userId, String token) {
        return refreshTokenRepository.findByUserIdAndToken(userId, token)
                .isPresent();
    }
}
