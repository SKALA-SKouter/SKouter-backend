package com.skouter.recruitai.domain.company.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 기업 메모 엔티티
 * - 사용자가 기업에 대해 남긴 메모 정보 저장
 */
@Entity
@Table(name = "company_memos", indexes = {
        @Index(name = "idx_company_id", columnList = "company_id"),
        @Index(name = "idx_user_id", columnList = "user_id")
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class CompanyMemo extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Long companyId;

    @Column(nullable = false)
    private Long userId;

    @Column(columnDefinition = "LONGTEXT")
    private String content;

    /**
     * 메모 내용 업데이트
     *
     * @param content 새로운 메모 내용
     */
    public void updateContent(String content) {
        this.content = content;
    }
}
