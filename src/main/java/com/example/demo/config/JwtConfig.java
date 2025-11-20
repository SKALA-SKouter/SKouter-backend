package com.example.demo.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

import lombok.Data;

/**
 * JWT 토큰 관련 설정
 */
@Data
@Configuration
@ConfigurationProperties(prefix = "jwt")
public class JwtConfig {
    private String secret = "your-secret-key-change-this-in-production";
    private long expiration = 86400000; // 24시간 (밀리초)
}
