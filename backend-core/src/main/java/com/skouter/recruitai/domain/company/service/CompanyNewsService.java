package com.skouter.recruitai.domain.company.service;

import com.skouter.recruitai.domain.company.dto.response.CompanyNewsResponse;
import com.skouter.recruitai.domain.company.entity.CompanyNews;
import com.skouter.recruitai.domain.company.repository.CompanyNewsRepository;
import com.skouter.recruitai.global.error.exception.EntityNotFoundException;
import com.skouter.recruitai.global.error.ErrorCode;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

/**
 * 기업 뉴스 서비스
 * - 기업 뉴스 조회, 생성, 수정, 삭제 등 비즈니스 로직 처리
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class CompanyNewsService {

    private final CompanyNewsRepository companyNewsRepository;

    /**
     * 기업별 뉴스 목록 조회
     *
     * @param companyId 기업 ID
     * @return 뉴스 응답 DTO 목록
     */
    public List<CompanyNewsResponse> getNewsByCompanyId(Long companyId) {
        return companyNewsRepository.findByCompanyIdOrderByPublishedDateDesc(companyId)
                .stream()
                .map(CompanyNewsResponse::fromEntity)
                .collect(Collectors.toList());
    }

    /**
     * 뉴스 상세 정보 조회
     *
     * @param newsId 뉴스 ID
     * @return 뉴스 응답 DTO
     */
    public CompanyNewsResponse getNewsDetail(Long newsId) {
        CompanyNews news = companyNewsRepository.findById(newsId)
                .orElseThrow(() -> new EntityNotFoundException(ErrorCode.ENTITY_NOT_FOUND, "뉴스를 찾을 수 없습니다."));
        return CompanyNewsResponse.fromEntity(news);
    }

    /**
     * 기업별 뉴스 생성
     *
     * @param companyId 기업 ID
     * @param title 제목
     * @param content 내용
     * @param source 출처
     * @param sourceUrl 출처 URL
     * @param summary 요약
     * @param publishedDate 발행일
     * @return 생성된 뉴스 응답 DTO
     */
    @Transactional
    public CompanyNewsResponse createNews(Long companyId, String title, String content,
                                           String source, String sourceUrl, String summary,
                                           String publishedDate) {
        CompanyNews news = CompanyNews.builder()
                .companyId(companyId)
                .title(title)
                .content(content)
                .source(source)
                .sourceUrl(sourceUrl)
                .summary(summary)
                .publishedDate(publishedDate)
                .build();

        CompanyNews savedNews = companyNewsRepository.save(news);
        return CompanyNewsResponse.fromEntity(savedNews);
    }

    /**
     * 뉴스 정보 수정
     *
     * @param newsId 뉴스 ID
     * @param title 제목
     * @param content 내용
     * @param summary 요약
     * @return 수정된 뉴스 응답 DTO
     */
    @Transactional
    public CompanyNewsResponse updateNews(Long newsId, String title, String content, String summary) {
        CompanyNews news = companyNewsRepository.findById(newsId)
                .orElseThrow(() -> new EntityNotFoundException(ErrorCode.ENTITY_NOT_FOUND, "뉴스를 찾을 수 없습니다."));

        news.updateNews(title, content, summary);

        return CompanyNewsResponse.fromEntity(news);
    }

    /**
     * 뉴스 삭제
     *
     * @param newsId 뉴스 ID
     */
    @Transactional
    public void deleteNews(Long newsId) {
        CompanyNews news = companyNewsRepository.findById(newsId)
                .orElseThrow(() -> new EntityNotFoundException(ErrorCode.ENTITY_NOT_FOUND, "뉴스를 찾을 수 없습니다."));
        companyNewsRepository.delete(news);
    }
}
