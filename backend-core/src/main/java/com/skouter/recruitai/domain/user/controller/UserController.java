package com.skouter.recruitai.domain.user.controller;

import com.skouter.recruitai.domain.user.dto.request.UserUpdateRequest;
import com.skouter.recruitai.domain.user.dto.response.UserResponse;
import com.skouter.recruitai.domain.user.service.UserService;
import com.skouter.recruitai.global.common.response.ApiResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 사용자 관련 API 엔드포인트
 * - 사용자 정보 조회, 수정, 삭제
 */
@RestController
@RequestMapping("/api/users")
@RequiredArgsConstructor
public class UserController {

    private final UserService userService;

    /**
     * 사용자 정보 조회 (ID 기반)
     *
     * @param userId 사용자 ID
     * @return 사용자 정보
     */
    @GetMapping("/{userId}")
    public ResponseEntity<ApiResponse<UserResponse>> getUserById(@PathVariable Long userId) {
        UserResponse response = userService.getUserById(userId);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 사용자 정보 조회 (이메일 기반)
     *
     * @param email 사용자 이메일
     * @return 사용자 정보
     */
    @GetMapping("/email/{email}")
    public ResponseEntity<ApiResponse<UserResponse>> getUserByEmail(@PathVariable String email) {
        UserResponse response = userService.getUserByEmail(email);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 사용자 정보 수정
     *
     * @param userId 사용자 ID
     * @param request 수정 요청 DTO
     * @return 수정된 사용자 정보
     */
    @PutMapping("/{userId}")
    public ResponseEntity<ApiResponse<UserResponse>> updateUser(
            @PathVariable Long userId,
            @RequestBody UserUpdateRequest request) {
        UserResponse response = userService.updateUser(userId, request);
        return ResponseEntity.ok(ApiResponse.ok(response));
    }

    /**
     * 사용자 삭제
     *
     * @param userId 사용자 ID
     * @return 성공 응답
     */
    @DeleteMapping("/{userId}")
    public ResponseEntity<ApiResponse<Void>> deleteUser(@PathVariable Long userId) {
        userService.deleteUser(userId);
        return ResponseEntity.ok(ApiResponse.ok());
    }
}
