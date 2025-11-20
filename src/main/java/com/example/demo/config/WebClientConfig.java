package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * WebClient 설정 (외부 API 호출용)
 * FastAPI, DART API, 뉴스 API 등 연동
 */
@Configuration
public class WebClientConfig {

    @Bean
    public WebClient webClient() {
        return WebClient.builder()
                .baseUrl("http://localhost:8000") // FastAPI 기본 URL
                .build();
    }
}
