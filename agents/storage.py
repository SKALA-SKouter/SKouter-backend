import os
import logging
from typing import Optional
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class StorageAgent:
    """
    이미지 파일 저장을 담당하는 Agent
    로컬 저장소와 S3 저장소를 지원
    """

    def __init__(self, local_base_path: str = "./data/screenshots", s3_config: Optional[dict] = None):
        """
        StorageAgent 초기화

        Args:
            local_base_path: 로컬 저장 경로
            s3_config: S3 설정 정보 {bucket, region, access_key, secret_key}
        """
        self.local_base_path = Path(local_base_path)
        self.s3_config = s3_config
        self.s3_client = None

        # 로컬 경로 생성
        self.local_base_path.mkdir(parents=True, exist_ok=True)

        # S3 클라이언트 초기화
        if s3_config:
            self._initialize_s3()

    def _initialize_s3(self) -> None:
        """S3 클라이언트 초기화"""
        try:
            import boto3
            self.s3_client = boto3.client(
                "s3",
                region_name=self.s3_config.get("region", "us-east-1"),
                aws_access_key_id=self.s3_config.get("access_key"),
                aws_secret_access_key=self.s3_config.get("secret_key"),
            )
            logger.info("S3 client initialized successfully")
        except ImportError:
            logger.warning("boto3 not installed. S3 storage will be disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {e}")

    def save_pdf_locally(
        self,
        pdf_bytes: bytes,
        company: str,
        job_id: str,
        job_title: str = "",
        subfolder: str = ""
    ) -> Optional[str]:
        """
        PDF를 로컬 저장소에 저장

        Args:
            pdf_bytes: PDF 바이너리 데이터
            company: 회사명
            job_id: 공고 ID
            job_title: 공고 제목 (파일명에 포함)
            subfolder: 추가 서브폴더

        Returns:
            저장된 파일 경로 또는 None (실패 시)
        """
        try:
            # 디렉토리 구조 생성: base_path/company/subfolder
            company_path = self.local_base_path / company
            if subfolder:
                company_path = company_path / subfolder
            company_path.mkdir(parents=True, exist_ok=True)

            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in job_title)[:30]
            safe_title = safe_title.rstrip('_')

            filename = f"{job_id}_{safe_title}_{timestamp}.pdf" if safe_title else f"{job_id}_{timestamp}.pdf"
            file_path = company_path / filename

            # PDF 저장
            with open(file_path, "wb") as f:
                f.write(pdf_bytes)

            logger.info(f"PDF saved locally: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Failed to save PDF locally: {e}")
            return None

    def save_pdf_to_s3(
        self,
        pdf_bytes: bytes,
        company: str,
        job_id: str,
        job_title: str = "",
        subfolder: str = ""
    ) -> Optional[str]:
        """
        PDF를 S3에 저장

        Args:
            pdf_bytes: PDF 바이너리 데이터
            company: 회사명
            job_id: 공고 ID
            job_title: 공고 제목
            subfolder: 추가 서브폴더

        Returns:
            S3 객체 키 또는 None (실패 시)
        """
        if not self.s3_client:
            logger.warning("S3 client not available. Skipping S3 storage.")
            return None

        try:
            # S3 키 생성: company/subfolder/job_id_title_timestamp.pdf
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in job_title)[:30]
            safe_title = safe_title.rstrip('_')

            filename = f"{job_id}_{safe_title}_{timestamp}.pdf" if safe_title else f"{job_id}_{timestamp}.pdf"

            s3_key = f"{company}"
            if subfolder:
                s3_key += f"/{subfolder}"
            s3_key += f"/{filename}"

            # S3에 업로드
            bucket = self.s3_config.get("bucket")
            self.s3_client.put_object(
                Bucket=bucket,
                Key=s3_key,
                Body=pdf_bytes,
                ContentType="application/pdf",
                Metadata={
                    "company": company,
                    "job_id": job_id,
                    "job_title": job_title,
                    "timestamp": timestamp,
                }
            )

            logger.info(f"PDF saved to S3: s3://{bucket}/{s3_key}")
            return s3_key

        except Exception as e:
            logger.error(f"Failed to save PDF to S3: {e}")
            return None

    def save_pdf(
        self,
        pdf_bytes: bytes,
        company: str,
        job_id: str,
        job_title: str = "",
        subfolder: str = "",
        save_to_s3: bool = False
    ) -> dict:
        """
        PDF를 저장 (로컬 + S3 선택 가능)

        Args:
            pdf_bytes: PDF 바이너리 데이터
            company: 회사명
            job_id: 공고 ID
            job_title: 공고 제목
            subfolder: 추가 서브폴더
            save_to_s3: S3 저장 여부

        Returns:
            {
                'local_path': '...' or None,
                's3_key': '...' or None,
                'success': True/False
            }
        """
        local_path = self.save_pdf_locally(pdf_bytes, company, job_id, job_title, subfolder)
        s3_key = None

        if save_to_s3:
            s3_key = self.save_pdf_to_s3(pdf_bytes, company, job_id, job_title, subfolder)

        success = local_path is not None or s3_key is not None

        return {
            "local_path": local_path,
            "s3_key": s3_key,
            "success": success
        }

    def save_image_locally(
        self,
        image_bytes: bytes,
        company: str,
        job_id: str,
        job_title: str = "",
        subfolder: str = "",
        image_format: str = "png"
    ) -> Optional[str]:
        """
        이미지를 로컬 저장소에 저장

        Args:
            image_bytes: 이미지 바이너리 데이터
            company: 회사명
            job_id: 공고 ID
            job_title: 공고 제목 (파일명에 포함)
            subfolder: 추가 서브폴더
            image_format: 이미지 포맷 ('png' 또는 'jpeg')

        Returns:
            저장된 파일 경로 또는 None (실패 시)
        """
        try:
            # 디렉토리 구조 생성: base_path/company/subfolder
            company_path = self.local_base_path / company
            if subfolder:
                company_path = company_path / subfolder
            company_path.mkdir(parents=True, exist_ok=True)

            # 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in job_title)[:30]
            safe_title = safe_title.rstrip('_')

            # 파일 확장자 결정
            ext = "jpeg" if image_format.lower() == "jpeg" else "png"
            filename = f"{job_id}_{safe_title}_{timestamp}.{ext}" if safe_title else f"{job_id}_{timestamp}.{ext}"
            file_path = company_path / filename

            # 이미지 저장
            with open(file_path, "wb") as f:
                f.write(image_bytes)

            logger.info(f"Image saved locally: {file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"Failed to save image locally: {e}")
            return None

    def save_image_to_s3(
        self,
        image_bytes: bytes,
        company: str,
        job_id: str,
        job_title: str = "",
        subfolder: str = "",
        image_format: str = "png"
    ) -> Optional[str]:
        """
        이미지를 S3에 저장

        Args:
            image_bytes: 이미지 바이너리 데이터
            company: 회사명
            job_id: 공고 ID
            job_title: 공고 제목
            subfolder: 추가 서브폴더
            image_format: 이미지 포맷 ('png' 또는 'jpeg')

        Returns:
            S3 객체 키 또는 None (실패 시)
        """
        if not self.s3_client:
            logger.warning("S3 client not available. Skipping S3 storage.")
            return None

        try:
            # S3 키 생성: company/subfolder/job_id_title_timestamp.ext
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in job_title)[:30]
            safe_title = safe_title.rstrip('_')

            # 파일 확장자 결정
            ext = "jpeg" if image_format.lower() == "jpeg" else "png"
            filename = f"{job_id}_{safe_title}_{timestamp}.{ext}" if safe_title else f"{job_id}_{timestamp}.{ext}"

            s3_key = f"{company}"
            if subfolder:
                s3_key += f"/{subfolder}"
            s3_key += f"/{filename}"

            # Content-Type 결정
            content_type = "image/jpeg" if image_format.lower() == "jpeg" else "image/png"

            # S3에 업로드
            bucket = self.s3_config.get("bucket")
            self.s3_client.put_object(
                Bucket=bucket,
                Key=s3_key,
                Body=image_bytes,
                ContentType=content_type,
                Metadata={
                    "company": company,
                    "job_id": job_id,
                    "job_title": job_title,
                    "timestamp": timestamp,
                    "format": image_format,
                }
            )

            logger.info(f"Image saved to S3: s3://{bucket}/{s3_key}")
            return s3_key

        except Exception as e:
            logger.error(f"Failed to save image to S3: {e}")
            return None

    def save_image(
        self,
        image_bytes: bytes,
        company: str,
        job_id: str,
        job_title: str = "",
        subfolder: str = "",
        image_format: str = "png",
        save_to_s3: bool = False
    ) -> dict:
        """
        이미지를 저장 (로컬 + S3 선택 가능)

        Args:
            image_bytes: 이미지 바이너리 데이터
            company: 회사명
            job_id: 공고 ID
            job_title: 공고 제목
            subfolder: 추가 서브폴더
            image_format: 이미지 포맷 ('png' 또는 'jpeg')
            save_to_s3: S3 저장 여부

        Returns:
            {
                'local_path': '...' or None,
                's3_key': '...' or None,
                'success': True/False
            }
        """
        local_path = self.save_image_locally(image_bytes, company, job_id, job_title, subfolder, image_format)
        s3_key = None

        if save_to_s3:
            s3_key = self.save_image_to_s3(image_bytes, company, job_id, job_title, subfolder, image_format)

        success = local_path is not None or s3_key is not None

        return {
            "local_path": local_path,
            "s3_key": s3_key,
            "success": success
        }

    def get_file_size(self, file_path: str) -> int:
        """로컬 파일 크기 반환"""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            logger.error(f"Failed to get file size: {e}")
            return 0

    def delete_local_file(self, file_path: str) -> bool:
        """로컬 파일 삭제"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted local file: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False

    def delete_s3_file(self, s3_key: str) -> bool:
        """S3 파일 삭제"""
        if not self.s3_client:
            logger.warning("S3 client not available.")
            return False

        try:
            bucket = self.s3_config.get("bucket")
            self.s3_client.delete_object(Bucket=bucket, Key=s3_key)
            logger.info(f"Deleted S3 file: {s3_key}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete S3 file: {e}")
            return False
