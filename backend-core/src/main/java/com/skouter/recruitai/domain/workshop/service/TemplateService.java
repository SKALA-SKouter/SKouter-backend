package com.skouter.recruitai.domain.workshop.service;

import com.skouter.recruitai.domain.workshop.entity.JobTemplate;
import com.skouter.recruitai.domain.workshop.repository.TemplateRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * 템플릿 서비스
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class TemplateService {

    private final TemplateRepository templateRepository;

    /**
     * 템플릿 조회
     */
    public JobTemplate getTemplate(Long templateId) {
        return templateRepository.findById(templateId).orElse(null);
    }

    /**
     * 템플릿 생성
     */
    @Transactional
    public JobTemplate createTemplate(String name, String content, String description, Long userId) {
        JobTemplate template = JobTemplate.builder()
                .name(name)
                .content(content)
                .description(description)
                .userId(userId)
                .build();
        return templateRepository.save(template);
    }

    /**
     * 템플릿 수정
     */
    @Transactional
    public JobTemplate updateTemplate(Long templateId, String name, String content, String description) {
        JobTemplate template = templateRepository.findById(templateId).orElse(null);
        if (template != null) {
            template.update(name, content, description);
        }
        return template;
    }

    /**
     * 템플릿 삭제
     */
    @Transactional
    public void deleteTemplate(Long templateId) {
        templateRepository.deleteById(templateId);
    }
}
