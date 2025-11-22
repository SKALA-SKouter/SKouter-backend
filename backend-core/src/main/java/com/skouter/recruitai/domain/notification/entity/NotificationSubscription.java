package com.skouter.recruitai.domain.notification.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 알림 구독 엔티티
 * - 사용자의 알림 채널 구독 정보
 */
@Entity
@Table(name = "notification_subscriptions", indexes = {
        @Index(name = "idx_user_id", columnList = "user_id"),
        @Index(name = "idx_channel", columnList = "channel")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class NotificationSubscription extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false)
    private String channel;

    @Column
    private String webhookUrl;

    @Column
    private Boolean isActive;

    /**
     * 구독 활성화
     */
    public void activate() {
        this.isActive = true;
    }

    /**
     * 구독 비활성화
     */
    public void deactivate() {
        this.isActive = false;
    }
}
