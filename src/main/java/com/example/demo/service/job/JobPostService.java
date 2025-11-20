package com.example.demo.service.job;

import com.example.demo.repository.JobPostRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 채용공고 비즈니스 로직
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class JobPostService {

    private final JobPostRepository jobPostRepository;

    // TODO: 검색, 필터링, CRUD 메서드 구현
}
