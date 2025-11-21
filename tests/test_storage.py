"""
StorageAgent 테스트
"""

import pytest
import tempfile
from pathlib import Path
from agents import StorageAgent


class TestStorageAgent:
    """StorageAgent 테스트"""

    @pytest.fixture
    def temp_dir(self):
        """임시 디렉토리 생성"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    def test_initialization(self, temp_dir):
        """StorageAgent 초기화"""
        agent = StorageAgent(local_base_path=temp_dir)
        assert agent.local_base_path == Path(temp_dir)

    def test_save_pdf_locally(self, temp_dir):
        """PDF 로컬 저장"""
        agent = StorageAgent(local_base_path=temp_dir)

        pdf_bytes = b"%PDF-1.4\nTest PDF content"
        result = agent.save_pdf_locally(
            pdf_bytes=pdf_bytes,
            company="TestCompany",
            job_id="job_001",
            job_title="Test Job"
        )

        assert result is not None
        assert Path(result).exists()
        assert "TestCompany" in result

    def test_save_pdf_locally_with_subfolder(self, temp_dir):
        """PDF 로컬 저장 (서브폴더)"""
        agent = StorageAgent(local_base_path=temp_dir)

        pdf_bytes = b"%PDF-1.4\nTest PDF content"
        result = agent.save_pdf_locally(
            pdf_bytes=pdf_bytes,
            company="TestCompany",
            job_id="job_001",
            job_title="Test Job",
            subfolder="2024-01-15"
        )

        assert result is not None
        assert "2024-01-15" in result

    def test_get_file_size(self, temp_dir):
        """파일 크기 조회"""
        agent = StorageAgent(local_base_path=temp_dir)

        pdf_bytes = b"%PDF-1.4\nTest PDF content"
        file_path = agent.save_pdf_locally(
            pdf_bytes=pdf_bytes,
            company="TestCompany",
            job_id="job_001"
        )

        size = agent.get_file_size(file_path)
        assert size == len(pdf_bytes)

    def test_delete_local_file(self, temp_dir):
        """로컬 파일 삭제"""
        agent = StorageAgent(local_base_path=temp_dir)

        pdf_bytes = b"%PDF-1.4\nTest PDF content"
        file_path = agent.save_pdf_locally(
            pdf_bytes=pdf_bytes,
            company="TestCompany",
            job_id="job_001"
        )

        assert Path(file_path).exists()

        success = agent.delete_local_file(file_path)
        assert success
        assert not Path(file_path).exists()

    def test_delete_nonexistent_file(self, temp_dir):
        """존재하지 않는 파일 삭제"""
        agent = StorageAgent(local_base_path=temp_dir)
        success = agent.delete_local_file("/nonexistent/file.pdf")
        assert not success

    def test_save_pdf_with_empty_title(self, temp_dir):
        """제목 없이 PDF 저장"""
        agent = StorageAgent(local_base_path=temp_dir)

        pdf_bytes = b"%PDF-1.4\nTest PDF content"
        result = agent.save_pdf_locally(
            pdf_bytes=pdf_bytes,
            company="TestCompany",
            job_id="job_001",
            job_title=""
        )

        assert result is not None
        assert Path(result).exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
