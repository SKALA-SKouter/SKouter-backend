package com.skouter.recruitai.domain.auth.service;

import com.skouter.recruitai.domain.auth.dto.request.LoginRequest;
import com.skouter.recruitai.domain.auth.dto.request.SignupRequest;
import com.skouter.recruitai.domain.auth.dto.response.AuthResponse;
import com.skouter.recruitai.domain.auth.dto.response.TokenResponse;
import com.skouter.recruitai.domain.user.entity.User;
import com.skouter.recruitai.domain.user.repository.UserRepository;
import com.skouter.recruitai.global.error.exception.BusinessException;
import com.skouter.recruitai.global.error.exception.InvalidValueException;
import com.skouter.recruitai.global.error.ErrorCode;
import com.skouter.recruitai.global.error.exception.EntityNotFoundException;
import com.skouter.recruitai.global.util.EncryptionUtil;
import com.skouter.recruitai.global.util.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 인증 서비스
 * - 회원가입, 로그인, 토큰 갱신 등 인증 관련 비즈니스 로직 처리
 */
@Service
@Transactional
@RequiredArgsConstructor
public class AuthService {

    private final UserRepository userRepository;
    private final TokenService tokenService;
    private final JwtUtil jwtUtil;
    private final EncryptionUtil encryptionUtil;

    /**
     * 회원가입 처리
     *
     * @param request 회원가입 요청 정보
     * @return 인증 응답 (사용자 정보 및 토큰)
     */
    public AuthResponse signup(SignupRequest request) {
        // 이메일 중복 확인
        if (userRepository.existsByEmail(request.getEmail())) {
            throw InvalidValueException.duplicateEmail();
        }

        // 사용자 생성
        User user = User.builder()
                .email(request.getEmail())
                .name(request.getName())
                .password(encryptionUtil.encryptPassword(request.getPassword()))
                .build();

        User savedUser = userRepository.save(user);

        // 토큰 생성
        String accessToken = jwtUtil.generateToken(savedUser.getId(), savedUser.getEmail());
        String refreshToken = jwtUtil.generateRefreshToken(savedUser.getId());

        // RefreshToken DB 저장
        tokenService.saveRefreshToken(savedUser.getId(), refreshToken);

        return AuthResponse.builder()
                .userId(savedUser.getId())
                .email(savedUser.getEmail())
                .name(savedUser.getName())
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .build();
    }

    /**
     * 로그인 처리
     *
     * @param request 로그인 요청 정보
     * @return 인증 응답 (사용자 정보 및 토큰)
     */
    public AuthResponse login(LoginRequest request) {
        // 사용자 조회
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new EntityNotFoundException(ErrorCode.USER_NOT_FOUND));

        // 비밀번호 검증
        if (!encryptionUtil.matchesPassword(request.getPassword(), user.getPassword())) {
            throw InvalidValueException.invalidPassword();
        }

        // 토큰 생성
        String accessToken = jwtUtil.generateToken(user.getId(), user.getEmail());
        String refreshToken = jwtUtil.generateRefreshToken(user.getId());

        // RefreshToken DB 저장
        tokenService.saveRefreshToken(user.getId(), refreshToken);

        return AuthResponse.builder()
                .userId(user.getId())
                .email(user.getEmail())
                .name(user.getName())
                .accessToken(accessToken)
                .refreshToken(refreshToken)
                .build();
    }

    /**
     * 토큰 갱신 처리
     *
     * @param refreshToken 갱신 토큰
     * @return 새로운 토큰 정보
     */
    public TokenResponse refreshToken(String refreshToken) {
        // RefreshToken 유효성 검증
        if (!jwtUtil.isTokenValid(refreshToken)) {
            throw new EntityNotFoundException(ErrorCode.INVALID_TOKEN);
        }

        // UserId 추출
        Long userId = jwtUtil.extractUserId(refreshToken);

        String email = jwtUtil.extractEmail(refreshToken);
        // 새 AccessToken 생성
        String newAccessToken = jwtUtil.generateToken(userId, email);

        return TokenResponse.builder()
                .accessToken(newAccessToken)
                .refreshToken(refreshToken)
                .build();
    }

    /**
     * 로그아웃 처리
     *
     * @param token 현재 토큰
     */
    public void logout(String token) {
        Long userId = jwtUtil.extractUserId(token);
        tokenService.deleteRefreshToken(userId);
    }
}
