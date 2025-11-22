package com.skouter.recruitai.global.client.fastapi.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

/**
 * FastAPI 클라이언트 설정
 * - RestTemplate 빈 등록
 */
@Configuration
public class FastApiClientConfig {

    /**
     * RestTemplate 빈 등록
     *
     * @return RestTemplate
     */
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
