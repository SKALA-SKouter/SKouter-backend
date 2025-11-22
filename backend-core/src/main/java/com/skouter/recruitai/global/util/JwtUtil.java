package com.skouter.recruitai.global.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.util.Date;

/**
 * JWT(JSON Web Token) 생성 및 검증을 담당하는 유틸리티 클래스
 */
@Slf4j
@Component
public class JwtUtil {

    @Value("${jwt.secret-key:your-secret-key-change-this-in-production}")
    private String secretKey;

    @Value("${jwt.expiration:3600000}")
    private long expirationTime;

    @Value("${jwt.refresh-expiration:604800000}")
    private long refreshExpirationTime;

    /**
     * JWT 토큰 생성 (Access Token)
     *
     * @param userId 사용자 ID
     * @param email 사용자 이메일
     * @return JWT 토큰 문자열
     */
    public String generateToken(Long userId, String email) {
        return Jwts.builder()
                .setSubject(userId.toString())
                .claim("email", email)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + expirationTime))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * JWT 토큰 생성 (Refresh Token)
     *
     * @param userId 사용자 ID
     * @return JWT 토큰 문자열
     */
    public String generateRefreshToken(Long userId) {
        return Jwts.builder()
                .setSubject(userId.toString())
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + refreshExpirationTime))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    /**
     * JWT 토큰에서 사용자 ID 추출
     *
     * @param token JWT 토큰
     * @return 사용자 ID
     */
    public Long extractUserId(String token) {
        Claims claims = extractAllClaims(token);
        return Long.parseLong(claims.getSubject());
    }

    /**
     * JWT 토큰에서 이메일 추출
     *
     * @param token JWT 토큰
     * @return 이메일
     */
    public String extractEmail(String token) {
        Claims claims = extractAllClaims(token);
        return claims.get("email", String.class);
    }

    /**
     * JWT 토큰 유효성 검증
     *
     * @param token JWT 토큰
     * @return 유효 여부 (true: 유효, false: 유효하지 않음)
     */
    public boolean isTokenValid(String token) {
        try {
            Jwts.parser()
                    .verifyingKey(getSigningKey())
                    .build()
                    .parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            log.error("JWT 토큰 검증 실패: {}", e.getMessage());
            return false;
        }
    }

    /**
     * JWT 토큰이 만료되었는지 확인
     *
     * @param token JWT 토큰
     * @return 만료 여부 (true: 만료됨, false: 유효함)
     */
    public boolean isTokenExpired(String token) {
        try {
            Claims claims = extractAllClaims(token);
            return claims.getExpiration().before(new Date());
        } catch (Exception e) {
            log.error("토큰 만료 시간 확인 실패: {}", e.getMessage());
            return true;
        }
    }

    /**
     * JWT 토큰에서 모든 클레임 추출
     *
     * @param token JWT 토큰
     * @return Claims 객체
     */
    private Claims extractAllClaims(String token) {
        return Jwts.parser()
                .verifyingKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody();
    }

    /**
     * 서명 키 생성
     *
     * @return SecretKey
     */
    private SecretKey getSigningKey() {
        byte[] keyBytes = secretKey.getBytes(StandardCharsets.UTF_8);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
