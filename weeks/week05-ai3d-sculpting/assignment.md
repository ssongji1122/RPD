# Week 05 과제: AI 3D + Sculpt 수정

## 학습 목표

- [ ] AI 3D 생성 도구를 사용하여 3D 모델을 생성할 수 있다
- [ ] 생성된 AI 모델을 Blender에 임포트하고 기본 설정을 할 수 있다
- [ ] Sculpt Mode의 브러시를 사용하여 AI 모델의 형태를 수정할 수 있다

## 과제 내용

AI 도구로 3D 모델을 생성한 후, Blender의 Sculpt Mode를 사용하여 형태를 수정한다.

### 제작 과정

1. **AI 3D 모델 생성**
   - Meshy AI (Text to 3D) 또는 Tripo AI (Image to 3D) 사용
   - 자신의 로봇/캐릭터 컨셉에 맞는 프롬프트 작성
   - 생성된 모델을 GLB/FBX 형식으로 다운로드

2. **Blender 임포트**
   - File > Import > glTF 2.0으로 임포트
   - 스케일 조정 (S 키)
   - Origin 설정 (Set Origin > Origin to Geometry)
   - Apply All Transforms (Ctrl+A)

3. **Before 스크린샷 촬영**
   - AI 생성 직후의 원본 상태를 촬영

4. **Sculpt Mode 수정**
   - Smooth 브러시로 거친 표면 정리
   - Grab 브러시로 형태 조정
   - Draw/Clay Strips로 디테일 추가
   - 필요시 Mask로 영역 보호

5. **After 스크린샷 촬영**
   - Sculpt 수정 완료 후 동일한 각도에서 촬영

### 프롬프트 예시

**Meshy AI (Text to 3D)**
- "cute companion robot, spherical head, stubby arms, matte finish"
- "small delivery robot, box-shaped body, wheel base, friendly face"
- "retro toy robot, boxy design, antenna, vintage style"

**Tripo AI (Image to 3D)**
- Week 01에서 만든 캐릭터 컨셉 이미지 활용
- 배경이 단순하고 정면 뷰인 이미지 권장

## 제출 방법

- **제출처:** Discord #week05-assignment 채널
- **형식:**
  - 이미지 2장 (Before: AI 원본 / After: Sculpt 수정 후)
    - 동일한 각도에서 비교가 가능하도록 촬영
  - 사용한 AI 도구 이름 (Meshy 또는 Tripo)
  - 한줄 코멘트 (AI 모델의 한계점과 수정 과정에서 느낀 점)
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| AI 도구 활용 | 30% | 적절한 프롬프트 작성, 도구의 효과적 사용 |
| Sculpt 수정 품질 | 40% | 표면 정리, 형태 개선, 디테일 추가 정도 |
| 창의성 | 30% | 독창적인 컨셉, AI 한계를 넘어선 수정 시도 |

## 참고 자료

- [AI 도구 가이드](../../resources/ai-tools-guide.md)
- [Blender 단축키 모음](../../resources/blender-shortcuts.md)
- [Meshy AI](https://meshy.ai)
- [Tripo AI](https://tripo3d.ai)
