package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * 직무 역할 엔티티
 */
@Entity
@Table(name = "job_roles")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobRole {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name; // 백엔드, 프론트엔드, DevOps 등

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "category_id")
    private JobCategory category;
}
