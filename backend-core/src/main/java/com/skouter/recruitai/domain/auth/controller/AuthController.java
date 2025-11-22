package com.skouter.recruitai.domain.auth.controller;

import com.skouter.recruitai.domain.auth.dto.request.LoginRequest;
import com.skouter.recruitai.domain.auth.dto.request.SignupRequest;
import com.skouter.recruitai.domain.auth.dto.response.AuthResponse;
import com.skouter.recruitai.domain.auth.dto.response.TokenResponse;
import com.skouter.recruitai.domain.auth.service.AuthService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 인증 관련 API 엔드포인트
 * - 로그인, 회원가입, 토큰 갱신
 */
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthService authService;

    /**
     * 사용자 회원가입
     *
     * @param request 회원가입 요청 DTO
     * @return 인증 응답 (사용자 정보 및 토큰)
     */
    @PostMapping("/signup")
    public ResponseEntity<ApiResponse<AuthResponse>> signup(@RequestBody SignupRequest request) {
        AuthResponse response = authService.signup(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.ok(response));
    }

    /**
     * 사용자 로그인
     *
     * @param request 로그인 요청 DTO
     * @return 인증 응답 (사용자 정보 및 토큰)
     */
    @PostMapping("/login")
    public ResponseEntity<ApiResponse<AuthResponse>> login(@RequestBody LoginRequest request) {
        AuthResponse response = authService.login(request);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 토큰 갱신
     *
     * @param refreshToken 갱신 토큰
     * @return 새 토큰 정보
     */
    @PostMapping("/refresh")
    public ResponseEntity<ApiResponse<TokenResponse>> refreshToken(@RequestParam String refreshToken) {
        TokenResponse response = authService.refreshToken(refreshToken);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 로그아웃
     *
     * @param token 현재 사용 중인 토큰
     * @return 성공 응답
     */
    @PostMapping("/logout")
    public ResponseEntity<ApiResponse<Void>> logout(@RequestParam String token) {
        authService.logout(token);
        return ResponseEntity.ok(ApiResponse.ok());
    }
}
