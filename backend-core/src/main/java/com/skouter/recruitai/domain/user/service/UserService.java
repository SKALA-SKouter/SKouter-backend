package com.skouter.recruitai.domain.user.service;

import com.skouter.recruitai.domain.user.dto.request.UserUpdateRequest;
import com.skouter.recruitai.domain.user.dto.response.UserResponse;
import com.skouter.recruitai.domain.user.entity.User;
import com.skouter.recruitai.domain.user.repository.UserRepository;
import com.skouter.recruitai.global.error.exception.EntityNotFoundException;
import com.skouter.recruitai.global.util.EncryptionUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 사용자 서비스
 * - 사용자 정보 조회, 수정 등 비즈니스 로직 처리
 */
@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final EncryptionUtil encryptionUtil;

    /**
     * 사용자 ID로 사용자 정보 조회
     *
     * @param userId 사용자 ID
     * @return 사용자 응답 DTO
     */
    public UserResponse getUserById(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(EntityNotFoundException::userNotFound);
        return UserResponse.fromEntity(user);
    }

    /**
     * 이메일로 사용자 정보 조회
     *
     * @param email 이메일
     * @return 사용자 응답 DTO
     */
    public UserResponse getUserByEmail(String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(EntityNotFoundException::userNotFound);
        return UserResponse.fromEntity(user);
    }

    /**
     * 사용자 정보 수정
     *
     * @param userId 사용자 ID
     * @param request 수정 요청 DTO
     * @return 수정된 사용자 응답 DTO
     */
    @Transactional
    public UserResponse updateUser(Long userId, UserUpdateRequest request) {
        User user = userRepository.findById(userId)
                .orElseThrow(EntityNotFoundException::userNotFound);

        user.updateProfile(
                request.getName(),
                request.getCompany(),
                request.getPosition(),
                request.getPhone(),
                request.getBio()
        );

        return UserResponse.fromEntity(user);
    }

    /**
     * 사용자 비밀번호 변경
     *
     * @param userId 사용자 ID
     * @param newPassword 새 비밀번호
     */
    @Transactional
    public void updatePassword(Long userId, String newPassword) {
        User user = userRepository.findById(userId)
                .orElseThrow(EntityNotFoundException::userNotFound);

        String encryptedPassword = encryptionUtil.encryptPassword(newPassword);
        user.updatePassword(encryptedPassword);
    }

    /**
     * 사용자 삭제 (소프트 삭제)
     *
     * @param userId 사용자 ID
     */
    @Transactional
    public void deleteUser(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(EntityNotFoundException::userNotFound);

        // 소프트 삭제: 활성 상태를 false로 변경
        // user.setIsActive(false);
        // 또는 엔티티 삭제
        userRepository.delete(user);
    }
}
