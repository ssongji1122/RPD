# RPD 외부 AI 도구 최신성 감사 (2026-06)

- 감사일: 2026-06-02
- 대상: RPD 2026 봄학기 자료(syllabus.md, course-site 데이터)에 등장하는 외부 AI/SaaS 도구
- 자료 작성 시점: 대부분 2026년 3월 (약 3개월 경과)
- 방법 caveat: 이 환경은 shell/grep 미제공. 도구 인벤토리는 `syllabus.md`의 "AI 도구" 컬럼(저자 큐레이션, 권위 소스) + `course-site/data/curriculum.js` 본문 cross-check 기반. 본문(curriculum/i18n)은 AI 도구를 추상적으로만 언급하고, 도구별 공식 URL/가격은 자료에 직접 명시돼 있지 않음(Blender 공식 문서 링크만 존재). 따라서 "자료 내 설명/용도" 칸은 syllabus 컬럼 + 주차 실습 맥락 기준.
- 모든 현황 주장은 웹 검색/공식 페이지 fetch 기반. 신뢰수준: [High] 공식/다수 cross-ref, [Medium] 2차 출처 다수, [Low] 단일/불명확.

## 도구별 감사 표

| 도구 | 자료 내 설명/용도 | 2026-06 현황 | 변동 유형 | 수업 실습 영향 | 신뢰수준 | 출처 | 권장 조치 |
|------|------------------|-------------|----------|--------------|---------|------|----------|
| Mixboard | W1: 무드보드/디자인 컨셉 설정 (나노바나나와 함께) | Google Labs 실험 도구, 무료. 2025-10 기준 180개국+ 확대로 **한국 사용 가능**. Google 계정만 필요. 고급 AI 기능(Nano Banana Pro/Gemini 3)은 일일 한도 + AI Ultra 유료 상향. `regionError=true`는 미지원 지역용 안내일 뿐 한국 영향 없음 | 가용성 확대(한국 정식 지원), 무료 유지 | 낮음(긍정적). 무료로 W1 실습 완주 가능. 단 고급 이미지 생성은 일일 한도 | High | [Mixboard 180+국 확대(blog.google)](https://blog.google/technology/google-labs/mixboard-180-more-countries/), [TechCrunch 출시](https://techcrunch.com/2025/09/24/google-launches-an-ai-powered-mood-board-app-mixboard/), [공식](https://mixboard.google.com) | 공식 URL `mixboard.google.com`(또는 `labs.google.com/mixboard`) 확인. 한국 접근 가능 명시. 변동 없음 수준 |
| 나노바나나 (Nano Banana) | W1/W7: 무드보드 이미지 + AI 텍스처 생성 | "Nano Banana" = Google **Gemini 2.5 Flash Image**의 별칭(2025-08-26 공식 출시). 2026-06 현재 모델 세대 진화: **Nano Banana Pro**(Gemini 3 Pro Image), **Nano Banana 2**(Gemini 3.x Flash). Gemini 앱/웹 무료 사용 가능하나 **일일 생성 한도**(2차 출처는 Basic 약 20장/일). Pro 고해상도(2K/4K)는 유료(Google AI Pro $19.99/월~) | 리브랜딩/모델 세대 변화. "나노바나나"가 단일 모델명에서 모델 패밀리 별칭으로 | 중간. 무료 일일 한도 내 W1/W7 실습 가능하나, 자료가 단일 모델로 설명했다면 현재 Pro/2 세대 구분 반영 필요 | High (별칭/세대 사실) / Medium (구체 일일 한도 수치는 공식 재확인 권장) | [Gemini 2.5 Flash Image 출시(Google Developers)](https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/), [Nano Banana Pro(blog.google)](https://blog.google/innovation-and-ai/products/nano-banana-pro/), [무료 티어 한도(aifreeapi)](https://www.aifreeapi.com/en/posts/gemini-image-free-tier-2026) | "나노바나나 = Gemini 2.5 Flash Image, Gemini 앱에서 무료(일일 한도)" 명시. Pro/2 세대 존재 각주. 일일 한도 정확값은 수업 직전 Gemini 앱에서 확인 |
| Meshy AI | W5: 텍스트→3D 모델 생성 후 Blender 임포트 / W7: AI 텍스처(=Meshy 기능, 별도 도구 아님) | Free 플랜 유지: 월 100 크레딧. 단 **Meshy 5 모델 월 10 다운로드 한도 + CC BY 4.0(출처표기 필수)**. Meshy 6는 무료 다운로드 불가(생성만). 사유화/무제한 다운로드는 Pro $20/월 | 무료 유지하나 다운로드/라이선스 제약 명확화 | 중간. 무료로 W5 생성·소량 다운로드 가능하나 월 10회 한도 + CC BY. 학생 다수가 반복 생성 시 한도 도달 가능 | High | [Meshy 공식 pricing](https://www.meshy.ai/pricing), [크레딧/다운로드 한도(Help Center)](https://help.meshy.ai/en/articles/12062933-what-are-your-prices-and-plans-offered-and-do-you-have-monthly-annual-plans) | "무료 월 100크레딧 + 월 10 다운로드 + CC BY 4.0" 명시. "Meshy AI Texture"는 별도 도구 아닌 Meshy 기능으로 표기 정정 |
| Tripo AI | W5: 텍스트→3D 모델 생성 (Meshy 대안) | Free Basic 유지: 월 300 크레딧. **무료는 public-only(모델 공개) + CC BY 4.0, 상업적 사용 불가**. 상업권/비공개는 Pro $19.90/월(3,000 크레딧) | 무료 유지, 라이선스 제약 명확화 | 낮음~중간. 무료 크레딧이 Meshy보다 넉넉(300). 수업 실습(비상업)엔 충분. 단 공개 모델 됨 | High | [Tripo 공식 pricing](https://www.tripo3d.ai/pricing), [무료 플랜 리뷰(lorphic)](https://lorphic.com/tripo-ai-pricing-explained-guide/) | "무료 월 300크레딧, 모델 공개+CC BY" 명시. W5 무료 대안으로 Meshy보다 크레딧 여유 |
| Luma Genie | W5: 텍스트→3D 생성 (Meshy/Tripo와 함께 나열) | **단독 제품으로 흐릿해짐**. `lumalabs.ai/genie/`가 메인 플랫폼으로 리다이렉트. Luma가 Dream Machine(영상) 중심으로 피벗하며 Genie deprioritize. 공식 단종 발표는 없으나 단독 가용성/가격 불명확. 일부 리뷰는 2026-05까지 존재 언급 | 사실상 deprioritize/제품 경계 모호 (단종은 아님) | 높음(주의). W5에서 Genie를 "바로 쓰는 도구"로 안내하면 학생이 진입점을 못 찾을 위험. Meshy/Tripo가 안정적 대안 | Medium | [Genie 리다이렉트/상태(aiapps)](https://www.aiapps.com/items/genie-by-lumalabs/), [Luma 공식](https://lumalabs.ai/), [상태 재확인(toolworthy)](https://www.toolworthy.ai/tool/luma-ai-genie) | W5에서 Luma Genie를 **보조/선택**으로 강등하거나 제거, Meshy+Tripo를 주력으로. 안내 전 `lumalabs.ai/genie` 진입 동작 직접 확인 권장 |
| Blockade Labs Skybox | W9: AI HDRI 생성 → Blender 환경 조명 | **공식 멤버십 페이지 확정(2026-06-02 WebFetch)**: Free는 "5 generations to get you started" + **"Preview only (no exports)" — 다운로드 자체 불가(저해상도조차 안 됨)**. Essential $20/월(8K export, HDRI 미포함). **HDRI export는 Standard $48/월부터**. Business $112/월(16K) | 무료로 HDRI 다운로드 불가(공식 확정) | **높음(실습 차단)**. W9 실습 목표가 "AI HDRI 생성 후 Blender 조명 적용"인데, 무료론 export 자체 불가 → 학생이 실제 HDRI를 못 씀. 최저 HDRI 플랜이 $48/월 | High | [Skybox 공식 멤버십/가격](https://skybox.blockadelabs.com/membership) (직접 fetch 확인), [Skybox AI 공식](https://www.blockadelabs.com/) | W9 재설계: (a) 무료는 "생성 체험"만으로 한정 + 실제 조명은 **Poly Haven 무료 HDRI(CC0)**로 진행, (b) Skybox는 데모로만. 학생 결제 유도 금지 |
| Mixamo | W12: 자동 리깅 + 애니메이션 라이브러리 | **무료 유지, 운영 중**(2026-05 기준 정상). 단 장기 불확실성: Adobe가 CC 구독 연동 강화(2024~), CC 없는 사용자 접근 disruption 사례, 2025-06 장애 + "더 이상 지원 안 함" 발언 보고. 인수 후 기능 업데이트 사실상 없음. 휴머노이드 이족만 지원 | 무료 유지하나 미래 불확실 + 간헐 장애 이력 | 중간. 현재 W12 무료 실습 가능. 단 수업 당일 장애/접근 이슈 대비 필요 | High | [Mixamo FAQ(Adobe)](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html), [상태 모니터(StatusGator)](https://statusgator.com/services/adobe-creative-cloud/mixamo), [대안 정리(MoCap Online)](https://mocaponline.com/blogs/mocap-news/mixamo-alternatives) | "무료 유지하나 장애 이력 있음" 주석. 백업 플랜(Blender 내장 Rigify 또는 사전 다운로드 애니메이션) 준비. Adobe 계정 필요 여부 사전 안내 |
| Kling AI | W13: 이미지→비디오 생성 | Free 일일 크레딧 제공(2차 출처: 약 66 크레딧/일, 매일 갱신·누적 안 됨). **무료는 워터마크 + 약 5초 + 720p + 비상업용**. 유료 Standard $6.99/월~. 현재 Kling 3.0 세대 | 무료 유지, 제약(워터마크/길이) 존재. 버전 진화 | 낮음~중간. W13은 "테스트 결과물" 목적이라 무료로 충분. 단 워터마크/5초 한계 학생에게 사전 고지 | High (무료+워터마크+비상업 방향) / Medium (66크레딧·5초 구체 수치는 2차 출처) | [무료 크레딧(aiimagetovideo)](https://aiimagetovideo.pro/blog/free-kling-ai-video-generator/), [Kling 3.0 pricing(soravideo)](https://soravideo.art/blog/kling-3-pricing) | "무료 일일 크레딧, 워터마크+짧은 길이+720p" 명시. 정확 수치는 공식 사이트 확인. W13 무료 실습은 가능 |
| Veo | W13: 이미지/텍스트→비디오 (Kling과 함께) | 현재 **Veo 3.1 / Veo 3.1 Lite**로 진화. **무료 Gemini로는 사용 불가**. 한국은 Gemini 지원국이며 Google AI Pro($19.99/월) 구독자가 Flow에서 제한적 접근 + Gemini 앱 10팩 트라이얼. 최상위는 AI Ultra($249.99/월) | 버전 진화 + 무료 접근 거의 불가(유료 구독 필요) | **높음(무료 실습 어려움)**. W13에서 Veo를 무료 도구로 기대하면 학생 대부분 접근 불가. Kling/무료 대안 대비 진입장벽 큼 | High | [Veo 한국 포함 Gemini 확대(blog.google)](https://blog.google/products-and-platforms/products/gemini/veo-3-expansion-mobile/), [Veo 3 pricing 2026(veo3ai)](https://www.veo3ai.io/blog/veo3-free-trial-how-to-get-free-access-2026), [Gemini 한국 지원(TechCrunch)](https://techcrunch.com/2026/04/20/google-rolls-out-gemini-in-chrome-in-seven-new-countries/) | W13에서 Veo는 "유료/선택(Pro 구독 시)"로 명확히 구분. 무료 주력은 Kling. "무료 Gemini로 Veo 불가" 고지 |
| Suno AI | W13: BGM 생성 | Free 유지: 약 10곡/일(50 일일 크레딧, 곡당 5크레딧). **무료는 비상업용**. 현재 v5.5 모델. 상업권/사유화는 Pro $10/월(2,500 크레딧) | 무료 유지, 버전 진화(v5.5) | 낮음. W13 "테스트 결과물"엔 무료 충분. 비상업 한계만 고지 | High | [Suno 공식 pricing](https://suno.com/pricing), [무료 플랜(soundverse)](https://www.soundverse.ai/blog/article/is-suno-ai-free-1123) | "무료 약 10곡/일, 비상업" 명시. W13 무료 실습 가능 |
| ElevenLabs Music | W13: AI 사운드/BGM (Suno 대안) | 정식명 **Eleven Music**(2025-08 출시, **상업용 클리어가 차별점** — 라이선스 데이터 기반). 2026-04-01 iOS 앱 ElevenMusic 출시. **무료 7곡/일**. Pro $9.99/월(500곡). 2026-05 장르 전환 신모델 발표 | 신규 제품 정착 + 무료 가능 | 낮음. W13 무료 7곡/일로 충분. Suno와 달리 상업 사용 라이선스 명확 | High | [Eleven Music 출시(TechCrunch)](https://techcrunch.com/2025/08/05/elevenlabs-launches-an-ai-music-generator-which-it-claims-is-cleared-for-commercial-use/), [ElevenMusic 앱(TechCrunch)](https://techcrunch.com/2026/04/02/elevenlabs-releases-a-new-ai-powered-music-generation-app/), [Music 공식](https://elevenlabs.io/music) | 정식명 "Eleven Music"으로 표기. "무료 7곡/일" 명시. 공식 URL `elevenlabs.io/music` |
| Blender MCP + Claude | W2(설치)/W5/W9/W13: Claude로 Blender 자연어 제어 (씬 생성, 조명/카메라 자동화) | **중대 변화(긍정)**: 2026-04-28 Anthropic이 **공식 Blender 커넥터** 출시(9개 창작 도구 통합 중 하나). **모든 Claude 플랜(무료 포함)에서 작동**, claude.ai/connectors + `blender.org/lab/mcp-server/` 드래그앤드롭 설치(터미널 불필요). Anthropic이 Blender Development Fund 후원사 합류. 기존 ahujasid 비공식 MCP도 오픈소스 유지 | 공식 커넥터 등장(설치 방식 대폭 간소화) | 중간~높음(긍정적). 자료의 W2 설치가 구버전 비공식 MCP(터미널/uv 설치)라면, 공식 커넥터로 업데이트 시 학생 진입장벽 크게 하락 | High | [공식 커넥터 9종(9to5Mac)](https://9to5mac.com/2026/04/28/anthropic-releases-9-new-claude-connectors-for-creative-tools-including-blender-and-adobe/), [Blender 펀딩+커넥터(Digital Production)](https://digitalproduction.com/2026/04/30/anthropic-funds-blender-ships-claude-connector/), [원본 ahujasid](https://github.com/ahujasid/blender-mcp) | **W2 설치 가이드 업데이트 권장**: 공식 커넥터(드래그앤드롭, 무료 플랜 OK) 안내. 단 "임의 Python 실행 → 작업 저장 후 사용" 안전 주의 추가. (참고: curriculum.js W2 steps에는 MCP 설치 step이 보이지 않아 syllabus와 본문 간 정합성 별도 점검 필요 — audit 범위 밖) |
| Poly Haven (보조) | W6/W9: 무료 텍스처/HDRI 에셋 | 변동 없음. CC0(퍼블릭 도메인), 로그인 불필요, 상업 사용 자유. BlenderKit에 통합됨. 생성형 AI 아닌 실측 에셋 | 변동 없음 | 없음(안정). W6/W9 무료 핵심 자원. W9 Skybox 무료 한계의 대체재로 가치 상승 | High | [Poly Haven 라이선스(CC0)](https://polyhaven.com/license), [공식](https://polyhaven.com/) | 변동 없음. W9 HDRI 실습의 무료 대안으로 적극 활용 |
| BlenderKit (보조) | W6: 텍스처/에셋 라이브러리 | 변동 없음. 무료 티어 + Poly Haven 에셋 통합 제공. Blender 애드온 | 변동 없음 | 없음(안정) | Medium | [BlenderKit×Poly Haven](https://www.blenderkit.com/articles/polyhaven-hdris-in-blenderkit-add-on/) | 변동 없음 |

## 변동 우선순위 요약

### 실습이 깨지거나 막히는 것 (최우선)
1. **Blockade Labs Skybox (W9)** — 공식 페이지 확정: 무료는 export 자체 불가(저해상도조차 안 됨), HDRI는 $48/월부터. W9 "AI HDRI 생성→조명 적용"이 무료로 완주 불가. → Poly Haven 무료 HDRI(CC0)로 대체, Skybox는 생성 체험만.
2. **Veo (W13)** — 무료 Gemini로 사용 불가, Google AI Pro($19.99/월) 이상 필요. → W13 무료 주력을 Kling으로, Veo는 유료/선택 명시.
3. **Luma Genie (W5)** — 단독 제품 deprioritize(Dream Machine으로 피벗), 진입점 모호. → Meshy+Tripo 주력, Genie 강등/제거.

### 리브랜딩/제품명 정정
4. **나노바나나** — Gemini 2.5 Flash Image 별칭. 현재 Nano Banana Pro/2 세대 존재. 무료는 Gemini 앱 일일 한도.
5. **ElevenLabs Music → Eleven Music** — 정식명 정정. 무료 7곡/일, 상업 라이선스 클리어.
6. **Meshy "AI Texture"** — 별도 도구 아닌 Meshy 기능. 무료 다운로드 월 10회 + CC BY 4.0 제약 명시.

### 긍정적 업데이트 (반영 시 학생 편의 상승)
7. **Blender MCP 공식 커넥터 (W2)** — 2026-04 Anthropic 공식 출시, 무료 플랜 OK, 드래그앤드롭 설치. 구버전 설치 가이드 업데이트 권장.

### 무료 제약 고지 필요 (실습은 가능하나 한계 안내)
8. Kling(워터마크+짧은 길이+720p), Suno(비상업), Tripo(모델 공개), Mixboard/나노바나나(일일 한도).

### 주의 관찰
9. **Mixamo (W12)** — 무료 유지하나 Adobe의 장기 방치 + 간헐 장애 이력. 백업 플랜(Rigify 등) 준비.

### 변동 없음 (안정)
10. Poly Haven, BlenderKit — CC0/무료 안정. W9 Skybox 무료 한계의 대체재로 가치 상승.

## 방법 한계 (caveat)
- shell/glob 미제공 환경 → `docs/` 디렉토리 전수 열거 불가. syllabus.md "AI 도구" 컬럼(저자 큐레이션)을 권위 소스로 삼고 curriculum.js 본문과 cross-check. 그에 대해 인벤토리는 완전.
- 가격/티어는 가능한 공식 pricing 페이지(Meshy, Tripo, Suno, Skybox 등) 우선. 무료 일일 한도 등 일부 구체 수치는 2차 출처라 [Medium] 처리 + 공식 재확인 권장 표기.
- 도구 가입/결제/사용은 하지 않음(웹 정보 조사만).
