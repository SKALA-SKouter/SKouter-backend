package com.skouter.recruitai.domain.auth.token;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * RefreshToken 엔티티
 * - 사용자별 Refresh 토큰 저장
 */
@Entity
@Table(name = "refresh_tokens", indexes = {
        @Index(name = "idx_user_id", columnList = "user_id")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RefreshToken extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false, columnDefinition = "LONGTEXT")
    private String token;
}
