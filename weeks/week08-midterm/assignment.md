# Week 08 중간 프로젝트: 캐릭터 로봇 모델링 + 텍스처

## 학습 목표

- [ ] Week 01~07까지의 기법을 종합하여 하나의 완성된 결과물을 제출할 수 있다
- [ ] 모델링과 텍스처가 적용된 로봇/캐릭터의 렌더 이미지를 제작할 수 있다
- [ ] 자신의 제작 과정을 체계적으로 설명할 수 있다

## 과제 내용

Week 01에서 기획한 컨셉을 바탕으로, Week 03~07까지 배운 모델링, Material, UV, 텍스처 기법을 총동원하여 완성된 캐릭터 로봇을 제출합니다.

### 제출물

1. **렌더 이미지 3장 이상** - 서로 다른 각도 (정면, 측면, 3/4 뷰 등)
2. **.blend 파일** - 파일명: `week08_학번_이름.blend`, Pack Resources 완료
3. **프로세스 설명** - 컨셉, 사용한 기법, 어려웠던 점을 간략히 서술 (Discord 메시지)

### 제작 과정

1. **모델링 마무리:** Edit Mode 도구 + Modifier를 활용한 최종 형태 완성
2. **Material 설정:** Principled BSDF로 부위별 재질 할당 (금속, 플라스틱, 발광 등)
3. **UV Unwrap:** Seam 설정 후 Unwrap, UV Editor에서 Island 정리
4. **텍스처 적용:** AI 텍스처, Texture Painting, PBR 라이브러리 등 활용
5. **렌더:** 다양한 각도에서 최소 3장 렌더링
6. **Pack Resources:** File > External Data > Pack Resources 실행
7. **Apply Transform:** Ctrl+A > All Transforms 적용 확인

## 제출 방법

- **제출처:** Discord #midterm-project 채널
- **형식:** 렌더 이미지 3장 + .blend 파일 + 프로세스 설명 (텍스트)
- **기한:** 발표일까지 (수업시간 발표 필수)
- **발표:** 5분 발표 + 2분 Q&A

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| 모델링 완성도 | 30% | 형태 완성도, Topology 품질, Modifier 활용도, Apply Transform 여부 |
| 텍스처/재질 품질 | 25% | Material 구성, UV 품질, 텍스처 매핑 정확도, AI 도구 활용 |
| 창의성/독창성 | 25% | 컨셉의 독창성, 디자인 개성, AI 도구의 창의적 활용 |
| 발표/설명 | 20% | 발표 구성, 과정 설명의 명확성, Q&A 대응 |

> **배점:** 전체 성적의 **35%**

## 제출 전 체크리스트

- [ ] 렌더 이미지가 3장 이상인가
- [ ] 모든 이미지의 해상도가 1920x1080 이상인가
- [ ] .blend 파일명이 `week08_학번_이름.blend` 형식인가
- [ ] Pack Resources (File > External Data > Pack Resources)가 완료되었는가
- [ ] Apply Transform (Ctrl+A > All Transforms)이 적용되었는가
- [ ] Object 이름이 정리되었는가 (Outliner에서 직관적인 이름)
- [ ] UV Unwrap이 수행되었는가
- [ ] Viewport와 Render 모드에서 모두 정상 표시되는가
- [ ] Discord #midterm-project 채널에 모든 파일이 업로드되었는가
- [ ] 프로세스 설명 (컨셉, 기법, 어려웠던 점)이 작성되었는가

## 팁

- 발표 시 Blender Viewport를 직접 보여주면서 설명하면 효과적입니다
- 제작 과정 스크린샷 (비포/애프터)을 미리 준비하면 발표가 수월합니다
- 렌더 이미지의 구도를 다양하게 잡으세요 (정면, 3/4 뷰, 클로즈업 등)
- 시간 관리: 5분을 초과하지 않도록 미리 발표 연습을 해주세요
- 피어 리뷰에 적극 참여하면 가산점이 부여됩니다

## 참고 자료

- [Blender Manual: Rendering](https://docs.blender.org/manual/en/latest/render/index.html)
- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- [Poly Haven](https://polyhaven.com) - 무료 HDRI/텍스처
- [Meshy AI](https://www.meshy.ai) - AI 3D 텍스처 생성
- [나노바나나](https://nanobananas.ai) - Gemini 기반 이미지 생성
