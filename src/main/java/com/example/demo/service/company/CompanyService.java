package com.example.demo.service.company;

import com.example.demo.repository.CompanyRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * 회사 관련 비즈니스 로직
 */
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class CompanyService {

    private final CompanyRepository companyRepository;

    // TODO: 회사 조회, 관리 메서드 구현
}
