package com.skouter.recruitai.domain.user.dto.response;

import com.skouter.recruitai.domain.user.entity.User;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 사용자 정보 응답 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserResponse {

    /**
     * 사용자 ID
     */
    private Long id;

    /**
     * 이메일
     */
    private String email;

    /**
     * 이름
     */
    private String name;

    /**
     * 회사명
     */
    private String company;

    /**
     * 직위
     */
    private String position;

    /**
     * 전화번호
     */
    private String phone;

    /**
     * 프로필 이미지 URL
     */
    private String profileImage;

    /**
     * 자기소개
     */
    private String bio;

    /**
     * 활성 상태
     */
    private Boolean isActive;

    /**
     * 생성일시
     */
    private LocalDateTime createdAt;

    /**
     * 수정일시
     */
    private LocalDateTime updatedAt;

    /**
     * User 엔티티를 DTO로 변환
     *
     * @param user User 엔티티
     * @return UserResponse DTO
     */
    public static UserResponse fromEntity(User user) {
        return UserResponse.builder()
                .id(user.getId())
                .email(user.getEmail())
                .name(user.getName())
                .company(user.getCompany())
                .position(user.getPosition())
                .phone(user.getPhone())
                .profileImage(user.getProfileImage())
                .bio(user.getBio())
                .isActive(user.getIsActive())
                .createdAt(user.getCreatedAt())
                .updatedAt(user.getUpdatedAt())
                .build();
    }
}
