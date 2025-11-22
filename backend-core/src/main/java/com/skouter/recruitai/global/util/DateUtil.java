package com.skouter.recruitai.global.util;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

/**
 * 날짜/시간 관련 유틸리티 클래스
 */
public class DateUtil {

    private static final DateTimeFormatter DATE_TIME_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final DateTimeFormatter DATE_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    /**
     * 현재 시간 반환
     *
     * @return 현재 LocalDateTime
     */
    public static LocalDateTime now() {
        return LocalDateTime.now();
    }

    /**
     * LocalDateTime을 문자열로 변환 (기본 포맷: yyyy-MM-dd HH:mm:ss)
     *
     * @param dateTime LocalDateTime
     * @return 포맷된 문자열
     */
    public static String format(LocalDateTime dateTime) {
        return dateTime.format(DATE_TIME_FORMATTER);
    }

    /**
     * LocalDateTime을 지정된 포맷으로 변환
     *
     * @param dateTime LocalDateTime
     * @param pattern 포맷 패턴
     * @return 포맷된 문자열
     */
    public static String format(LocalDateTime dateTime, String pattern) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(pattern);
        return dateTime.format(formatter);
    }

    /**
     * 문자열을 LocalDateTime으로 파싱 (기본 포맷: yyyy-MM-dd HH:mm:ss)
     *
     * @param dateTimeString 날짜 문자열
     * @return LocalDateTime
     */
    public static LocalDateTime parse(String dateTimeString) {
        return LocalDateTime.parse(dateTimeString, DATE_TIME_FORMATTER);
    }

    /**
     * 문자열을 지정된 포맷으로 LocalDateTime으로 파싱
     *
     * @param dateTimeString 날짜 문자열
     * @param pattern 포맷 패턴
     * @return LocalDateTime
     */
    public static LocalDateTime parse(String dateTimeString, String pattern) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(pattern);
        return LocalDateTime.parse(dateTimeString, formatter);
    }

    /**
     * 두 시간 사이의 일수 계산
     *
     * @param start 시작 시간
     * @param end 종료 시간
     * @return 일수
     */
    public static long daysBetween(LocalDateTime start, LocalDateTime end) {
        return ChronoUnit.DAYS.between(start, end);
    }

    /**
     * 두 시간 사이의 시간 수 계산
     *
     * @param start 시작 시간
     * @param end 종료 시간
     * @return 시간 수
     */
    public static long hoursBetween(LocalDateTime start, LocalDateTime end) {
        return ChronoUnit.HOURS.between(start, end);
    }

    /**
     * 특정 날짜가 과거인지 확인
     *
     * @param dateTime 확인할 시간
     * @return 과거 여부 (true: 과거, false: 미래 또는 현재)
     */
    public static boolean isPast(LocalDateTime dateTime) {
        return dateTime.isBefore(LocalDateTime.now());
    }

    /**
     * 특정 날짜가 미래인지 확인
     *
     * @param dateTime 확인할 시간
     * @return 미래 여부 (true: 미래, false: 과거 또는 현재)
     */
    public static boolean isFuture(LocalDateTime dateTime) {
        return dateTime.isAfter(LocalDateTime.now());
    }
}
