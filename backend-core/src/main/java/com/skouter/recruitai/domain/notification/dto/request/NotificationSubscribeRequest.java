package com.skouter.recruitai.domain.notification.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 알림 구독 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class NotificationSubscribeRequest {

    /**
     * 사용자 ID
     */
    private Long userId;

    /**
     * 채널 (slack, email 등)
     */
    private String channel;

    /**
     * Webhook URL
     */
    private String webhookUrl;
}
