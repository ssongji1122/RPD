# Week 13 과제: 렌더링 + AI 영상/사운드 테스트

## 학습 목표

- [ ] Eevee와 Cycles 렌더 엔진으로 각각 렌더링할 수 있다
- [ ] AI 영상 생성 도구(Kling AI)를 활용하여 프로모션 영상을 만들 수 있다
- [ ] AI 음악 생성 도구(Suno AI / ElevenLabs)를 활용하여 BGM을 제작할 수 있다
- [ ] 적절한 영문 프롬프트를 작성할 수 있다

## 과제 내용

자신의 로봇 또는 캐릭터 모델을 2가지 렌더 엔진(Eevee / Cycles)으로 렌더링하고, AI 도구를 활용하여 프로모션 영상과 BGM을 제작합니다.

### 1. 렌더링 (Eevee + Cycles)

1. **Camera 설정:** 로봇/캐릭터를 가장 잘 보여주는 앵글로 Camera 배치
   - Focal Length: 50mm 권장 (클로즈업은 85mm)
   - Depth of Field 활용 추천 (선택 사항)
2. **Eevee 렌더:** Eevee 엔진으로 렌더링하여 PNG로 저장
   - Bloom, AO 등 Eevee 전용 설정 활용
   - 해상도: 1920x1080 이상
3. **Cycles 렌더:** 같은 Camera 앵글에서 Cycles 엔진으로 렌더링하여 PNG로 저장
   - Denoising 활성화 권장
   - Samples: 128 이상

### 2. AI 영상 생성 (Kling AI)

1. 렌더 이미지 중 마음에 드는 1장을 선택
2. **Kling AI (klingai.com)** > Image to Video에 업로드
3. 영문 프롬프트를 작성하여 비디오 생성
4. 생성된 영상 다운로드

**프롬프트 작성 가이드:**
- 로봇의 움직임 묘사: "slowly turning", "waving", "eyes lighting up"
- 카메라 움직임: "camera orbiting", "slowly zooming in", "dolly shot"
- 분위기: "studio lighting", "cinematic", "soft shadows"

### 3. AI BGM 생성 (Suno AI 또는 ElevenLabs)

1. **Suno AI (suno.com)** 또는 **ElevenLabs (elevenlabs.io)** 접속
2. 프로모션 영상에 어울리는 BGM 프롬프트 작성
3. 30초 이상의 음악 생성 후 다운로드

**프롬프트 작성 가이드:**
- 장르: electronic, ambient, cinematic, lo-fi, pop 등
- 분위기: cheerful, futuristic, calm, energetic 등
- 용도: "product showcase", "background music", "commercial"
- 길이: "30 seconds", "1 minute"

## 제출 방법

- **제출처:** 본인 학생 페이지
- **형식:**
  - 렌더 이미지 2장 (Eevee 1장, Cycles 1장) - PNG 또는 JPG
  - AI 생성 영상 1개 - MP4
  - AI 생성 BGM 1개 - MP3
  - 각각의 프롬프트와 한줄 코멘트 (텍스트로 작성)
- **기한:** 다음 수업 전까지

### 코멘트 작성 예시

```
[Eevee 렌더] Bloom과 AO를 활용하여 로봇 눈의 발광 효과를 강조했습니다.
[Cycles 렌더] Denoising + 256 Samples로 금속 반사를 사실적으로 표현했습니다.
[AI 영상] 프롬프트: "A cute robot slowly waving with soft studio lighting"
[AI BGM] 프롬프트: "cheerful electronic music for robot product showcase, 30 seconds"
         Suno AI로 생성, 밝고 경쾌한 느낌의 BGM을 선택했습니다.
```

## 평가 기준

| 항목 | 비율 | 세부 기준 |
|------|------|-----------|
| 렌더링 품질 | 30% | Camera 구도가 적절한가, 렌더 설정(Bloom, AO, Denoising 등)을 활용했는가 |
| AI 영상 활용 | 30% | AI 영상이 자연스러운가, 프롬프트가 구체적이고 효과적인가 |
| AI 음악 활용 | 20% | BGM이 프로모션 영상에 어울리는가, 프롬프트가 적절한가 |
| 프롬프트 작성 | 20% | 영문 프롬프트의 구체성과 창의성, 코멘트의 충실도 |

## 참고 자료

- [Kling AI](https://klingai.com) - AI 이미지 -> 비디오 생성
- [Veo (Google Gemini)](https://gemini.google.com) - AI 텍스트 -> 비디오 생성
- [Suno AI](https://suno.com) - AI 음악 생성
- [ElevenLabs](https://elevenlabs.io) - AI Sound Effects / 음악 생성
- [Blender Manual: Rendering](https://docs.blender.org/manual/en/latest/render/index.html)
- [Blender Manual: Camera](https://docs.blender.org/manual/en/latest/render/cameras.html)
