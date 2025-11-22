package com.skouter.recruitai.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.repository.configuration.EnableRedisRepositories;

/**
 * Redis 설정
 * - Redis 연결 풀, 직렬화 설정
 */
@Configuration
@EnableRedisRepositories(basePackages = "com.skouter.recruitai")
public class RedisConfig {

    // TODO: Redis 연결 풀 설정
    // TODO: 직렬화 설정
    // TODO: Redis Template 빈 등록
}
