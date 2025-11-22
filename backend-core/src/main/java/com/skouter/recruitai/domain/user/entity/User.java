package com.skouter.recruitai.domain.user.entity;

import com.skouter.recruitai.global.common.entity.BaseEntity;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import jakarta.persistence.*;

/**
 * 사용자 엔티티
 * - 회원 정보 저장
 */
@Entity
@Table(name = "users", indexes = {
        @Index(name = "idx_email", columnList = "email", unique = true)
})
@Getter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class User extends BaseEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String password;

    @Column
    private String company;

    @Column
    private String position;

    @Column
    private String phone;

    @Column
    private String profileImage;

    @Column
    private String bio;

    @Column(nullable = false)
    @Builder.Default
    private Boolean isActive = true;

    /**
     * 사용자 정보 수정
     *
     * @param name 이름
     * @param company 회사명
     * @param position 직위
     * @param phone 전화번호
     * @param bio 소개
     */
    public void updateProfile(String name, String company, String position, String phone, String bio) {
        if (name != null) this.name = name;
        if (company != null) this.company = company;
        if (position != null) this.position = position;
        if (phone != null) this.phone = phone;
        if (bio != null) this.bio = bio;
    }

    /**
     * 비밀번호 변경
     *
     * @param newPassword 새 비밀번호 (암호화된 값)
     */
    public void updatePassword(String newPassword) {
        this.password = newPassword;
    }
}
