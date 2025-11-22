package com.skouter.recruitai.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * JPA 설정
 * - JPA Auditing, QueryDSL 설정
 */
@Configuration
@EnableJpaRepositories(basePackages = "com.skouter.recruitai")
@EnableJpaAuditing
public class JpaConfig {

    // TODO: QueryDSL 빈 설정
    // TODO: JPA 메타모델 설정
}
