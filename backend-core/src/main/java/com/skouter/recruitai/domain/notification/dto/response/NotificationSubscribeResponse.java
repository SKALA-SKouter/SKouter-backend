package com.skouter.recruitai.domain.notification.dto.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 알림 구독 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class NotificationSubscribeResponse {

    /**
     * 구독 ID
     */
    private Long subscriptionId;

    /**
     * 채널
     */
    private String channel;

    /**
     * 활성 여부
     */
    private Boolean isActive;
}
