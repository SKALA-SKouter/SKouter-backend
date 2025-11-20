package com.example.demo.repository;

import com.example.demo.entity.Company;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 회사 데이터 접근
 */
@Repository
public interface CompanyRepository extends JpaRepository<Company, Long> {
}
