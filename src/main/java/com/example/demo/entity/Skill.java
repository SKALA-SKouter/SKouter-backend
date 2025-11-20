package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * 스킬 엔티티
 */
@Entity
@Table(name = "skills")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Skill {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    private String category; // 언어, 프레임워크, 도구 등
}
