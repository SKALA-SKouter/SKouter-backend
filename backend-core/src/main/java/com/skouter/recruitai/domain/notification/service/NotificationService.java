package com.skouter.recruitai.domain.notification.service;

import com.skouter.recruitai.domain.notification.entity.NotificationSubscription;
import com.skouter.recruitai.domain.notification.repository.NotificationSubscriptionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 알림 서비스
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class NotificationService {

    private final NotificationSubscriptionRepository subscriptionRepository;

    /**
     * 사용자 구독 목록 조회
     */
    public List<NotificationSubscription> getUserSubscriptions(Long userId) {
        return subscriptionRepository.findByUserId(userId);
    }

    /**
     * 구독 추가
     */
    @Transactional
    public NotificationSubscription subscribe(Long userId, String channel, String webhookUrl) {
        NotificationSubscription subscription = NotificationSubscription.builder()
                .userId(userId)
                .channel(channel)
                .webhookUrl(webhookUrl)
                .isActive(true)
                .build();
        return subscriptionRepository.save(subscription);
    }

    /**
     * 구독 해제
     */
    @Transactional
    public void unsubscribe(Long userId, String channel) {
        subscriptionRepository.deleteByUserIdAndChannel(userId, channel);
    }
}
