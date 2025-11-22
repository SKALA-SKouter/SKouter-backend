package com.skouter.recruitai.domain.notification.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

/**
 * Slack 알림 서비스
 * - Slack Webhook을 통한 알림 전송
 */
@Service
@RequiredArgsConstructor
public class SlackNotificationService {

    /**
     * Slack 메시지 전송
     *
     * @param webhookUrl Webhook URL
     * @param message 메시지 내용
     */
    public void sendMessage(String webhookUrl, String message) {
        // TODO: Slack Webhook을 통한 메시지 전송
    }

    /**
     * 풍부한 메시지 전송
     *
     * @param webhookUrl Webhook URL
     * @param payload 페이로드
     */
    public void sendRichMessage(String webhookUrl, Object payload) {
        // TODO: Block Kit을 사용한 풍부한 메시지 전송
    }
}
