# Week 07 과제: 텍스처 적용 로봇 렌더

## 학습 목표

- [ ] UV Unwrap을 수행하고 UV 전개도를 정리할 수 있다
- [ ] AI 도구 또는 수동으로 텍스처를 제작하고 적용할 수 있다
- [ ] 텍스처가 적용된 로봇/캐릭터의 렌더 이미지를 제출할 수 있다

## 과제 내용

자신의 로봇 또는 캐릭터 모델에 UV Unwrap을 수행하고, AI 텍스처 또는 수동 텍스처를 적용하여 렌더 이미지를 제출한다.

### 제작 과정

1. **Seam 설정:** 로봇/캐릭터 모델에 적절한 Seam 배치
2. **UV Unwrap:** Unwrap 또는 Smart UV Project 등을 활용하여 UV 전개
3. **UV 정리:** UV Editor에서 Island 크기와 위치 정리
4. **텍스처 제작:** 아래 방법 중 하나 이상 활용
   - Meshy AI로 AI 텍스처 생성
   - 나노바나나로 텍스처 패턴 생성
   - Texture Paint로 직접 페인팅
   - Poly Haven에서 PBR 텍스처 다운로드
5. **텍스처 적용:** Shader Editor에서 Image Texture 노드 연결
6. **렌더:** 서로 다른 각도에서 2장 렌더

### 프롬프트 예시 (AI 텍스처 생성 시)

- "seamless robot armor texture, brushed metal, silver gray"
- "cute character skin texture, soft pastel, smooth surface"
- "futuristic circuit board pattern, glowing blue lines, dark background, seamless"

## 제출 방법

- **제출처:** 본인 학생 페이지에 업로드
- **형식:**
  - 렌더 이미지 2장 (서로 다른 각도)
  - UV 전개도 스크린샷 1장
  - 한줄 코멘트
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| UV 작업 품질 | 30% | Seam 배치가 적절한가, UV 왜곡이 적은가 |
| 텍스처 활용 | 40% | 텍스처가 모델에 잘 매핑되었는가, AI 도구를 효과적으로 활용했는가 |
| 완성도 | 30% | 전체적인 마감 품질, 렌더 이미지 구도 |

## 중간고사 안내

다음 주는 중간고사입니다! 이번 과제를 통해 모델링과 텍스처 작업을 마무리하세요.

- **중간고사 범위:** 모델링 + Material + 텍스처 완성본
- **준비물:** 로봇/캐릭터 모델 완성본 (.blend 파일)
- Week 01~07까지 배운 모든 기술을 총합하여 완성도 높은 결과물을 제출할 것

## 참고 자료

- [Blender Manual: UV Editing](https://docs.blender.org/manual/en/latest/editors/uv/index.html)
- [Poly Haven](https://polyhaven.com) - 무료 PBR 텍스처 라이브러리
- [Meshy AI](https://www.meshy.ai) - AI 3D 텍스처 생성
- [나노바나나](https://nanobananas.ai) - Gemini 기반 이미지 생성
