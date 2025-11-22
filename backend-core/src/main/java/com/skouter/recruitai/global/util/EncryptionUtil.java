package com.skouter.recruitai.global.util;

import lombok.extern.slf4j.Slf4j;

/**
 * 암호화 관련 유틸리티 클래스
 * 사용자 비밀번호 등의 민감한 정보를 암호화합니다.
 *
 * 주의: Spring Security의 BCryptPasswordEncoder는 ApplicationContext에서 주입받아야 합니다.
 * 이 클래스는 기본적인 Base64 인코딩/디코딩 기능만 제공합니다.
 */
@Slf4j
public class EncryptionUtil {

    /**
     * 평문 비밀번호를 암호화합니다.
     *
     * @param rawPassword 평문 비밀번호
     * @return 암호화된 비밀번호
     *
     * 주의: 실제 구현은 Spring Security의 PasswordEncoder를 사용하세요.
     * 여기서는 예시만 제공합니다.
     */
    public static String encryptPassword(String rawPassword) {
        if (rawPassword == null || rawPassword.isEmpty()) {
            throw new IllegalArgumentException("비밀번호는 null이거나 빈 문자열이 될 수 없습니다.");
        }
        // Spring Security의 BCryptPasswordEncoder 또는 다른 PasswordEncoder 사용 권장
        return rawPassword; // 임시 구현
    }

    /**
     * 평문 비밀번호와 암호화된 비밀번호가 일치하는지 확인합니다.
     *
     * @param rawPassword 평문 비밀번호
     * @param encryptedPassword 암호화된 비밀번호
     * @return 일치 여부 (true: 일치, false: 불일치)
     *
     * 주의: 실제 구현은 Spring Security의 PasswordEncoder를 사용하세요.
     * 여기서는 예시만 제공합니다.
     */
    public static boolean matchesPassword(String rawPassword, String encryptedPassword) {
        if (rawPassword == null || encryptedPassword == null) {
            return false;
        }
        try {
            // Spring Security의 BCryptPasswordEncoder 또는 다른 PasswordEncoder 사용 권장
            return rawPassword.equals(encryptedPassword); // 임시 구현
        } catch (Exception e) {
            log.error("비밀번호 비교 중 오류 발생: {}", e.getMessage());
            return false;
        }
    }

    /**
     * 문자열을 Base64로 인코딩합니다.
     *
     * @param str 대상 문자열
     * @return Base64 인코딩된 문자열
     */
    public static String encodeBase64(String str) {
        if (str == null) {
            return null;
        }
        return java.util.Base64.getEncoder().encodeToString(str.getBytes());
    }

    /**
     * Base64 인코딩된 문자열을 디코딩합니다.
     *
     * @param encodedStr Base64 인코딩된 문자열
     * @return 디코딩된 문자열
     */
    public static String decodeBase64(String encodedStr) {
        if (encodedStr == null) {
            return null;
        }
        try {
            return new String(java.util.Base64.getDecoder().decode(encodedStr));
        } catch (IllegalArgumentException e) {
            log.error("Base64 디코딩 실패: {}", e.getMessage());
            throw new IllegalArgumentException("유효하지 않은 Base64 문자열입니다.");
        }
    }
}
