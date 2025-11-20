package com.example.demo.dto.request;

import lombok.Data;

/**
 * 로그인 요청 DTO
 */
@Data
public class LoginRequest {
    private String email;
    private String password;
}
