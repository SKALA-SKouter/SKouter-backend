package com.skouter.recruitai.domain.notification.repository;

import com.skouter.recruitai.domain.notification.entity.NotificationSubscription;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 알림 구독 저장소
 */
@Repository
public interface NotificationSubscriptionRepository extends JpaRepository<NotificationSubscription, Long> {

    List<NotificationSubscription> findByUserId(Long userId);

    Optional<NotificationSubscription> findByUserIdAndChannel(Long userId, String channel);

    List<NotificationSubscription> findByChannelAndIsActive(String channel, Boolean isActive);

    void deleteByUserIdAndChannel(Long userId, String channel);
}
