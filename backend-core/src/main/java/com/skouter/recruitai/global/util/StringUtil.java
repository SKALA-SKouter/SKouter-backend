package com.skouter.recruitai.global.util;

/**
 * 문자열 관련 유틸리티 클래스
 */
public class StringUtil {

    /**
     * 문자열이 null 또는 빈 문자열인지 확인
     *
     * @param str 확인할 문자열
     * @return 비어있는지 여부 (true: 빈 문자열, false: 값이 있음)
     */
    public static boolean isEmpty(String str) {
        return str == null || str.trim().isEmpty();
    }

    /**
     * 문자열이 null이 아니고 값이 있는지 확인
     *
     * @param str 확인할 문자열
     * @return 값이 있는지 여부 (true: 값이 있음, false: 빈 문자열)
     */
    public static boolean isNotEmpty(String str) {
        return !isEmpty(str);
    }

    /**
     * 문자열을 지정된 길이로 자름
     *
     * @param str 대상 문자열
     * @param maxLength 최대 길이
     * @return 자른 문자열
     */
    public static String truncate(String str, int maxLength) {
        if (isEmpty(str)) {
            return str;
        }
        if (str.length() <= maxLength) {
            return str;
        }
        return str.substring(0, maxLength);
    }

    /**
     * 문자열의 앞뒤 공백 제거
     *
     * @param str 대상 문자열
     * @return 공백이 제거된 문자열
     */
    public static String trim(String str) {
        return str == null ? null : str.trim();
    }

    /**
     * 문자열이 특정 문자열로 시작하는지 확인 (대소문자 무시)
     *
     * @param str 대상 문자열
     * @param prefix 접두사
     * @return 시작 여부
     */
    public static boolean startsWithIgnoreCase(String str, String prefix) {
        if (str == null || prefix == null) {
            return false;
        }
        return str.toLowerCase().startsWith(prefix.toLowerCase());
    }

    /**
     * 문자열이 특정 문자열로 끝나는지 확인 (대소문자 무시)
     *
     * @param str 대상 문자열
     * @param suffix 접미사
     * @return 종료 여부
     */
    public static boolean endsWithIgnoreCase(String str, String suffix) {
        if (str == null || suffix == null) {
            return false;
        }
        return str.toLowerCase().endsWith(suffix.toLowerCase());
    }

    /**
     * 문자열에서 특수문자 제거
     *
     * @param str 대상 문자열
     * @return 특수문자가 제거된 문자열
     */
    public static String removeSpecialCharacters(String str) {
        if (isEmpty(str)) {
            return str;
        }
        return str.replaceAll("[^a-zA-Z0-9\\s]", "");
    }

    /**
     * 문자열에서 숫자만 추출
     *
     * @param str 대상 문자열
     * @return 숫자만 포함된 문자열
     */
    public static String extractNumbers(String str) {
        if (isEmpty(str)) {
            return "";
        }
        return str.replaceAll("[^0-9]", "");
    }

    /**
     * 캐멜 케이스를 스네이크 케이스로 변환
     *
     * @param camelCase 캐멜 케이스 문자열
     * @return 스네이크 케이스 문자열
     */
    public static String camelToSnakeCase(String camelCase) {
        if (isEmpty(camelCase)) {
            return camelCase;
        }
        return camelCase
                .replaceAll("([a-z])([A-Z]+)", "$1_$2")
                .toLowerCase();
    }

    /**
     * 스네이크 케이스를 캐멜 케이스로 변환
     *
     * @param snakeCase 스네이크 케이스 문자열
     * @return 캐멜 케이스 문자열
     */
    public static String snakeToCamelCase(String snakeCase) {
        if (isEmpty(snakeCase)) {
            return snakeCase;
        }
        String[] parts = snakeCase.split("_");
        StringBuilder result = new StringBuilder(parts[0].toLowerCase());

        for (int i = 1; i < parts.length; i++) {
            result.append(parts[i].substring(0, 1).toUpperCase())
                    .append(parts[i].substring(1).toLowerCase());
        }
        return result.toString();
    }
}
