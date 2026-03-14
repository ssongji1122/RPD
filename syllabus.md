# 로봇프러덕트 디자인 (Robot Product Design) - 2026 Spring Syllabus

## 교과목 정보

| 항목 | 내용 |
|------|------|
| 교과목명 | 로봇프러덕트 디자인 (Robot Product Design) |
| 학수번호 | DET3012-001 |
| 학점 | 3.0 |
| 강의시간 | 화요일 10:00 - 15:00 |
| 강의실 | 60주년기념관 908호 |
| 대학 | 인하대학교 |
| 학기 | 2026학년도 1학기 (Spring 2026) |

> **필수 소프트웨어:** 본 수업은 **Blender 5.0**을 기준으로 진행됩니다. 반드시 Blender 5.0 이상 버전을 설치하여 사용하시기 바랍니다. 이전 버전(4.x 이하)은 UI 및 기능 차이로 인해 실습 진행이 어려울 수 있습니다.

---

## 주차별 강의 계획

| 주차 | 강의주제 | 강의내용 | 실습내용 | AI 도구 | 과제 | 비고 |
|:----:|----------|----------|----------|---------|------|------|
| 01 | 오리엔테이션, Blender 설치, 컨셉 설정 | 수업 목표/평가/일정 안내, 2026 캐릭터 프로덕트 트렌드 분석 | Blender 5.0 설치 및 환경 설정, Mixboard + 나노바나나를 활용한 무드보드 제작 | Mixboard, 나노바나나 | 무드보드 Discord 제출 | |
| 02 | Blender 인터페이스 및 기초 + MCP 설정 | Blender 5.0 UI (Viewport, Outliner, Properties), 뷰 조작, Transform (G/R/S), Apply Transform (Ctrl+A), Origin 설정, Pivot Point | 기본 도형(Primitive) 배치 연습, Blender MCP + Claude 설치 및 연결 | Blender MCP + Claude | 기본 도형 배치 + MCP 테스트 스크린샷 제출 | |
| 03 | 기초 모델링 1 - Edit Mode + Modifier | Edit Mode 핵심 도구, Modifier 개념, Mirror / Subdivision / Solidify / Array / Boolean, Bevel Tool vs Bevel Modifier, Weighted Normal, Join/Separate, Apply 타이밍 | Extrude, Loop Cut, Inset, Bevel로 기본형 제작 후 Mirror + Subdivision + Solidify + Array + Boolean 적용, 파츠 정리와 음영 확인 실습 | - | Edit Mode + Modifier를 함께 사용한 로봇/캐릭터 기본 형태 제출 | |
| 04 | 기초 모델링 2 - 하드서피스 디테일 & 정리 | 얼굴/관절/패널 디테일 추가, Bevel/Weighted Normal 반복 적용, Boolean/Inset 디테일 심화, 파츠 정리 반복 | Week 03 기본형에 얼굴/관절/패널 디테일 추가, 음영 정리, 파츠 정리 실습 | - | 로봇/캐릭터 디테일 정리 결과물 제출 | |
| 05 | AI 3D 생성 + Sculpting + MCP | AI 3D 생성 원리 이해, Sculpt Mode 기초 (Draw, Clay Strips, Smooth, Grab) | Meshy AI / Tripo AI로 3D 모델 생성 후 Blender 임포트, Sculpt 수정 작업, MCP 씬 자동 생성 | Meshy AI, Tripo AI, Luma Genie, Blender MCP | AI 3D 생성 + Blender 작업 이미지 제출 | |
| 06 | Material & Shader Node | Material 생성, Principled BSDF (Base Color, Metallic, Roughness, Specular), Thin Film Iridescence (5.0 신기능), Shader Node Editor | Poly Haven / BlenderKit 텍스처 활용, 로봇에 금속/플라스틱/유리 재질 적용 | - | 로봇/캐릭터 재질 적용 이미지 제출 | |
| 07 | UV Unwrapping + AI Texture | UV 개념, Seam (Mark Seam), Unwrap 방법, UV Editor 활용 | Texture 이미지 적용, AI 텍스처 생성 및 적용, Texture Painting | Meshy AI Texture, 나노바나나 | 텍스처 적용된 로봇 렌더 이미지 제출 | |
| **08** | **중간고사 - 중간 프로젝트 발표** | 로봇/캐릭터 모델링 + 텍스처 완성본 제출 (렌더 이미지 3장 이상 + .blend 파일) | - | - | 중간 프로젝트 제출 | **배점: 35%** |
| 09 | Lighting 기초 + MCP 조명 연출 | 조명 종류 (Point, Sun, Spot, Area), 3-Point Lighting, HDRI 환경 조명, Blender 5.0 색상 관리 (AgX vs ACES) | Poly Haven HDRI 적용, Blockade Labs AI HDRI 생성, Claude MCP 조명 자동 연출 | Blockade Labs Skybox, Blender MCP | 3가지 조명 환경 렌더 이미지 제출 | |
| 10 | Animation 기초 | Timeline, Keyframe (I), 오브젝트 애니메이션 (이동/회전/스케일), Graph Editor 기초 | 3~5초 로봇 움직임 애니메이션 제작 | - | 3~5초 간단한 애니메이션 제출 | |
| 11 | Rigging 기초 | Armature, Bone 구조 (Parent-Child), IK/FK, Weight Painting, Pose Mode | 로봇 팔/다리 기초 리깅 작업 | - | 기초 리깅 적용 결과물 제출 | |
| 12 | AI 활용 리깅 (Mixamo) | Mixamo 자동 리깅 원리, 애니메이션 라이브러리 활용, NLA Editor 기초 | Mixamo 리깅 후 Blender 임포트, 애니메이션 편집 | Mixamo | Mixamo 리깅/애니메이션 적용 결과물 제출 | |
| 13 | AI 영상/사운드 + 렌더링 + MCP | Camera 설정 (Focal Length, DOF), Eevee vs Cycles 비교, 5.0 색상 관리, Compositor 기초 | Kling AI (이미지에서 비디오 생성), Suno AI (BGM 생성), MCP 카메라/렌더 자동화 | Kling AI, Veo, Suno AI, ElevenLabs Music, Blender MCP | 렌더링 + AI 영상/사운드 테스트 결과물 제출 | |
| 14 | 최종 프로젝트 제작 | 기말 프로젝트 본격 제작, 개별 피드백 진행 | 최종 프로젝트 자유 작업 | - | 최종 프로젝트 중간 체크 제출 | |
| **15** | **기말고사 - 최종 프로젝트 발표** | 최종 프로덕트 완성본 제출 (렌더 이미지 + .blend 파일 + 영상) 및 발표 | - | - | 최종 프로젝트 제출 및 발표 | **배점: 35%** |
