"""
OCR 및 이미지 처리 에이전트
스크린샷에서 텍스트를 추출하고 영역별로 분할하여 정확도 향상
"""

import logging
import io
from typing import List, Dict, Optional, Tuple
from PIL import Image
import pytesseract

logger = logging.getLogger(__name__)


class OCRAgent:
    """
    OCR 기반 텍스트 추출 에이전트
    스크린샷에서 텍스트를 추출하고 영역별로 분할 처리
    """

    def __init__(self, tesseract_path: Optional[str] = None, lang: str = "kor+eng"):
        """
        OCRAgent 초기화

        Args:
            tesseract_path: Tesseract 실행 경로 (Windows의 경우)
            lang: OCR 언어 설정 (기본값: 한글+영어)
        """
        self.lang = lang

        # Tesseract 경로 설정 (Windows)
        if tesseract_path:
            pytesseract.pytesseract.pytesseract_cmd = tesseract_path
        else:
            try:
                # Windows 기본 설치 경로
                pytesseract.pytesseract.pytesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            except:
                logger.warning("Tesseract not found at default Windows path")

    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """
        이미지에서 전체 텍스트 추출

        Args:
            image_bytes: 이미지 바이너리 데이터

        Returns:
            추출된 텍스트
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            text = pytesseract.image_to_string(image, lang=self.lang)
            return text
        except Exception as e:
            logger.error(f"Failed to extract text from image: {e}")
            return ""

    def split_image_vertically(self, image_bytes: bytes, num_sections: int = 2) -> List[bytes]:
        """
        이미지를 수직으로 분할

        Args:
            image_bytes: 이미지 바이너리 데이터
            num_sections: 분할할 섹션 개수

        Returns:
            분할된 이미지 바이너리 리스트
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            width, height = image.size

            # 섹션 높이 계산
            section_height = height // num_sections

            sections = []
            for i in range(num_sections):
                top = i * section_height
                bottom = (i + 1) * section_height if i < num_sections - 1 else height

                # 영역 자르기
                cropped = image.crop((0, top, width, bottom))

                # 바이너리로 변환
                buffer = io.BytesIO()
                cropped.save(buffer, format="PNG")
                sections.append(buffer.getvalue())

            logger.info(f"Image split into {len(sections)} sections")
            return sections

        except Exception as e:
            logger.error(f"Failed to split image: {e}")
            return [image_bytes]

    def extract_text_by_sections(
        self, image_bytes: bytes, num_sections: int = 3
    ) -> Dict[int, str]:
        """
        이미지를 섹션별로 분할하여 텍스트 추출

        Args:
            image_bytes: 이미지 바이너리 데이터
            num_sections: 분할할 섹션 개수

        Returns:
            {섹션번호: 텍스트} 형식의 딕셔너리
        """
        try:
            sections = self.split_image_vertically(image_bytes, num_sections)

            result = {}
            for idx, section_bytes in enumerate(sections):
                logger.info(f"Extracting text from section {idx + 1}/{num_sections}...")
                text = self.extract_text_from_image(section_bytes)
                result[idx + 1] = text
                logger.info(f"Section {idx + 1} extracted: {len(text)} characters")

            return result

        except Exception as e:
            logger.error(f"Failed to extract text by sections: {e}")
            return {}

    def extract_text_with_preprocessing(self, image_bytes: bytes) -> str:
        """
        전처리를 적용하여 텍스트 추출 (해상도 조정, 이진화 등)

        Args:
            image_bytes: 이미지 바이너리 데이터

        Returns:
            추출된 텍스트
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))

            # 이미지 크기 확대 (작은 글씨 해상도 향상)
            # 원본의 2배로 확대
            new_width = image.width * 2
            new_height = image.height * 2
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 대비 향상
            from PIL import ImageEnhance

            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2)

            # 밝기 조정
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)

            # OCR 수행
            text = pytesseract.image_to_string(image, lang=self.lang)

            logger.info(f"Text extracted with preprocessing: {len(text)} characters")
            return text

        except Exception as e:
            logger.error(f"Failed to extract text with preprocessing: {e}")
            return ""

    def crop_region(
        self, image_bytes: bytes, region: Tuple[int, int, int, int]
    ) -> bytes:
        """
        이미지의 특정 영역 자르기

        Args:
            image_bytes: 이미지 바이너리 데이터
            region: (left, top, right, bottom) 좌표

        Returns:
            자른 이미지 바이너리 데이터
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            cropped = image.crop(region)

            buffer = io.BytesIO()
            cropped.save(buffer, format="PNG")
            return buffer.getvalue()

        except Exception as e:
            logger.error(f"Failed to crop region: {e}")
            return image_bytes

    def auto_detect_regions(self, image_bytes: bytes) -> Dict[str, Tuple[int, int, int, int]]:
        """
        이미지에서 텍스트 영역 자동 감지

        Args:
            image_bytes: 이미지 바이너리 데이터

        Returns:
            {영역명: (left, top, right, bottom)} 형식의 딕셔너리
        """
        try:
            import cv2
            import numpy as np

            # 이미지 로드
            image = Image.open(io.BytesIO(image_bytes))
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

            # 이진화
            _, binary = cv2.threshold(cv_image, 150, 255, cv2.THRESH_BINARY)

            # 컨투어 검출
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            regions = {}
            for idx, contour in enumerate(contours):
                x, y, w, h = cv2.boundingRect(contour)

                # 최소 크기 필터링 (노이즈 제거)
                if w > 50 and h > 20:
                    regions[f"region_{idx}"] = (x, y, x + w, y + h)

            logger.info(f"Detected {len(regions)} text regions")
            return regions

        except ImportError:
            logger.warning("OpenCV not installed. Auto-detection disabled.")
            return {}
        except Exception as e:
            logger.error(f"Failed to auto-detect regions: {e}")
            return {}

    def merge_texts(self, text_dict: Dict[int, str], separator: str = "\n\n") -> str:
        """
        여러 섹션의 텍스트를 병합

        Args:
            text_dict: {섹션번호: 텍스트} 형식의 딕셔너리
            separator: 섹션 간 구분자

        Returns:
            병합된 텍스트
        """
        try:
            texts = [text_dict[i] for i in sorted(text_dict.keys())]
            return separator.join(texts)
        except Exception as e:
            logger.error(f"Failed to merge texts: {e}")
            return ""
