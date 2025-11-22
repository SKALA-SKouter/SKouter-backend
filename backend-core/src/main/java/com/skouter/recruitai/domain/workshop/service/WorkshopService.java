package com.skouter.recruitai.domain.workshop.service;

import com.skouter.recruitai.domain.workshop.entity.JobTemplate;
import com.skouter.recruitai.domain.workshop.repository.TemplateRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 공고 제작소 서비스
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class WorkshopService {

    private final TemplateRepository templateRepository;

    /**
     * 공고 생성
     */
    @Transactional
    public Object generateJob(Long templateId, Long companyId) {
        // TODO: AI를 통한 공고 생성
        return null;
    }

    /**
     * 사용자 템플릿 조회
     */
    public List<JobTemplate> getUserTemplates(Long userId) {
        return templateRepository.findByUserId(userId);
    }
}
