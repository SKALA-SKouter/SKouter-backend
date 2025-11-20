package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * 직무 카테고리 엔티티
 */
@Entity
@Table(name = "job_categories")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobCategory {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name; // 개발, 디자인, 마케팅 등
}
