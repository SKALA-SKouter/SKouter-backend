package com.skouter.recruitai.domain.user.dto.request;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 사용자 정보 수정 요청 DTO
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class UserUpdateRequest {

    /**
     * 사용자 이름
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
     * 자기소개
     */
    private String bio;
}
