package com.skouter.recruitai.domain.job.service;

import com.skouter.recruitai.domain.job.entity.JobBookmark;
import com.skouter.recruitai.domain.job.repository.JobBookmarkRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 채용 공고 북마크 서비스
 * - 북마크 조회, 추가, 삭제 등 비즈니스 로직 처리
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class JobBookmarkService {

    private final JobBookmarkRepository jobBookmarkRepository;

    /**
     * 사용자의 모든 북마크 조회
     *
     * @param userId 사용자 ID
     * @return 북마크 목록
     */
    public List<JobBookmark> getUserBookmarks(Long userId) {
        return jobBookmarkRepository.findByUserId(userId);
    }

    /**
     * 북마크 여부 확인
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     * @return 북마크되어 있으면 true
     */
    public boolean isBookmarked(Long userId, Long jobId) {
        return jobBookmarkRepository.findByUserIdAndJobId(userId, jobId).isPresent();
    }

    /**
     * 북마크 추가
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     * @return 추가된 북마크
     */
    @Transactional
    public JobBookmark addBookmark(Long userId, Long jobId) {
        // 이미 북마크되어 있으면 반환
        return jobBookmarkRepository.findByUserIdAndJobId(userId, jobId)
                .orElseGet(() -> {
                    JobBookmark bookmark = JobBookmark.builder()
                            .userId(userId)
                            .jobId(jobId)
                            .build();
                    return jobBookmarkRepository.save(bookmark);
                });
    }

    /**
     * 북마크 제거
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     */
    @Transactional
    public void removeBookmark(Long userId, Long jobId) {
        jobBookmarkRepository.deleteByUserIdAndJobId(userId, jobId);
    }

    /**
     * 공고별 북마크 개수 조회
     *
     * @param jobId 공고 ID
     * @return 북마크 개수
     */
    public long getBookmarkCount(Long jobId) {
        return jobBookmarkRepository.countByJobId(jobId);
    }

    /**
     * 사용자별 북마크 개수 조회
     *
     * @param userId 사용자 ID
     * @return 북마크 개수
     */
    public long getUserBookmarkCount(Long userId) {
        return jobBookmarkRepository.countByUserId(userId);
    }
}
