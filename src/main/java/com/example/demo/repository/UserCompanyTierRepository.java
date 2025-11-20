package com.example.demo.repository;

import com.example.demo.entity.UserCompanyTier;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

/**
 * 사용자-회사 티어 데이터 접근
 */
@Repository
public interface UserCompanyTierRepository extends JpaRepository<UserCompanyTier, Long> {
}
