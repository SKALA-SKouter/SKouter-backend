package com.skouter.recruitai.global.common.response;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.domain.Page;

import java.util.List;

/**
 * 페이징 응답 DTO
 * - 페이징된 데이터 반환
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class PageResponse<T> {

    /**
     * 데이터 목록
     */
    private List<T> content;

    /**
     * 현재 페이지 번호 (0-based)
     */
    private int page;

    /**
     * 페이지 크기
     */
    private int size;

    /**
     * 전체 데이터 개수
     */
    private long totalElements;

    /**
     * 전체 페이지 개수
     */
    private int totalPages;

    /**
     * 첫 페이지 여부
     */
    private boolean isFirst;

    /**
     * 마지막 페이지 여부
     */
    private boolean isLast;

    /**
     * Page 객체를 PageResponse로 변환
     *
     * @param page Spring Data Page 객체
     * @param <T> 데이터 타입
     * @return PageResponse
     */
    public static <T> PageResponse<T> of(Page<T> page) {
        return PageResponse.<T>builder()
                .content(page.getContent())
                .page(page.getNumber())
                .size(page.getSize())
                .totalElements(page.getTotalElements())
                .totalPages(page.getTotalPages())
                .isFirst(page.isFirst())
                .isLast(page.isLast())
                .build();
    }
}
