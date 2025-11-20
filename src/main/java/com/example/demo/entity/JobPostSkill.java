package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * 채용공고-스킬 매핑 엔티티 (다대다 관계)
 */
@Entity
@Table(name = "job_post_skills")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class JobPostSkill {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "job_post_id")
    private JobPost jobPost;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "skill_id")
    private Skill skill;
}
