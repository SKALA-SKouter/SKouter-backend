package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.*;

/**
 * 회사 엔티티
 */
@Entity
@Table(name = "companies")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Company {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    private String address;
    private String industry;
    private String description;
}
