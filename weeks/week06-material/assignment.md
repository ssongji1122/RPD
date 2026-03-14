# Week 06 과제: 로봇/캐릭터 재질 적용

## 학습 목표

- [ ] 3가지 이상의 서로 다른 Material을 만들어 적용할 수 있다
- [ ] Principled BSDF 파라미터를 조절하여 원하는 재질을 표현할 수 있다
- [ ] Material Preview 또는 Rendered 모드에서 결과를 확인하고 렌더할 수 있다

## 과제 내용

자신의 로봇 또는 캐릭터 모델에 3가지 이상의 서로 다른 재질을 적용하고 렌더 이미지를 제출한다.

### 재질 예시

- 금속 (Metallic=1, Roughness 조절)
- 매트 플라스틱 (Metallic=0, Roughness=0.8)
- 광택 플라스틱 (Metallic=0, Roughness=0.1)
- 투명 유리 (Transmission=1, IOR=1.5)
- 자체 발광 (Emission Color + Strength)
- Thin Film Iridescence (Blender 5.0 신기능, 선택 사항)

### 제작 과정

1. 로봇/캐릭터 모델에 부위별 Material 계획 수립
2. Material 슬롯에 여러 Material 생성
3. Edit Mode에서 Face 선택 후 각 Material Assign
4. 파라미터 조절로 원하는 재질감 표현
5. Material Preview 또는 Rendered 모드에서 확인
6. 렌더 이미지 저장

## 제출 방법

- **제출처:** Discord #week06-assignment 채널
- **형식:** 렌더 이미지 1~2장 + 사용한 재질 종류 설명 + 한줄 코멘트
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| Material 활용 다양성 | 40% | 3가지 이상 서로 다른 재질 사용, 재질 간 차이가 명확한가 |
| 완성도 | 30% | Material 할당이 정확한가, 파라미터 조절이 적절한가 |
| 창의성 | 30% | 재질 조합이 캐릭터/로봇의 컨셉과 어울리는가 |

## 참고 자료

- [Poly Haven](https://polyhaven.com) - 무료 PBR 텍스처 라이브러리
- [Blender Manual: Materials](https://docs.blender.org/manual/en/latest/render/materials/index.html)
- [Blender Manual: Shader Nodes](https://docs.blender.org/manual/en/latest/render/shader_nodes/index.html)
