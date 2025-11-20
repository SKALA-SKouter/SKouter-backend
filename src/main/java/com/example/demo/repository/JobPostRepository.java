package com.example.demo.repository;

import com.example.demo.entity.JobPost;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 채용공고 데이터 접근
 */
@Repository
public interface JobPostRepository extends JpaRepository<JobPost, Long> {
    // 커스텀 쿼리 추가 가능
}
