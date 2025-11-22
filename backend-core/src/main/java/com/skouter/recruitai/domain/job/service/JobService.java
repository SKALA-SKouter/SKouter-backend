package com.skouter.recruitai.domain.job.service;

import com.skouter.recruitai.domain.job.dto.response.JobDetailResponse;
import com.skouter.recruitai.domain.job.dto.response.JobListResponse;
import com.skouter.recruitai.domain.job.entity.Job;
import com.skouter.recruitai.domain.job.repository.JobRepository;
import com.skouter.recruitai.global.error.exception.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;

/**
 * 채용 공고 서비스
 * - 공고 조회, 생성, 수정, 삭제 등 비즈니스 로직 처리
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class JobService {

    private final JobRepository jobRepository;

    /**
     * 공고 상세 정보 조회
     *
     * @param jobId 공고 ID
     * @return 공고 상세 응답 DTO
     */
    public JobDetailResponse getJobDetail(Long jobId) {
        Job job = jobRepository.findById(jobId)
                .orElseThrow(EntityNotFoundException::jobNotFound);
        return JobDetailResponse.fromEntity(job);
    }

    /**
     * 모든 공고 목록 조회 (페이징)
     *
     * @param pageable 페이징 정보
     * @return 공고 목록 페이지
     */
    public Page<JobListResponse> getAllJobs(Pageable pageable) {
        return jobRepository.findAll(pageable)
                .map(JobListResponse::fromEntity);
    }

    /**
     * 기업별 공고 목록 조회
     *
     * @param companyId 기업 ID
     * @param pageable 페이징 정보
     * @return 공고 목록 페이지
     */
    public Page<JobListResponse> getJobsByCompanyId(Long companyId, Pageable pageable) {
        return jobRepository.findByCompanyId(companyId, pageable)
                .map(JobListResponse::fromEntity);
    }

    /**
     * 공고 제목으로 검색
     *
     * @param title 제목
     * @param pageable 페이징 정보
     * @return 공고 목록 페이지
     */
    public Page<JobListResponse> searchJobsByTitle(String title, Pageable pageable) {
        return jobRepository.findByTitleContaining(title, pageable)
                .map(JobListResponse::fromEntity);
    }

    /**
     * 공고 생성
     *
     * @param companyId 기업 ID
     * @param title 제목
     * @param content 내용
     * @param location 위치
     * @param experienceLevel 경력 수준
     * @param salary 급여
     * @param deadline 마감일
     * @return 생성된 공고 상세 응답 DTO
     */
    @Transactional
    public JobDetailResponse createJob(Long companyId, String title, String content,
                                        String location, String experienceLevel,
                                        String salary, LocalDateTime deadline) {
        Job job = Job.builder()
                .companyId(companyId)
                .title(title)
                .content(content)
                .location(location)
                .experienceLevel(experienceLevel)
                .salary(salary)
                .deadline(deadline)
                .isActive(true)
                .build();

        Job savedJob = jobRepository.save(job);
        return JobDetailResponse.fromEntity(savedJob);
    }

    /**
     * 공고 수정
     *
     * @param jobId 공고 ID
     * @param title 제목
     * @param content 내용
     * @param location 위치
     * @param experienceLevel 경력 수준
     * @param salary 급여
     * @param deadline 마감일
     * @return 수정된 공고 상세 응답 DTO
     */
    @Transactional
    public JobDetailResponse updateJob(Long jobId, String title, String content,
                                        String location, String experienceLevel,
                                        String salary, LocalDateTime deadline) {
        Job job = jobRepository.findById(jobId)
                .orElseThrow(EntityNotFoundException::jobNotFound);

        job.updateJob(title, content, location, experienceLevel, salary, deadline);

        return JobDetailResponse.fromEntity(job);
    }

    /**
     * 공고 삭제
     *
     * @param jobId 공고 ID
     */
    @Transactional
    public void deleteJob(Long jobId) {
        Job job = jobRepository.findById(jobId)
                .orElseThrow(EntityNotFoundException::jobNotFound);
        jobRepository.delete(job);
    }
}
