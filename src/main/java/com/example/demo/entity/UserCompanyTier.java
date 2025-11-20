package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * 사용자-회사 티어 매핑 엔티티
 */
@Entity
@Table(name = "user_company_tiers")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserCompanyTier {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "company_id")
    private Company company;

    private Integer tier; // 1, 2, 3 등
}
