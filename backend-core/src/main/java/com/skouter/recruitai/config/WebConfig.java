package com.skouter.recruitai.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * Web MVC 설정
 * - CORS, 인터셉터, 메시지 컨버터
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {

    /**
     * CORS 설정
     *
     * @param registry CorsRegistry
     */
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("*")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .maxAge(3600);
    }

    /**
     * 인터셉터 등록
     *
     * @param registry InterceptorRegistry
     */
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // TODO: 로깅 인터셉터
        // TODO: 인증 인터셉터
    }
}
