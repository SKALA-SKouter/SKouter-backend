package com.skouter.recruitai.domain.auth.token;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * RefreshToken 저장소
 * - RefreshToken 데이터 접근
 */
@Repository
public interface RefreshTokenRepository extends JpaRepository<RefreshToken, Long> {

    /**
     * 사용자 ID로 RefreshToken 조회
     *
     * @param userId 사용자 ID
     * @return RefreshToken 엔티티
     */
    Optional<RefreshToken> findByUserId(Long userId);

    /**
     * 사용자 ID와 토큰으로 RefreshToken 조회
     *
     * @param userId 사용자 ID
     * @param token 토큰 값
     * @return RefreshToken 엔티티
     */
    Optional<RefreshToken> findByUserIdAndToken(Long userId, String token);

    /**
     * 사용자 ID로 RefreshToken 삭제
     *
     * @param userId 사용자 ID
     */
    void deleteByUserId(Long userId);
}
