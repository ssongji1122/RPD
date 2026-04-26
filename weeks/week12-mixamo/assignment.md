# Week 12 과제: Mixamo 리깅/애니메이션 적용

## 학습 목표

- [ ] Mixamo에 자신의 모델을 업로드하고 자동 리깅을 수행할 수 있다
- [ ] Mixamo 애니메이션 라이브러리에서 적절한 애니메이션을 선택하고 적용할 수 있다
- [ ] FBX 파일을 Blender로 임포트하여 애니메이션을 재생할 수 있다
- [ ] NLA Editor를 활용하여 여러 애니메이션을 이어 붙일 수 있다

## 과제 내용

자신의 로봇 또는 캐릭터 모델에 Mixamo 자동 리깅을 적용하고, 2가지 이상의 서로 다른 애니메이션을 적용하여 제출한다.

### 제작 과정

1. **모델 준비:**
   - T-Pose 확인 (팔을 양옆으로 벌린 자세)
   - 여러 파츠가 있으면 Ctrl+J로 합치기
   - 기존 Armature 삭제
   - Ctrl+A > All Transforms 적용
2. **FBX 내보내기:** File > Export > FBX (Apply Modifiers 체크)
3. **Mixamo 업로드:** mixamo.com > Upload Character > FBX 업로드
4. **마커 배치:** Chin, Wrists, Elbows, Knees, Groin 위치에 마커 배치
5. **자동 리깅 확인:** 프리뷰에서 리깅 결과 확인
6. **애니메이션 선택:** 최소 2가지 서로 다른 애니메이션 적용 및 다운로드
7. **Blender 임포트:** File > Import > FBX
8. **NLA Editor 편집:** 두 애니메이션을 NLA Strip으로 이어 붙이기
9. **결과물 캡처:** 애니메이션 GIF 또는 영상으로 녹화

### 애니메이션 조합 아이디어 (참고)

- 걷기 + 인사: 걸어오다가 인사하는 장면
- 대기 + 춤추기: 가만히 있다가 춤을 추기 시작
- 뛰기 + 점프: 달리다가 점프하는 장면
- 인사 + 앉기: 인사한 후 앉는 장면

### Mixamo 자동 리깅이 실패하는 경우

만약 자신의 모델이 Mixamo에서 리깅이 잘 되지 않는 경우:
- Mixamo에서 제공하는 기본 캐릭터(X Bot, Y Bot 등)를 사용해도 됨
- 모델을 수정하여 다시 시도 (사지 분리, Mesh 정리)
- 과제 제출 시 어떤 문제가 있었는지 코멘트에 기록

### GIF/영상 녹화 방법

**방법 A: Viewport 녹화 (간편)**
- View > Viewport Render Animation (Ctrl+F12 대신 Viewport 렌더)
- Output Properties에서 파일 경로, 프레임 범위, 포맷(FFmpeg Video) 설정
- 또는 화면 녹화 프로그램(OBS 등) 사용

**방법 B: GIF 변환**
- 렌더된 이미지 시퀀스를 온라인 변환 도구로 GIF 변환
- 또는 FFmpeg, ezgif.com 등 활용

## 제출 방법

- **제출처:** 본인 학생 페이지
- **형식:**
  - 애니메이션 GIF 또는 영상 2개 (서로 다른 애니메이션)
  - Mixamo 자동 리깅 화면 스크린샷 1장 (마커 배치 또는 리깅 결과)
  - 한줄 코멘트 (사용한 애니메이션 이름 + 소감)
- **기한:** 다음 수업 전까지

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| Mixamo 리깅 성공 | 30% | 자동 리깅이 올바르게 적용되었는가, 마커 배치가 적절한가, 메쉬가 자연스럽게 변형되는가 |
| 애니메이션 선택/적용 | 35% | 2가지 이상의 서로 다른 애니메이션인가, 로봇/캐릭터에 어울리는 선택인가, 설정(Speed, Trim 등)을 적절히 조정했는가 |
| NLA 편집 | 35% | NLA Editor에서 여러 애니메이션을 이어 붙였는가, Blend In/Out으로 전환이 부드러운가, 전체 흐름이 자연스러운가 |

## 참고 자료

- [Mixamo](https://www.mixamo.com) - Adobe 자동 리깅 및 애니메이션
- [Blender Manual: NLA Editor](https://docs.blender.org/manual/en/latest/editors/nla/index.html)
- [Blender Manual: FBX Import/Export](https://docs.blender.org/manual/en/latest/files/import_export/fbx.html)
- [ezgif.com](https://ezgif.com) - 온라인 GIF 변환 도구
