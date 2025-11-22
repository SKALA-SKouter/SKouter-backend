package com.skouter.recruitai.domain.job.repository;

import com.skouter.recruitai.domain.job.entity.JobBookmark;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 채용 공고 북마크 저장소
 * - 사용자 북마크 데이터 접근
 */
@Repository
public interface JobBookmarkRepository extends JpaRepository<JobBookmark, Long> {

    /**
     * 사용자 ID로 북마크 목록 조회
     *
     * @param userId 사용자 ID
     * @return 북마크 목록
     */
    List<JobBookmark> findByUserId(Long userId);

    /**
     * 사용자와 공고 ID로 북마크 조회
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     * @return 북마크 엔티티
     */
    Optional<JobBookmark> findByUserIdAndJobId(Long userId, Long jobId);

    /**
     * 공고 ID로 북마크 개수 조회
     *
     * @param jobId 공고 ID
     * @return 북마크 개수
     */
    long countByJobId(Long jobId);

    /**
     * 사용자별 북마크 개수 조회
     *
     * @param userId 사용자 ID
     * @return 북마크 개수
     */
    long countByUserId(Long userId);

    /**
     * 사용자의 북마크 삭제
     *
     * @param userId 사용자 ID
     * @param jobId 공고 ID
     */
    void deleteByUserIdAndJobId(Long userId, Long jobId);
}
