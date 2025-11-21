#!/usr/bin/env python3
"""
통합 채용공고 크롤링 시스템 메인 스크립트

사용법:
    python main.py --company Coupang
    python main.py --all
    python main.py --company Naver --output results.json
"""

import argparse
import logging
import json
from datetime import datetime
from pathlib import Path

from crawlers import (
    CrawlerRegistry,
    CoupangCrawler,
    NaverCrawler,
    KakaoCrawler,
    WoowahanCrawler,
)
from agents import PDFCaptureAgent, StorageAgent
from orchestrator import IntegratedCrawlerOrchestrator

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawler.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def setup_registry() -> CrawlerRegistry:
    """크롤러 레지스트리 설정 및 크롤러 등록"""
    registry = CrawlerRegistry()

    # 크롤러 등록
    crawlers = [
        CoupangCrawler(),
        NaverCrawler(),
        KakaoCrawler(),
        WoowahanCrawler(),
    ]

    for crawler in crawlers:
        registry.register(crawler)

    return registry


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(
        description="통합 채용공고 크롤링 시스템",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python main.py --company Coupang
    python main.py --all
    python main.py --company Naver --output results.json
    python main.py --list
        """,
    )

    parser.add_argument(
        "--company",
        type=str,
        help="특정 회사 크롤링 (예: Coupang, Naver, Kakao)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="등록된 모든 회사 크롤링",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="등록된 크롤러 목록 출력",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="results.json",
        help="결과 저장 파일 경로 (기본값: results.json)",
    )
    parser.add_argument(
        "--pdf-dir",
        type=str,
        default="./data/pdfs",
        help="PDF 저장 디렉토리 (기본값: ./data/pdfs)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Selenium 헤드리스 모드 (기본값: True)",
    )
    parser.add_argument(
        "--no-headless",
        action="store_false",
        dest="headless",
        help="Selenium 헤드리스 모드 비활성화",
    )

    args = parser.parse_args()

    # 레지스트리 설정
    logger.info("Setting up crawler registry...")
    registry = setup_registry()

    # --list 옵션
    if args.list:
        print("\n=== Registered Crawlers ===")
        for company in registry.list_companies():
            print(f"  ✓ {company}")
        print()
        return

    # --company 또는 --all 옵션 필수
    if not args.company and not args.all:
        parser.print_help()
        print("\nError: --company or --all is required")
        return

    # 에이전트 초기화
    logger.info("Initializing agents...")
    pdf_capture_agent = PDFCaptureAgent(headless=args.headless)
    storage_agent = StorageAgent(local_base_path=args.pdf_dir)

    # 오케스트레이터 생성
    orchestrator = IntegratedCrawlerOrchestrator(
        registry=registry,
        storage_agent=storage_agent,
        pdf_capture_agent=pdf_capture_agent,
    )

    # 크롤링 실행
    logger.info("Starting crawl...")
    print("\n" + "=" * 60)

    if args.company:
        # 특정 회사 크롤링
        if not registry.is_registered(args.company):
            print(f"Error: Crawler for '{args.company}' not found")
            print(f"Available: {', '.join(registry.list_companies())}")
            return

        print(f"Crawling {args.company}...")
        results = orchestrator.run_company(args.company)

    else:
        # 모든 회사 크롤링
        print("Crawling all registered companies...")
        results = orchestrator.run_all_companies()

    # 결과 출력
    print("\n" + "=" * 60)
    print("CRAWL RESULTS")
    print("=" * 60)

    if isinstance(results, dict) and "success" in results:
        # 단일 회사 결과
        if results["success"]:
            print(f"\n✓ {results['company_name']}")
            print(f"  Total Jobs: {results.get('total_jobs', 0)}")
            print(f"  PDFs Captured: {results.get('pdfs_captured', 0)}")
            print(f"  PDFs Stored: {results.get('pdfs_stored', 0)}")

            if results.get("error_logs"):
                print(f"  Errors: {len(results['error_logs'])}")
                for error in results["error_logs"][:5]:
                    print(f"    - {error}")
        else:
            print(f"\n✗ {results.get('company_name', 'Unknown')}")
            print(f"  Error: {results.get('error', 'Unknown error')}")

    else:
        # 다중 회사 결과
        total_jobs = 0
        total_pdfs = 0
        total_errors = 0

        for company, result in results.items():
            if result["success"]:
                jobs = result.get("total_jobs", 0)
                pdfs = result.get("pdfs_stored", 0)
                errors = len(result.get("error_logs", []))

                print(f"\n✓ {company}")
                print(f"  Total Jobs: {jobs}")
                print(f"  PDFs Stored: {pdfs}")
                if errors:
                    print(f"  Errors: {errors}")

                total_jobs += jobs
                total_pdfs += pdfs
                total_errors += errors
            else:
                print(f"\n✗ {company}")
                print(f"  Error: {result.get('error', 'Unknown error')}")

        print("\n" + "-" * 60)
        print("SUMMARY")
        print("-" * 60)
        print(f"Total Jobs: {total_jobs}")
        print(f"Total PDFs Stored: {total_pdfs}")
        print(f"Total Errors: {total_errors}")

    # 결과 JSON 저장
    print(f"\nSaving results to {args.output}...")
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"✓ Results saved to {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
