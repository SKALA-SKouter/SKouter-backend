package com.skouter.recruitai.domain.job.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 채용 공고 북마크 엔티티
 * - 사용자가 저장한 채용 공고 정보
 */
@Entity
@Table(name = "job_bookmarks", indexes = {
        @Index(name = "idx_user_id", columnList = "user_id"),
        @Index(name = "idx_job_id", columnList = "job_id"),
        @Index(name = "idx_user_job", columnList = "user_id,job_id", unique = true)
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobBookmark extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long userId;

    @Column(nullable = false)
    private Long jobId;

    /**
     * 북마크 제거 (논리 삭제)
     */
    public void remove() {
        // 논리 삭제 처리 로직
    }
}
