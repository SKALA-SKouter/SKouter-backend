package com.skouter.recruitai.domain.notification.controller;

import com.skouter.recruitai.domain.notification.dto.request.NotificationSubscribeRequest;
import com.skouter.recruitai.domain.notification.dto.response.NotificationSubscribeResponse;
import com.skouter.recruitai.domain.notification.service.NotificationService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 알림 관련 API 엔드포인트
 */
@RestController
@RequestMapping("/api/notifications")
@RequiredArgsConstructor
public class NotificationController {

    private final NotificationService notificationService;

    /**
     * 알림 구독
     */
    @PostMapping("/subscribe")
    public ResponseEntity<ApiResponse<NotificationSubscribeResponse>> subscribe(
            @RequestBody NotificationSubscribeRequest request) {
        var subscription = notificationService.subscribe(
                request.getUserId(),
                request.getChannel(),
                request.getWebhookUrl());

        NotificationSubscribeResponse response = NotificationSubscribeResponse.builder()
                .subscriptionId(subscription.getId())
                .channel(subscription.getChannel())
                .isActive(subscription.getIsActive())
                .build();

        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok(response));
    }

    /**
     * 알림 구독 해제
     */
    @DeleteMapping("/unsubscribe")
    public ResponseEntity<ApiResponse<Void>> unsubscribe(
            @RequestParam Long userId,
            @RequestParam String channel) {
        notificationService.unsubscribe(userId, channel);
        return ResponseEntity.ok(ApiResponse.ok());
    }
}
