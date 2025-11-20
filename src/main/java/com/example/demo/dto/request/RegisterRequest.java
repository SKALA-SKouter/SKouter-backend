package com.example.demo.dto.request;

import lombok.Data;

/**
 * 회원가입 요청 DTO
 */
@Data
public class RegisterRequest {
    private String name;
    private String email;
    private String password;
}
