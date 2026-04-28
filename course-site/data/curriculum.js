// ============================================================
// 15주 블렌더 수업 커리큘럼 데이터
// 이 파일은 weeks/site-data.json 에서 자동 생성됩니다.
// ============================================================

const CURRICULUM = [
  {
    "week": 1,
    "status": "done",
    "title": "오리엔테이션, Blender 설치, Mixboard 활용하여 디자인 컨셉 설정",
    "subtitle": "오리엔테이션 · Blender 설치 · 컨셉 설정",
    "duration": "~2시간",
    "topics": [
      "수업 소개 및 방향",
      "Blender 설치 및 실행 확인",
      "Mixboard 디자인 컨셉 설정"
    ],
    "steps": [
      {
        "title": "Blender 설치",
        "copy": "blender.org에서 다운로드 후 실행 확인.",
        "goal": [
          "Blender 공식 사이트에서 설치 파일 다운로드",
          "실행 후 Welcome Screen 확인"
        ],
        "done": [
          "Blender가 정상적으로 열린다",
          "버전 번호를 확인했다"
        ],
        "tasks": [
          {
            "id": "w1-t1",
            "label": "blender.org 에서 다운로드 완료",
            "detail": "최신 LTS 버전 권장"
          },
          {
            "id": "w1-t2",
            "label": "Blender 처음 실행 완료",
            "detail": "Welcome Screen이 보이는지 확인"
          }
        ]
      },
      {
        "title": "컨셉 설정 (Mixboard)",
        "copy": "이번 수업에서 뭘 만들고 싶은지 이미지로 모아두세요. 방향이 있으면 매 주 수업이 훨씬 재밌어져요.",
        "goal": [
          "Mixboard를 열어 레이아웃 구성",
          "3개 이상 레퍼런스 이미지 수집"
        ],
        "done": [
          "Mixboard에 적어도 3개 이상 이미지가 있다",
          "어떤 걸 만들지 한 문장으로 설명할 수 있다"
        ],
        "tasks": [
          {
            "id": "w1-t3",
            "label": "레퍼런스 이미지 3개 이상 수집",
            "detail": ""
          },
          {
            "id": "w1-t4",
            "label": "Mixboard 보드 캡처해서 저장",
            "detail": ""
          }
        ]
      }
    ],
    "shortcuts": [
      {
        "keys": "LMB",
        "action": "선택 (Left Mouse Button)"
      },
      {
        "keys": "Ctrl + S",
        "action": "파일 저장"
      },
      {
        "keys": "Ctrl + Z",
        "action": "되돌리기 (Undo)"
      },
      {
        "keys": "Ctrl + Shift + Z",
        "action": "다시 실행 (Redo)"
      }
    ],
    "explore": [],
    "assignment": {
      "title": "Blender 설치 확인 스크린샷",
      "description": "Blender를 실행해서 Welcome Screen이 보이는 화면을 캡처해서 제출하세요.",
      "checklist": [
        "Blender 정상 실행 확인",
        "버전 번호 포함된 스크린샷 제출"
      ]
    },
    "mistakes": [
      "설치 중 권한 오류 → 관리자 권한으로 재설치",
      "한글 경로에 설치하면 오류 → 영어 경로 사용"
    ],
    "videos": [
      {
        "title": "Blender Studio - First Steps",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/first-steps/"
      }
    ],
    "docs": [
      {
        "title": "Blender 설치 가이드",
        "url": "https://docs.blender.org/manual/en/latest/getting_started/installing/index.html"
      },
      {
        "title": "시작하기",
        "url": "https://docs.blender.org/manual/en/latest/getting_started/index.html"
      }
    ],
    "summary": "Blender 설치, Mixboard로 컨셉 설정."
  },
  {
    "week": 2,
    "status": "done",
    "title": "Blender 인터페이스 및 기초",
    "subtitle": "화면 조작 · 오브젝트 변형 · 첫 모델링",
    "duration": "~3시간",
    "topics": [
      "Blender 인터페이스 구조",
      "화면 조작 (Orbit/Pan/Zoom)",
      "오브젝트 기본 변형 (G/R/S)",
      "Extrude / Bevel / Loop Cut"
    ],
    "steps": [
      {
        "title": "프리퍼런스 세팅",
        "copy": "Blender를 처음 열면 옵션이 너무 많아서 압도돼요. 일단 수업과 같은 세팅으로 맞춰두면 헷갈릴 일이 줄어요.",
        "goal": [
          "Preferences 위치를 안다",
          "입력 장치 제약을 먼저 해결한다"
        ],
        "done": [
          "Preferences를 직접 열 수 있다",
          "필요 시 Emulate 설정을 켰다"
        ],
        "tasks": [
          {
            "id": "w2-t1",
            "label": "Edit → Preferences 직접 열어보기",
            "detail": "단축키: Ctrl + , (쉼표)"
          },
          {
            "id": "w2-t2",
            "label": "Input → Emulate 3 Button Mouse 켜기",
            "detail": "마우스 휠 없는 경우"
          },
          {
            "id": "w2-t3",
            "label": "저장 방식 Preferences에서 확인",
            "detail": "Auto-Save 설정 위치 파악"
          }
        ],
        "image": "assets/images/week02/ui-overview.png",
        "showme": "blender-preferences"
      },
      {
        "title": "화면 조작",
        "copy": "구글 지도에서 거리뷰를 돌리는 것처럼, Blender 화면도 마우스로 돌리고 확대해요. 처음엔 어색하지만 10분만 하면 익숙해져요.",
        "goal": [
          "Orbit/Pan/Zoom을 자유롭게 쓴다",
          "정면/측면/상면 뷰로 이동한다"
        ],
        "done": [
          "Numpad 1/3/7로 뷰 전환 가능",
          "마우스를 잃지 않고 오브젝트를 따라다닐 수 있다"
        ],
        "tasks": [
          {
            "id": "w2-t4",
            "label": "Numpad 1/3/7 로 뷰 전환 연습",
            "detail": ""
          },
          {
            "id": "w2-t5",
            "label": "Scroll로 Zoom In/Out 해보기",
            "detail": ""
          },
          {
            "id": "w2-t6",
            "label": "Middle Mouse로 Orbit 해보기",
            "detail": "없으면 Alt+LMB"
          }
        ],
        "image": "assets/images/week02/navigation-gizmo.png",
        "showme": "viewport-navigation"
      },
      {
        "title": "기본 변형 (G/R/S)",
        "copy": "G/R/S 세 글자만 기억하면 돼요. G(잡아서 이동), R(돌리기), S(늘리거나 줄이기). 그 다음에 X/Y/Z를 누르면 방향도 고정할 수 있어요.",
        "goal": [
          "G/R/S 단축키를 손에 익힌다",
          "축 고정 (X/Y/Z)을 이해한다"
        ],
        "done": [
          "G → X 처럼 축 고정 이동이 된다",
          "숫자 입력으로 정확한 값 이동이 된다"
        ],
        "tasks": [
          {
            "id": "w2-t7",
            "label": "G → X로 X축 방향으로만 이동",
            "detail": ""
          },
          {
            "id": "w2-t8",
            "label": "S → 0.5 로 절반 크기로 줄이기",
            "detail": ""
          },
          {
            "id": "w2-t9",
            "label": "R → Z → 45 로 45도 회전",
            "detail": ""
          }
        ],
        "image": "assets/images/week02/transform-gizmo.png",
        "showme": "transform-grs",
        "widgets": [
          {
            "type": "showme",
            "id": "origin-vs-3dcursor"
          }
        ]
      },
      {
        "title": "Edit Mode 모델링",
        "copy": "Tab 키 하나로 '보는 모드'와 '편집 모드'를 오가요. Extrude(E)는 점토를 손으로 당기는 것처럼 면을 뽑아내는 거예요.",
        "goal": [
          "Object/Edit Mode 전환을 안다",
          "면을 선택하고 Extrude로 뽑는다"
        ],
        "done": [
          "Tab 키로 모드 전환이 된다",
          "단순한 상자형 구조를 만들었다"
        ],
        "tasks": [
          {
            "id": "w2-t10",
            "label": "Tab으로 Edit Mode 진입/복귀",
            "detail": ""
          },
          {
            "id": "w2-t11",
            "label": "면 선택 후 E로 Extrude 하기",
            "detail": "위나 아래 방향으로 뽑기"
          },
          {
            "id": "w2-t12",
            "label": "Ctrl+R로 Loop Cut 추가해보기",
            "detail": "마우스로 위치 조정 후 클릭"
          }
        ],
        "image": "assets/images/week02/editmode-modeling.png",
        "showme": [
          "edit-mode",
          "extrude",
          "loop-cut"
        ]
      },
      {
        "title": "Bevel 마무리",
        "copy": "날카로운 모서리를 부드럽게 깎는 거예요. 실제 제품 디자인에서도 안전을 위해 모서리를 깎는데 (Chamfer), 그게 Bevel이에요.",
        "goal": [
          "Bevel의 원리를 이해한다",
          "최종 형태를 Object Mode에서 확인한다"
        ],
        "done": [
          "Ctrl+B로 Bevel이 됐다",
          "결과물을 스크린샷으로 저장했다"
        ],
        "tasks": [
          {
            "id": "w2-t13",
            "label": "모서리 선택 후 Ctrl+B로 Bevel",
            "detail": "스크롤로 분할 수 조절"
          },
          {
            "id": "w2-t14",
            "label": "Tab으로 Object Mode 복귀 후 확인",
            "detail": ""
          },
          {
            "id": "w2-t15",
            "label": "F12로 렌더 or 스크린샷 저장",
            "detail": ""
          }
        ],
        "image": "assets/images/week02/bevel-tool.png",
        "showme": "bevel-tool",
        "widgets": [
          {
            "type": "showme",
            "id": "box-rounding"
          }
        ]
      },
      {
        "title": "뷰포트 셰이딩",
        "copy": "같은 모델도 어떤 '조명 방식'으로 보느냐에 따라 전혀 다르게 보여요. Solid는 작업 중 기본 뷰, Material Preview는 재질 확인, Rendered는 실제 렌더 결과예요.",
        "goal": [
          "4가지 Shading 모드를 구분한다",
          "작업 목적에 맞는 모드를 선택한다"
        ],
        "done": [
          "Z Pie Menu로 빠르게 모드 전환이 된다",
          "Solid와 Material Preview 차이를 말할 수 있다"
        ],
        "tasks": [
          {
            "id": "w2-t16",
            "label": "Z 키로 Pie Menu 열어 모드 전환",
            "detail": "Wireframe / Solid / Material Preview / Rendered"
          },
          {
            "id": "w2-t17",
            "label": "Solid 모드에서 Cavity/Matcap 바꿔보기",
            "detail": "헤더 오른쪽 구 아이콘 클릭"
          },
          {
            "id": "w2-t18",
            "label": "Material Preview로 HDRI 환경 확인",
            "detail": "재질 없어도 형태는 확인 가능"
          }
        ],
        "showme": [
          "viewport-shading",
          "xray-opacity"
        ]
      }
    ],
    "shortcuts": [
      {
        "keys": "Middle Mouse",
        "action": "회전"
      },
      {
        "keys": "Shift + Middle Mouse",
        "action": "이동"
      },
      {
        "keys": "Scroll",
        "action": "줌"
      },
      {
        "keys": "Numpad 1 / 3 / 7",
        "action": "정면 / 측면 / 상면"
      },
      {
        "keys": "Numpad 5",
        "action": "원근 ↔ 직교"
      },
      {
        "keys": "Numpad 0",
        "action": "카메라 뷰"
      },
      {
        "keys": "Z",
        "action": "Shading 모드 전환"
      },
      {
        "keys": "G",
        "action": "이동 (Grab)"
      },
      {
        "keys": "R",
        "action": "회전 (Rotate)"
      },
      {
        "keys": "S",
        "action": "스케일 (Scale)"
      },
      {
        "keys": "G/R/S + X/Y/Z",
        "action": "축 제한"
      },
      {
        "keys": "G/R/S + 숫자 + Enter",
        "action": "정밀 입력"
      },
      {
        "keys": "Ctrl + A",
        "action": "Apply Transform"
      },
      {
        "keys": "Tab",
        "action": "Object ↔ Edit Mode 전환"
      },
      {
        "keys": "1 / 2 / 3",
        "action": "Vertex / Edge / Face 선택"
      },
      {
        "keys": "E",
        "action": "Extrude"
      },
      {
        "keys": "Ctrl + R",
        "action": "Loop Cut"
      },
      {
        "keys": "I",
        "action": "Inset"
      },
      {
        "keys": "Ctrl + B",
        "action": "Bevel"
      },
      {
        "keys": "M",
        "action": "Merge"
      },
      {
        "keys": "Shift + A",
        "action": "Primitive 추가"
      },
      {
        "keys": "F9",
        "action": "생성 옵션 조절"
      },
      {
        "keys": "Ctrl + Z",
        "action": "되돌리기 (Undo)"
      },
      {
        "keys": "Shift + N",
        "action": "Normal 재계산"
      },
      {
        "keys": "H / Alt + H",
        "action": "숨기기 / 모두 보이기"
      },
      {
        "keys": "N",
        "action": "사이드바 열기"
      }
    ],
    "explore": [],
    "assignment": {
      "title": "간단한 로우폴리 소품 만들기",
      "description": "화면 조작과 기본 모델링 도구를 사용해 간단한 소품을 만들고 제출합니다.",
      "checklist": [
        "완성 이미지 2장 이상",
        ".blend 파일 1개",
        "사용한 도구 3개 이상 적기"
      ]
    },
    "mistakes": [
      "탭(Tab) 키 없이 면을 클릭하려고 함 → Object Mode에선 편집이 안 돼요. Tab으로 Edit Mode로 먼저 들어가세요.",
      "새 박스가 이상한 곳에 생겼어요 → 3D Cursor가 이동했을 때 생기는 현상. Shift+C로 원점으로 돌려놓으세요.",
      "화면이 안 돌아가요 → 마우스 휠이 없는 경우, Preferences에서 [Emulate 3 Button Mouse]를 켜세요."
    ],
    "videos": [
      {
        "title": "Blender Studio - Viewport Navigation",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/viewport-navigation/"
      },
      {
        "title": "Blender Studio - Interface Overview",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/interface-overview/"
      },
      {
        "title": "Blender Studio - Select & Transform",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/select-transform/"
      }
    ],
    "docs": [
      {
        "title": "Preferences",
        "url": "https://docs.blender.org/manual/en/latest/editors/preferences/introduction.html"
      },
      {
        "title": "3D Navigation",
        "url": "https://docs.blender.org/manual/en/latest/editors/3dview/navigate/introduction.html"
      },
      {
        "title": "Extrude Region",
        "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_region.html"
      },
      {
        "title": "Loop Cut",
        "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/loop.html"
      },
      {
        "title": "Bevel",
        "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/bevel.html"
      }
    ],
    "summary": "Blender 인터페이스, 화면 조작, G/R/S 변형, Extrude/Bevel/LoopCut 실습."
  },
  {
    "week": 3,
    "status": "done",
    "title": "기초 모델링 1 - Modifier",
    "subtitle": "기본형 · 대칭 · 곡면 · 반복",
    "duration": "~3시간",
    "topics": [
      "Edit Mode: Extrude / Loop Cut / Inset / Bevel",
      "Mirror — 대칭 모델링",
      "Subdivision Surface / Solidify — 곡면과 두께",
      "Array / Boolean — 반복과 구멍",
      "Bevel Modifier / Weighted Normal — 마무리",
      "Modifier Stack 순서와 Apply 타이밍"
    ],
    "steps": [
      {
        "title": "레퍼런스 이미지 설정",
        "copy": "모델링 전에 참고할 이미지를 뷰포트에 깔아 두면 형태를 잡기가 훨씬 쉬워요. 정면·측면·후면 레퍼런스를 각 뷰에 배치해서 로봇의 비율과 구조를 미리 파악해요.",
        "goal": [
          "이미지 레퍼런스를 뷰포트에 올린다",
          "4가지 이미지 타입의 차이를 안다"
        ],
        "done": [
          "정면·측면 레퍼런스가 각 뷰에 정렬되어 있다",
          "모델링 도중 레퍼런스가 방해되지 않는다"
        ],
        "tasks": [
          {
            "id": "w3-ref1",
            "label": "Numpad 1 → Shift+A → Image → Reference로 정면 이미지 추가",
            "detail": "Front View 상태에서 추가해야 정면에 정렬됨"
          },
          {
            "id": "w3-ref2",
            "label": "Numpad 3 → Shift+A → Image → Reference로 측면 이미지 추가",
            "detail": "Right Side View에서 추가"
          },
          {
            "id": "w3-ref3",
            "label": "N 패널 → Item에서 투명도(Opacity) 0.3~0.5로 조절",
            "detail": "모델링 중 메쉬와 구분되도록"
          },
          {
            "id": "w3-ref4",
            "label": "Outliner에서 선택 잠금으로 실수 이동 방지",
            "detail": "화살표 아이콘 클릭 → 선택 비활성화"
          }
        ],
        "image": "assets/images/week03/robot-ref-front.png",
        "link": "https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html",
        "images": [
          "assets/images/week03/robot-ref-front.png",
          "assets/images/week03/robot-ref-side.png",
          "assets/images/week03/robot-ref-back.png"
        ],
        "downloads": [
          {
            "label": "정면 (Front)",
            "url": "assets/images/week03/robot-ref-front.png"
          },
          {
            "label": "측면 (Side)",
            "url": "assets/images/week03/robot-ref-side.png"
          },
          {
            "label": "후면 (Back)",
            "url": "assets/images/week03/robot-ref-back.png"
          }
        ],
        "showme": "image-reference"
      },
      {
        "title": "기본형 만들기",
        "copy": "레고 블록을 직접 깎아 원하는 형태를 만들어요. Extrude로 덩어리를 뽑고, Loop Cut으로 나누고, Inset과 Bevel로 다듬는 게 기본 흐름이에요.",
        "goal": [
          "Edit Mode 도구 흐름을 안다",
          "기본형을 직접 만든다"
        ],
        "done": [
          "몸통과 주요 덩어리가 잡혔다",
          "도구를 바꿔가며 형태를 만들 수 있다"
        ],
        "tasks": [
          {
            "id": "w3-t1",
            "label": "Tab으로 Edit Mode 진입",
            "detail": "Object Mode ↔ Edit Mode 전환"
          },
          {
            "id": "w3-t2",
            "label": "Extrude로 팔이나 다리 위치 뽑기",
            "detail": "E로 면을 돌출"
          },
          {
            "id": "w3-t3",
            "label": "Loop Cut으로 관절 위치 나누기",
            "detail": "Ctrl+R로 분할선 추가"
          },
          {
            "id": "w3-t4",
            "label": "Inset과 Bevel로 패널과 모서리 다듬기",
            "detail": "I, Ctrl+B 사용"
          }
        ],
        "image": "assets/images/week03/base-form.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/extrude_region.html",
        "showme": "edit-mode-tools",
        "widgets": [
          {
            "type": "showme",
            "id": "poly-circle"
          }
        ]
      },
      {
        "title": "Mirror Modifier",
        "copy": "거울 앞에 서면 반대편이 자동으로 따라오죠? Mirror가 그거예요. 한쪽만 만들면 작업량이 반으로 줄어요.",
        "goal": [
          "Mirror 역할과 기본 설정을 이해한다"
        ],
        "done": [
          "한쪽을 움직이면 반대쪽도 같이 바뀐다",
          "Clipping으로 중심선이 벌어지지 않는다"
        ],
        "tasks": [
          {
            "id": "w3-t5",
            "label": "절반을 지우고 Mirror 추가하기",
            "detail": "Add Modifier → Mirror"
          },
          {
            "id": "w3-t6",
            "label": "Clipping 켜기",
            "detail": "중심선 버텍스가 넘어가지 않게 고정"
          },
          {
            "id": "w3-t7",
            "label": "한쪽만 Extrude해서 자동 대칭 확인",
            "detail": ""
          },
          {
            "id": "w3-t8",
            "label": "중심선이 벌어지면 S + X + 0 써보기",
            "detail": "X축 0으로 다시 정렬"
          }
        ],
        "image": "assets/images/week03/mirror-modifier.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html",
        "showme": "mirror-modifier",
        "widgets": [
          {
            "type": "showme",
            "id": "mirror-workflow"
          },
          {
            "type": "showme",
            "id": "mirror-origin-mode"
          }
        ]
      },
      {
        "title": "곡면과 두께",
        "copy": "각진 레고 블록에 사포를 대면 모서리가 둥글어지듯이, Subdivision은 표면을 부드럽게 만들어요. Solidify는 색종이를 두꺼운 판지로 바꾸는 거예요.",
        "goal": [
          "Subdivision과 Solidify를 구분해 쓴다",
          "곡면과 두께를 조절한다"
        ],
        "done": [
          "큰 덩어리가 부드러워졌다",
          "패널에 두께가 생겼다"
        ],
        "tasks": [
          {
            "id": "w3-t9",
            "label": "Subdivision Surface 추가하기",
            "detail": "Ctrl+1/2/3으로 레벨 바꿔보기"
          },
          {
            "id": "w3-t10",
            "label": "Shift+E로 날카로운 모서리 남기기",
            "detail": "Edge Crease"
          },
          {
            "id": "w3-t11",
            "label": "Plane에 Solidify로 두께 주기",
            "detail": "Thickness와 Offset 비교"
          }
        ],
        "image": "assets/images/week03/subdivision-surface.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html",
        "showme": [
          "subdivision-surface",
          "solidify-modifier"
        ]
      },
      {
        "title": "반복과 구멍",
        "copy": "복사기로 같은 부품을 줄줄이 찍어내는 게 Array, 쿠키 틀로 반죽에서 모양을 빼내는 게 Boolean이에요. 디테일을 빠르게 늘릴 때 유용해요.",
        "goal": [
          "Array와 Boolean을 구분해 쓴다"
        ],
        "done": [
          "반복 구조가 생겼다",
          "구멍이나 홈이 하나 이상 만들어졌다"
        ],
        "tasks": [
          {
            "id": "w3-t12",
            "label": "Array로 같은 부품 5개 반복하기",
            "detail": "Count와 Offset 바꿔보기"
          },
          {
            "id": "w3-t13",
            "label": "Boolean Difference로 홈 하나 만들기",
            "detail": "커터 오브젝트를 겹치게 두기"
          },
          {
            "id": "w3-t14",
            "label": "Solidify나 Array를 기존 형태에 추가해보기",
            "detail": "반복이나 패널 중 하나 더 실험"
          }
        ],
        "image": "assets/images/week03/array-boolean-detail.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html",
        "showme": [
          "array-modifier",
          "boolean-modifier"
        ],
        "widgets": [
          {
            "type": "showme",
            "id": "curve-to-tube"
          }
        ]
      },
      {
        "title": "마무리 손질",
        "copy": "Ctrl+B가 '이 모서리 하나만 다듬기'라면, Bevel Modifier는 '전체 모서리를 한 번에 정리'예요. Weighted Normal은 형태가 아니라 빛이 닿는 느낌(음영)을 정리해줘요.",
        "goal": [
          "필수 추가 Modifier를 안다"
        ],
        "done": [
          "Bevel Modifier나 Weighted Normal을 확인했다",
          "언제 쓰는지 말할 수 있다"
        ],
        "tasks": [
          {
            "id": "w3-t15",
            "label": "Bevel Modifier로 모서리 둥글게 만들기",
            "detail": "전체적인 하드서피스 느낌 확인"
          },
          {
            "id": "w3-t16",
            "label": "Weighted Normal로 음영 정리하기",
            "detail": "Bevel과 같이 넣으면 차이가 잘 보임"
          },
          {
            "id": "w3-t17",
            "label": "Ctrl+B와 Bevel Modifier 차이 보기",
            "detail": "부분 수정과 전체 정리 흐름 비교"
          }
        ],
        "image": "assets/images/week03/bevel-weighted-normal.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html",
        "showme": "bevel-modifier",
        "widgets": [
          {
            "type": "showme",
            "id": "build-modifier"
          },
          {
            "type": "showme",
            "id": "screw-modifier"
          },
          {
            "type": "showme",
            "id": "scatter-on-surface"
          }
        ]
      },
      {
        "title": "Boolean",
        "copy": "두 오브젝트가 겹치는 부분을 기준으로 자르거나 합쳐요. Difference는 구멍을 뚫고, Union은 합치고, Intersect는 겹치는 부분만 남겨요.",
        "goal": [
          "Boolean Difference로 구멍을 뚫는다"
        ],
        "done": [
          "메쉬에 구멍이나 홈이 만들어졌다"
        ],
        "tasks": [
          {
            "id": "w3-t15-2",
            "label": "커터 오브젝트를 겹치게 두고 Boolean Difference 추가하기",
            "detail": "Solver: Exact 선택"
          },
          {
            "id": "w3-t16-2",
            "label": "커터를 이동해서 구멍 위치 조절하기",
            "detail": "커터가 완전히 관통해야 깔끔하게 잘림"
          }
        ],
        "image": "assets/images/week03/array-boolean-detail.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html",
        "showme": "boolean-modifier",
        "widgets": [
          {
            "type": "showme",
            "id": "wireframe-modifier"
          }
        ]
      },
      {
        "title": "Bevel Modifier",
        "copy": "전체 모서리를 한꺼번에 둥글게 깎아줘요. Ctrl+B가 '모서리 하나씩 수동 다듬기'라면, Bevel Modifier는 '전체 자동 정리'예요.",
        "goal": [
          "Bevel Modifier를 추가하고 Amount/Segments를 조절한다"
        ],
        "done": [
          "전체 모서리가 자연스럽게 둥글어졌다"
        ],
        "tasks": [
          {
            "id": "w3-t17-2",
            "label": "Bevel Modifier 추가하고 Amount와 Segments 조절하기",
            "detail": "Segments가 높을수록 부드러움"
          },
          {
            "id": "w3-t18",
            "label": "Limit Method를 Angle로 바꿔서 날카운 모서리만 적용하기",
            "detail": "30°~60° 사이 실험"
          }
        ],
        "image": "assets/images/week03/bevel-tool.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html",
        "showme": [
          "bevel-modifier",
          "transform-apply"
        ],
        "widgets": [
          {
            "type": "showme",
            "id": "bevel-tool-vs-modifier"
          }
        ]
      },
      {
        "title": "Weighted Normal",
        "copy": "형태는 바꾸지 않고, 빛이 닿는 느낌(음영)만 정리해줘요. Bevel Modifier 바로 아래에 넣으면 하드서피스가 훨씬 깔끔해져요.",
        "goal": [
          "Weighted Normal을 추가해서 음영 차이를 확인한다"
        ],
        "done": [
          "음영이 깔끔하게 정리됐다"
        ],
        "tasks": [
          {
            "id": "w3-t19",
            "label": "Weighted Normal 추가 전/후 음영 비교하기",
            "detail": "Bevel Modifier 아래에 배치"
          },
          {
            "id": "w3-t20",
            "label": "Face Strength Mode 켜보기",
            "detail": "Keep Sharp와 함께 쓰면 효과가 더 잘 보임"
          }
        ],
        "image": "assets/images/week03/weighted-normal.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html",
        "showme": "weighted-normal",
        "widgets": [
          {
            "type": "showme",
            "id": "edge-split-modifier"
          }
        ]
      },
      {
        "title": "Modifier Stack 정리",
        "copy": "Modifier는 위에서 아래로 순서대로 적용돼요. Mirror → Subdivision → Bevel 순서가 바뀌면 결과도 달라져요. Apply는 '되돌릴 수 없는 확정'이라 마지막에만 써요.",
        "goal": [
          "Modifier 순서가 결과에 미치는 영향을 이해한다",
          "Apply 타이밍을 안다"
        ],
        "done": [
          "순서를 바꿨을 때 결과가 달라지는 것을 확인했다",
          "Apply는 마지막에만 하는 이유를 안다"
        ],
        "tasks": [
          {
            "id": "w3-t21",
            "label": "Modifier 순서를 드래그로 바꿔보고 결과 차이 확인하기",
            "detail": "Mirror ↔ Subdivision 위치 교환"
          },
          {
            "id": "w3-t22",
            "label": "Apply 전에 Ctrl+A로 Transform 정리하기",
            "detail": "Scale이 1이 아니면 Modifier 결과가 달라짐"
          }
        ],
        "image": "assets/images/week03/modifier-stack.png",
        "link": "https://docs.blender.org/manual/en/latest/modeling/modifiers/introduction.html",
        "showme": "transform-apply",
        "widgets": [
          {
            "type": "showme",
            "id": "simple-deform"
          },
          {
            "type": "showme",
            "id": "skin-modifier"
          }
        ]
      },
      {
        "title": "Collection",
        "copy": "씬이 복잡해질수록 오브젝트를 묶어서 관리하는 게 중요해요. Collection은 폴더처럼 오브젝트를 그룹으로 정리해서 켜고 끄거나 한꺼번에 선택할 수 있어요.",
        "goal": [
          "Collection을 만들고 오브젝트를 정리한다",
          "Outliner에서 Collection 단위로 숨기고 보이기를 제어한다"
        ],
        "done": [
          "Outliner에 Collection 구조가 정리되어 있다",
          "레퍼런스 이미지와 메쉬가 분리된 Collection에 들어있다"
        ],
        "tasks": [
          {
            "id": "w3-col1",
            "label": "Outliner에서 New Collection 만들기",
            "detail": "우클릭 → New Collection, 또는 M 키로 이동"
          },
          {
            "id": "w3-col2",
            "label": "오브젝트 선택 후 M 키 → Collection으로 이동하기",
            "detail": "레퍼런스 이미지, 로봇 파츠를 별도 Collection으로 분리"
          },
          {
            "id": "w3-col3",
            "label": "Outliner 눈 아이콘으로 Collection 전체 숨기기/보이기",
            "detail": "H 키로 숨기기, Alt+H로 전부 보이기"
          }
        ],
        "sectionTitle": "로봇 모델링 기초"
      },
      {
        "title": "Reference Image 실습",
        "copy": "민트 로봇 레퍼런스 이미지를 뷰포트에 올려서 정면·측면을 각각 배치해요. 영상을 따라하면서 세팅을 완성해요.",
        "goal": [
          "레퍼런스 이미지를 뷰포트에 정확히 정렬한다"
        ],
        "done": [
          "정면·측면 레퍼런스가 각 뷰에 정렬되어 있다",
          "영상 따라 전체 세팅 완료"
        ],
        "tasks": [
          {
            "id": "w3-ref-a",
            "label": "Numpad 1 → Shift+A → Image → Reference로 정면 이미지 추가",
            "detail": "Front View 상태에서 추가해야 정렬됨"
          },
          {
            "id": "w3-ref-b",
            "label": "Numpad 3 → 측면 이미지 추가 후 위치 정렬",
            "detail": "Right View에서 추가"
          },
          {
            "id": "w3-ref-c",
            "label": "N 패널 → Opacity 0.3~0.5로 낮추기",
            "detail": "메쉬와 겹쳐도 작업이 편하도록"
          },
          {
            "id": "w3-ref-d",
            "label": "Outliner에서 선택 잠금 설정",
            "detail": "화살표 아이콘 클릭 → 실수로 이동 방지"
          }
        ],
        "images": [
          "assets/images/week03/robot-ref-front.png",
          "assets/images/week03/robot-ref-side.png",
          "assets/images/week03/robot-ref-back.png"
        ],
        "downloads": [
          {
            "label": "정면 (Front)",
            "url": "assets/images/week03/robot-ref-front.png"
          },
          {
            "label": "측면 (Side)",
            "url": "assets/images/week03/robot-ref-side.png"
          },
          {
            "label": "후면 (Back)",
            "url": "assets/images/week03/robot-ref-back.png"
          }
        ],
        "showme": "image-reference"
      }
    ],
    "shortcuts": [
      {
        "keys": "Tab",
        "action": "Edit Mode 전환"
      },
      {
        "keys": "E",
        "action": "Extrude"
      },
      {
        "keys": "Ctrl + R",
        "action": "Loop Cut"
      },
      {
        "keys": "I",
        "action": "Inset"
      },
      {
        "keys": "Ctrl + B",
        "action": "Bevel"
      },
      {
        "keys": "Ctrl + 1 / 2 / 3",
        "action": "Subdivision 레벨 빠른 변경"
      },
      {
        "keys": "Shift + E",
        "action": "Edge Crease"
      },
      {
        "keys": "Ctrl + A",
        "action": "All Transforms 적용"
      },
      {
        "keys": "P",
        "action": "Separate"
      },
      {
        "keys": "Ctrl + J",
        "action": "Join"
      },
      {
        "keys": "S + X + 0 + Enter",
        "action": "Mirror 중심선 정렬"
      }
    ],
    "explore": [
      {
        "title": "로봇 몸체 만들기",
        "hint": "큐브 → Edit Mode로 기본형 → Mirror → Subdivision으로 부드럽게"
      },
      {
        "title": "패널 구조 만들기",
        "hint": "Plane → Solidify → Boolean으로 홈 추가"
      },
      {
        "title": "반복 파츠 만들기",
        "hint": "Cube 또는 Cylinder → Array로 6~10개 반복"
      },
      {
        "title": "하드서피스 음영 정리",
        "hint": "Bevel Modifier → Weighted Normal 순서로 넣어 차이 비교"
      },
      {
        "title": "형태 휘기 실험",
        "hint": "Simple Deform의 Bend나 Twist로 안테나, 손잡이 같은 형태를 휘어보기"
      },
      {
        "title": "무거운 메쉬 가볍게 만들기",
        "hint": "Decimate로 Polygon 수를 줄였을 때 형태가 얼마나 유지되는지 비교해보기"
      }
    ],
    "assignment": {
      "title": "직접 해볼 수 있는 추가 실험이에요. 정답은 없고, 결과를 캡처해서 공유하면 좋아요.",
      "description": "Edit Mode와 Modifier를 함께 써서 기본형과 디테일이 보이는 형태를 만들어요. 스크린샷 3장 + Modifier 목록 + 한줄 코멘트를 제출해요.",
      "checklist": [
        "Edit Mode 도구 3가지 이상 사용",
        "Modifier 2가지 이상 사용",
        "필수 추가 Modifier 1개 확인",
        "Join/Separate 또는 Apply 타이밍 확인",
        "Modifier 스택이 보이는 스크린샷"
      ]
    },
    "mistakes": [
      "중심선이 벌어짐 → Mirror의 Clipping 확인",
      "너무 둥글어짐 → Subdivision Level 낮추고 Shift+E 써보기",
      "두께나 간격이 이상함 → Ctrl+A로 Scale 먼저 정리",
      "Modifier를 너무 일찍 Apply함 → Apply는 마지막에만",
      "Boolean이 이상함 → 커터가 실제로 겹치는지 확인",
      "음영이 지저분함 → Weighted Normal 추가해보기"
    ],
    "videos": [
      {
        "title": "Blender Studio - Modeling Introduction",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/modeling-introduction/"
      },
      {
        "title": "Blender Studio - Object and Edit Mode",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/object-and-edit-mode/"
      },
      {
        "title": "Blender Studio - Mesh Selection Mode",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/mesh-selection-mode/"
      },
      {
        "title": "Blender Studio - Extrude",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/extrude/"
      },
      {
        "title": "Blender Studio - Loop Cut",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/loop-cut/"
      },
      {
        "title": "Blender Studio - Bevel Tool",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/bevel-tool/"
      }
    ],
    "docs": [
      {
        "title": "Mirror Modifier",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html"
      },
      {
        "title": "Subdivision Surface",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/subdivision_surface.html"
      },
      {
        "title": "Solidify",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/solidify.html"
      },
      {
        "title": "Array",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/array.html"
      },
      {
        "title": "Boolean",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html"
      },
      {
        "title": "Bevel Modifier",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html"
      },
      {
        "title": "Weighted Normal",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html"
      },
      {
        "title": "Simple Deform",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/deform/simple_deform.html"
      },
      {
        "title": "Decimate",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html"
      }
    ],
    "summary": "레고 조립처럼, Edit Mode로 블록을 깎고 Modifier로 대칭·곡면·반복 효과를 얹는 흐름을 배워요."
  },
  {
    "week": 4,
    "status": "done",
    "title": "기초 모델링 2 — 로봇 조립",
    "subtitle": "Bevel · Weighted Normal · Apply",
    "duration": "~3시간",
    "topics": [
      "Inset / Boolean 디테일",
      "Bevel Tool vs Bevel Modifier",
      "Weighted Normal",
      "Join / Separate",
      "Apply Transform vs Modifier Apply"
    ],
    "steps": [
      {
        "title": "Transform 정리와 파츠 관리",
        "copy": "디테일을 넣기 전에 Scale과 파츠 구성을 먼저 정리해요. 수치가 꼬여 있거나 파츠가 뒤섞여 있으면 그다음 작업이 계속 불편해져요.",
        "goal": [
          "Transform을 정리한다",
          "파츠를 분리하거나 합쳐 관리한다"
        ],
        "done": [
          "Scale이 안정적으로 정리됐다",
          "움직일 파츠와 고정 파츠를 구분할 수 있다"
        ],
        "tasks": [
          {
            "id": "w4-t1",
            "label": "N 패널에서 Scale 값 확인",
            "detail": "1,1,1이 아니면 먼저 정리"
          },
          {
            "id": "w4-t2",
            "label": "Ctrl+A로 All Transforms 적용",
            "detail": "Modifier 전에 수치 정리"
          },
          {
            "id": "w4-t3",
            "label": "P로 움직일 파츠 분리하기",
            "detail": "안테나, 헤드셋, 손 파츠 등"
          },
          {
            "id": "w4-t4",
            "label": "Ctrl+J로 함께 갈 파츠 묶기",
            "detail": "고정 파츠끼리 정리"
          }
        ],
        "image": "assets/images/week04/transform-apply.png",
        "showme": "transform-apply"
      },
      {
        "title": "얼굴과 패널 디테일",
        "copy": "큰 덩어리가 잡힌 상태에서 눈, 패널, 관절 라인을 추가하는 단계예요. Inset과 Boolean을 같이 쓰면 디테일을 빠르게 만들 수 있어요.",
        "goal": [
          "Inset과 Boolean으로 디테일을 추가한다"
        ],
        "done": [
          "얼굴이나 가슴판에 디테일이 생겼다",
          "구멍이나 홈이 한 곳 이상 만들어졌다"
        ],
        "tasks": [
          {
            "id": "w4-t5",
            "label": "Inset으로 안쪽 영역 만들기",
            "detail": "눈, 버튼, 패널 라인 시작점"
          },
          {
            "id": "w4-t6",
            "label": "Extrude로 살짝 들어가거나 나오게 만들기",
            "detail": "작은 깊이 차이 주기"
          },
          {
            "id": "w4-t7",
            "label": "Boolean Difference로 홈 또는 소켓 만들기",
            "detail": "커터가 실제로 겹치는지 확인"
          }
        ],
        "image": "assets/images/week04/inset-panel-detail.png",
        "showme": "boolean-modifier"
      },
      {
        "title": "Bevel 두 가지 비교",
        "copy": "같은 '모서리 정리'라도 손으로 직접 깎는 방법과 Modifier로 전체를 정리하는 방법은 다르게 느껴져요. 둘 다 직접 비교해보는 게 가장 빠릅니다.",
        "goal": [
          "Ctrl+B와 Bevel Modifier를 구분해 쓴다"
        ],
        "done": [
          "부분 수정과 전체 정리의 차이를 알게 됐다",
          "모서리 느낌을 더 의도적으로 조절할 수 있다"
        ],
        "tasks": [
          {
            "id": "w4-t8",
            "label": "특정 모서리에 Ctrl+B 써보기",
            "detail": "부분 디테일 직접 다듬기"
          },
          {
            "id": "w4-t9",
            "label": "다른 파츠에는 Bevel Modifier 넣기",
            "detail": "Width와 Segments 비교"
          },
          {
            "id": "w4-t10",
            "label": "두 방식의 결과를 나란히 비교하기",
            "detail": "부분 수정 vs 전체 정리"
          }
        ],
        "image": "assets/images/week04/bevel-modifier.png",
        "showme": "bevel-modifier"
      },
      {
        "title": "Weighted Normal과 음영 정리",
        "copy": "형태는 괜찮은데 표면이 울퉁불퉁해 보일 때가 있어요. 이럴 때 음영을 정리해주는 흐름을 익혀두면 결과물이 훨씬 단정해져요.",
        "goal": [
          "Weighted Normal의 역할을 이해한다"
        ],
        "done": [
          "평평한 외장 면이 더 깔끔하게 보인다",
          "언제 넣는지 설명할 수 있다"
        ],
        "tasks": [
          {
            "id": "w4-t11",
            "label": "Shade Smooth 적용하기",
            "detail": "음영 비교 준비"
          },
          {
            "id": "w4-t12",
            "label": "Bevel Modifier 아래에 Weighted Normal 추가",
            "detail": "순서 포함해서 확인"
          },
          {
            "id": "w4-t13",
            "label": "전후 화면 비교하기",
            "detail": "가슴판, 팔 외장, 다리 파츠에서 확인"
          }
        ],
        "image": "assets/images/week04/weighted-normal.png",
        "showme": "weighted-normal",
        "widgets": [
          {
            "type": "showme",
            "id": "edge-split-modifier"
          }
        ]
      },
      {
        "title": "Apply 시점과 최종 점검",
        "copy": "정리 단계에서 가장 많이 헷갈리는 건 '언제 확정하느냐'예요. 수정 가능성을 남길지, 지금 확정할지를 의식적으로 나눠보면 훨씬 안정적으로 작업할 수 있어요.",
        "goal": [
          "Apply Transform과 Modifier Apply를 구분한다"
        ],
        "done": [
          "언제 Ctrl+A를 쓰는지 안다",
          "Modifier Apply는 마지막에만 하는 흐름을 이해한다"
        ],
        "tasks": [
          {
            "id": "w4-t14",
            "label": "Modifier Stack 순서 다시 보기",
            "detail": "수정 가능 상태 유지"
          },
          {
            "id": "w4-t15",
            "label": "정말 확정할 파츠만 따로 저장 후 Apply 시험",
            "detail": "Apply 전후 수정 차이 느끼기"
          },
          {
            "id": "w4-t16",
            "label": "Transform 또는 Modifier 화면 포함해 스크린샷 저장",
            "detail": "작업 흐름 증거 남기기"
          }
        ],
        "image": "assets/images/week04/array-modifier.png",
        "showme": "join-separate",
        "widgets": [
          {
            "type": "showme",
            "id": "triangulate-modifier"
          },
          {
            "type": "showme",
            "id": "weld-modifier"
          }
        ]
      }
    ],
    "shortcuts": [
      {
        "keys": "Shift + A",
        "action": "Add (Cube, UV Sphere 등)"
      },
      {
        "keys": "Shift + D",
        "action": "Duplicate (복제)"
      },
      {
        "keys": "Shift + S",
        "action": "Snap 메뉴 (Cursor to Selected 등)"
      },
      {
        "keys": "Ctrl + G이동",
        "action": "Snap 이동 (자석 켜진 상태)"
      },
      {
        "keys": "Ctrl + B",
        "action": "Bevel (모서리 직접 다듬기)"
      },
      {
        "keys": "Ctrl + R",
        "action": "Loop Cut (분절 추가)"
      },
      {
        "keys": "P",
        "action": "Separate (파츠 분리)"
      },
      {
        "keys": "Ctrl + J",
        "action": "Join (오브젝트 합치기)"
      },
      {
        "keys": "Ctrl + A",
        "action": "Apply All Transforms"
      },
      {
        "keys": "N",
        "action": "Properties 패널 (Scale 확인)"
      },
      {
        "keys": "H",
        "action": "선택 오브젝트 숨기기"
      },
      {
        "keys": "Alt + H",
        "action": "숨긴 오브젝트 복원"
      },
      {
        "keys": "Ctrl + Z",
        "action": "되돌리기"
      }
    ],
    "explore": [
      {
        "title": "얼굴 패널 디테일",
        "hint": "Inset → Extrude 또는 Boolean으로 눈/패널 라인 만들기"
      },
      {
        "title": "관절 음영 정리",
        "hint": "Bevel Modifier → Weighted Normal로 팔/다리 파츠 음영 비교"
      },
      {
        "title": "파츠 관리 정리",
        "hint": "헤드셋, 안테나, 손 파츠를 분리/합치며 구조 정리"
      },
      {
        "title": "Apply 타이밍 비교",
        "hint": "같은 파일을 복제해 Apply 전과 후의 수정 난이도 비교"
      }
    ],
    "assignment": {
      "title": "로봇 디테일 정리",
      "description": "Week 03 기본형에 디테일과 음영 정리를 더한 결과물을 제출하세요.",
      "checklist": [
        "디테일 1곳 이상 추가",
        "Bevel 계열 1회 이상 사용",
        "Weighted Normal 확인",
        "Modifier Stack 또는 Transform 확인 스크린샷"
      ]
    },
    "mistakes": [
      "Bevel이 너무 큼 → Width를 아주 작게 시작",
      "Weighted Normal 차이가 안 보임 → Bevel과 Shade Smooth 전후 비교",
      "Boolean이 지저분함 → 커터가 실제로 겹치는지 다시 확인",
      "Modifier를 너무 일찍 Apply함 → 마지막에만 확정",
      "파츠 관리가 헷갈림 → 움직일 파츠는 분리, 고정 파츠는 정리해서 묶기"
    ],
    "videos": [
      {
        "title": "Blender Studio - Modifiers",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/modifiers/"
      }
    ],
    "docs": [
      {
        "title": "Bevel Tool",
        "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/tools/bevel.html"
      },
      {
        "title": "Bevel Modifier",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/bevel.html"
      },
      {
        "title": "Weighted Normal",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/modify/weighted_normal.html"
      },
      {
        "title": "Boolean",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/booleans.html"
      }
    ],
    "summary": "지난 주 배운 흐름을 바탕으로 디테일 추가와 음영 정리를 더 안정적으로 반복합니다."
  },
  {
    "week": 5,
    "status": "done",
    "title": "AI 3D 생성 + Sculpting",
    "subtitle": "AI 툴 활용 · Sculpt Mode 기초 · 메쉬 정리",
    "duration": "~3시간",
    "topics": [
      "AI 3D 생성 툴 (Meshy/Tripo)",
      "AI 메쉬 Import 및 정리",
      "Sculpt Mode 기초 브러시",
      "Sculpt 브러시 심화 (Clay/Crease/Inflate)",
      "Remesh와 Dyntopo",
      "AI + Sculpt 하이브리드 워크플로우"
    ],
    "steps": [
      {
        "title": "AI 3D 생성 체험",
        "copy": "텍스트 몇 글자 입력하면 3D 메쉬가 뚝딱 나와요. AI가 초벌을 해주면 우리는 거기서 다듬기만 하면 돼요. 점토 조각으로 치면 AI가 큰 덩어리를 잡아준 셈이에요.",
        "goal": [
          "AI 생성 워크플로우를 이해한다",
          "프롬프트 작성 요령을 안다"
        ],
        "done": [
          "AI 생성 메쉬를 Blender에서 열었다",
          "최소 2가지 프롬프트로 결과를 비교했다"
        ],
        "tasks": [
          {
            "id": "w5-t1",
            "label": "Meshy 또는 Tripo에서 프롬프트 입력 후 생성",
            "detail": "구체적인 형용사를 넣을수록 결과가 좋아요"
          },
          {
            "id": "w5-t2",
            "label": "다른 프롬프트로 한 번 더 생성해서 비교",
            "detail": "같은 주제라도 문장에 따라 결과가 달라요"
          },
          {
            "id": "w5-t3",
            "label": ".glb 파일 Blender에서 Import",
            "detail": "File → Import → glTF (.glb/.gltf)"
          }
        ],
        "image": "assets/images/week05/ai-3d-generation.png"
      },
      {
        "title": "AI 메쉬 정리",
        "copy": "AI가 만든 메쉬는 대부분 폴리곤이 지나치게 많아요. 마치 해상도가 너무 높은 사진처럼요. Decimate로 적당히 줄여야 이후 작업이 편해져요.",
        "goal": [
          "AI 메쉬의 폴리곤 문제를 이해한다",
          "Decimate로 메쉬를 정리한다"
        ],
        "done": [
          "폴리곤 수가 절반 이하로 줄었다",
          "형태가 크게 무너지지 않았다"
        ],
        "tasks": [
          {
            "id": "w5-t4",
            "label": "Viewport Overlay에서 폴리곤 수 확인",
            "detail": "Statistics 켜기"
          },
          {
            "id": "w5-t5",
            "label": "Decimate Modifier 추가 후 Ratio 조절",
            "detail": "0.3~0.5 정도에서 형태 유지되는 지점 찾기"
          },
          {
            "id": "w5-t6",
            "label": "Ctrl+A로 Scale 정리 후 원점 확인",
            "detail": "Import 메쉬는 크기가 제각각이에요"
          }
        ],
        "image": "assets/images/week05/mesh-cleanup.png",
        "showme": "decimate-modifier",
        "widgets": [
          {
            "type": "showme",
            "id": "mask-modifier"
          }
        ]
      },
      {
        "title": "Sculpt Mode 기초",
        "copy": "브러시로 메쉬를 직접 주무르는 모드예요. 마우스로 칠하듯이 형태를 만들어요. 점토 조각과 가장 비슷한 방식이에요.",
        "goal": [
          "Sculpt Mode 진입 방법을 안다",
          "기본 3대 브러시를 쓴다"
        ],
        "done": [
          "Draw로 볼록하게, Grab으로 끌어당기고, Smooth로 정리했다"
        ],
        "tasks": [
          {
            "id": "w5-t7",
            "label": "Ctrl+Tab으로 Sculpt Mode 전환",
            "detail": ""
          },
          {
            "id": "w5-t8",
            "label": "F로 브러시 크기, Shift+F로 강도 조절",
            "detail": "큰 브러시로 시작해서 점점 줄이기"
          },
          {
            "id": "w5-t9",
            "label": "Draw 브러시로 표면 올려보기",
            "detail": "Ctrl 누르면 반대로 파내기"
          },
          {
            "id": "w5-t10",
            "label": "Grab 브러시로 형태 잡아 끌어보기",
            "detail": "큰 덩어리 잡을 때 유용해요"
          },
          {
            "id": "w5-t11",
            "label": "Smooth 브러시로 울퉁불퉁한 곳 정리",
            "detail": "Shift 누른 채로도 임시 Smooth"
          }
        ],
        "image": "assets/images/week05/sculpt-mode.png",
        "showme": "sculpt-basics"
      },
      {
        "title": "Sculpt 브러시 심화",
        "copy": "기본 3개로 큰 흐름을 잡았으면, 이제 세부 표현용 브러시를 익혀요. Clay는 점토를 덧붙이는 느낌, Crease는 주름이나 홈을 파는 느낌이에요.",
        "goal": [
          "용도별 브러시를 구분해 쓴다"
        ],
        "done": [
          "Clay/Crease/Inflate 중 2가지 이상 써봤다"
        ],
        "tasks": [
          {
            "id": "w5-t12",
            "label": "Clay Strips로 점토 덧붙이듯 형태 쌓기",
            "detail": "넓은 면 위에 층층이 쌓기"
          },
          {
            "id": "w5-t13",
            "label": "Crease로 홈이나 주름 선 파기",
            "detail": "관절, 눈, 입 라인에 활용"
          },
          {
            "id": "w5-t14",
            "label": "Inflate로 볼록하게 부풀려보기",
            "detail": "볼이나 근육 강조에 유용"
          }
        ],
        "image": "assets/images/week05/sculpt-brushes.png"
      },
      {
        "title": "Remesh와 마무리",
        "copy": "Sculpt를 하다 보면 메쉬가 늘어나서 찌그러지는 곳이 생겨요. Remesh는 메쉬를 다시 고르게 나눠주는 리셋 버튼 같은 거예요.",
        "goal": [
          "Remesh의 역할을 이해한다",
          "AI 초안 + Sculpt 마무리 흐름을 완성한다"
        ],
        "done": [
          "Remesh 후 메쉬가 고르게 정리됐다",
          "AI + Sculpt 결과물 스크린샷을 저장했다"
        ],
        "tasks": [
          {
            "id": "w5-t15",
            "label": "Sculpt Mode → Remesh 버튼 또는 Ctrl+R",
            "detail": "Voxel Size를 조절해서 해상도 맞추기"
          },
          {
            "id": "w5-t16",
            "label": "Remesh 전후 비교해보기",
            "detail": "메쉬가 고르게 나뉘었는지 확인"
          },
          {
            "id": "w5-t17",
            "label": "최종 형태 Object Mode에서 확인 후 스크린샷",
            "detail": ""
          }
        ],
        "image": "assets/images/week05/remesh.png",
        "showme": "remesh-modifier",
        "widgets": [
          {
            "type": "showme",
            "id": "multiresolution-modifier"
          }
        ]
      }
    ],
    "shortcuts": [
      {
        "keys": "Ctrl + Tab",
        "action": "Sculpt Mode 전환"
      },
      {
        "keys": "F",
        "action": "브러시 크기 조절"
      },
      {
        "keys": "Shift + F",
        "action": "브러시 강도 조절"
      },
      {
        "keys": "Ctrl (hold)",
        "action": "브러시 반전 (파내기)"
      },
      {
        "keys": "Shift (hold)",
        "action": "Smooth 임시 전환"
      },
      {
        "keys": "Ctrl + R (Sculpt)",
        "action": "Voxel Remesh"
      },
      {
        "keys": "Ctrl + Z",
        "action": "되돌리기"
      },
      {
        "keys": "X",
        "action": "Draw 브러시 빠른 선택"
      }
    ],
    "explore": [
      {
        "title": "AI 프롬프트 실험",
        "hint": "같은 로봇을 5가지 다른 스타일로 생성해서 비교해보기"
      },
      {
        "title": "유기적 형태 Sculpt",
        "hint": "Sphere에서 시작해서 동물이나 캐릭터 얼굴을 Sculpt로만 만들어보기"
      },
      {
        "title": "Dyntopo 체험",
        "hint": "Sculpt Mode → Dyntopo 켜고 디테일이 자동으로 늘어나는지 확인"
      },
      {
        "title": "AI + Edit Mode 하이브리드",
        "hint": "AI 메쉬를 Sculpt 대신 Edit Mode로 정리해서 하드서피스 느낌 만들기"
      }
    ],
    "assignment": {
      "title": "AI + 수동 하이브리드 오브젝트",
      "description": "AI 생성 메쉬를 Sculpt로 다듬은 결과물을 제출해요. 원본과 수정 후를 비교할 수 있어야 해요.",
      "checklist": [
        "AI 생성 원본과 Sculpt 수정 후 비교 이미지",
        "AI 생성 → Sculpt 수정 흔적 있는 .blend",
        "사용한 브러시 3가지 이상 적기",
        "완성 렌더 이미지 2장 이상"
      ]
    },
    "mistakes": [
      "AI 메쉬 폴리곤이 너무 많음 → Decimate Modifier로 줄이기",
      "Sculpt가 먹히지 않음 → 폴리곤이 너무 적으면 Remesh로 늘리기",
      "브러시가 반대로 작동함 → Ctrl을 누르고 있으면 반전이에요. 떼세요",
      "형태가 너무 울퉁불퉁 → Smooth 브러시로 정리, 또는 Strength 낮추기",
      "Import 메쉬가 너무 작거나 큼 → S로 크기 맞추고 Ctrl+A로 Scale 적용"
    ],
    "videos": [
      {
        "title": "Blender Studio - Introduction to Sculpting",
        "url": "https://studio.blender.org/training/sculpting-in-blender/introduction/"
      }
    ],
    "docs": [
      {
        "title": "Sculpt Mode",
        "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/index.html"
      },
      {
        "title": "Sculpt Brushes",
        "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tools/index.html"
      },
      {
        "title": "Remesh",
        "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/tool_settings/remesh.html"
      },
      {
        "title": "Decimate Modifier",
        "url": "https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/decimate.html"
      }
    ],
    "summary": "AI 기반 3D 생성 툴을 경험하고, Sculpt Mode로 유기적인 형태를 만들어요."
  },
  {
    "week": 6,
    "status": "done",
    "title": "Material & Shader Node",
    "subtitle": "재질 시스템 · Principled BSDF · 노드 편집",
    "duration": "~3시간",
    "topics": [
      "Material 슬롯 구조",
      "Principled BSDF 핵심 파라미터",
      "Shader Node Editor 기초",
      "Color Ramp / Texture 노드",
      "파츠별 Material 분리",
      "Viewport Shading 모드"
    ],
    "steps": [
      {
        "title": "Material 할당",
        "copy": "옷을 입히듯 오브젝트에 재질을 입혀요. 같은 로봇이라도 재질 하나로 장난감이 될 수도, 군용 장비가 될 수도 있어요.",
        "goal": [
          "Material 슬롯의 구조를 안다",
          "하나의 오브젝트에 여러 Material을 쓸 수 있다"
        ],
        "done": [
          "오브젝트 색이 바뀌었다",
          "한 오브젝트에 2가지 이상 Material을 할당했다"
        ],
        "tasks": [
          {
            "id": "w6-t1",
            "label": "Material Properties에서 + New 클릭",
            "detail": "기본 Principled BSDF가 자동 생성돼요"
          },
          {
            "id": "w6-t2",
            "label": "Base Color 바꿔서 색 변경 확인",
            "detail": "Z → Material Preview로 확인"
          },
          {
            "id": "w6-t3",
            "label": "Edit Mode에서 면 선택 → 두 번째 Material Assign",
            "detail": "눈이나 가슴판에 다른 색 입히기"
          }
        ],
        "image": "assets/images/week06/material-assign.png",
        "showme": "material-basics"
      },
      {
        "title": "Principled BSDF 탐색",
        "copy": "숫자 하나로 금속/유리/플라스틱이 바뀌어요. Metallic을 1로 올리면 금속, Transmission을 1로 올리면 유리처럼 보여요. 옷감을 고르듯 슬라이더를 움직여보세요.",
        "goal": [
          "핵심 파라미터 4가지를 구분한다",
          "원하는 재질을 슬라이더로 만든다"
        ],
        "done": [
          "금속/유리/플라스틱 재질을 각각 흉내냈다",
          "Roughness 차이를 눈으로 구분할 수 있다"
        ],
        "tasks": [
          {
            "id": "w6-t4",
            "label": "Metallic 1.0으로 금속 재질 만들기",
            "detail": "Roughness도 같이 바꿔서 광택 비교"
          },
          {
            "id": "w6-t5",
            "label": "Transmission 1.0으로 유리 재질 만들기",
            "detail": "IOR 1.45 정도면 유리 느낌"
          },
          {
            "id": "w6-t6",
            "label": "Roughness 0 vs 0.5 vs 1 비교",
            "detail": "반짝 → 은은 → 무광 변화 확인"
          },
          {
            "id": "w6-t7",
            "label": "Emission으로 발광 재질 만들기",
            "detail": "로봇 눈이나 표시등에 활용"
          }
        ],
        "image": "assets/images/week06/principled-bsdf.png",
        "showme": "principled-bsdf"
      },
      {
        "title": "Shader Node Editor",
        "copy": "노드는 레고 블록처럼 연결해서 재질을 만들어요. 색을 그라데이션으로 바꾸거나 질감을 섞을 수 있어요. 선을 연결하는 것만으로 복잡한 재질이 가능해져요.",
        "goal": [
          "노드 기반 재질 편집 방식을 이해한다",
          "Color Ramp 노드를 연결한다"
        ],
        "done": [
          "ColorRamp를 Principled BSDF에 연결했다",
          "노드 2개 이상을 직접 연결했다"
        ],
        "tasks": [
          {
            "id": "w6-t8",
            "label": "Shader Editor 열기",
            "detail": "상단 에디터 타입 메뉴 또는 워크스페이스 Shading 탭"
          },
          {
            "id": "w6-t9",
            "label": "Shift+A → Color → Color Ramp 추가",
            "detail": ""
          },
          {
            "id": "w6-t10",
            "label": "Color Ramp 출력 → Base Color 입력 연결",
            "detail": "드래그로 소켓 연결"
          },
          {
            "id": "w6-t11",
            "label": "Color Ramp 색상 두 개 바꿔서 그라데이션 만들기",
            "detail": "색 포인트 클릭 후 변경"
          }
        ],
        "image": "assets/images/week06/shader-editor.png",
        "showme": "shader-editor"
      },
      {
        "title": "Texture 노드로 질감 추가",
        "copy": "Noise Texture를 연결하면 표면에 얼룩이나 먼지 같은 질감이 생겨요. 실제 물건은 완전히 깨끗한 법이 없으니까, 이 한 단계가 리얼함을 크게 올려줘요.",
        "goal": [
          "Noise/Musgrave 등 텍스처 노드를 연결한다"
        ],
        "done": [
          "표면에 패턴이나 질감이 보인다"
        ],
        "tasks": [
          {
            "id": "w6-t12",
            "label": "Shift+A → Texture → Noise Texture 추가",
            "detail": ""
          },
          {
            "id": "w6-t13",
            "label": "Noise → Color Ramp → Base Color 연결",
            "detail": "Scale을 바꿔서 패턴 크기 조절"
          },
          {
            "id": "w6-t14",
            "label": "Noise의 Roughness 출력을 Principled BSDF Roughness에 연결",
            "detail": "표면 광택에 변화를 줘요"
          }
        ],
        "image": "assets/images/week06/texture-node.png"
      },
      {
        "title": "Viewport Shading 비교",
        "copy": "Z 키 하나로 와이어프레임/솔리드/미리보기/렌더를 오가요. 작업 중에는 Material Preview로, 최종 확인은 Rendered로 보는 습관을 들이면 편해요.",
        "goal": [
          "4가지 Shading 모드를 구분한다"
        ],
        "done": [
          "Z 파이 메뉴로 모드 전환이 자연스럽다"
        ],
        "tasks": [
          {
            "id": "w6-t15",
            "label": "Z 파이 메뉴로 4가지 모드 각각 전환",
            "detail": "Wireframe/Solid/Material/Rendered"
          },
          {
            "id": "w6-t16",
            "label": "Material Preview에서 작업 후 Rendered에서 최종 확인",
            "detail": "빛 반사가 다르게 보여요"
          }
        ],
        "image": "assets/images/week06/shading-modes.png"
      }
    ],
    "shortcuts": [
      {
        "keys": "Z",
        "action": "Shading 모드 전환 파이 메뉴"
      },
      {
        "keys": "Shift + A",
        "action": "Shader Editor 노드 추가"
      },
      {
        "keys": "Ctrl + Shift + Click",
        "action": "Viewer Node 연결"
      },
      {
        "keys": "Ctrl + T",
        "action": "Texture Mapping 자동 연결"
      },
      {
        "keys": "M",
        "action": "Frame 그룹 만들기"
      },
      {
        "keys": "H",
        "action": "노드 숨기기/접기"
      },
      {
        "keys": "Ctrl + Right Click",
        "action": "노드 연결선 끊기"
      }
    ],
    "explore": [
      {
        "title": "로봇 파츠별 재질 입히기",
        "hint": "몸통은 무광 플라스틱, 관절은 금속, 눈은 발광으로 나눠서 입히기"
      },
      {
        "title": "Mix Shader 실험",
        "hint": "금속과 플라스틱을 Mix Shader로 섞어 반반짜리 재질 만들기"
      },
      {
        "title": "Noise로 녹슨 느낌 만들기",
        "hint": "Noise Texture + Color Ramp로 깨끗한 금속과 녹슨 부분 분리"
      },
      {
        "title": "투명 재질 실험",
        "hint": "Alpha 값을 조절해서 반투명 바이저 만들기 (Settings → Blend Mode)"
      }
    ],
    "assignment": {
      "title": "재질 스타일 샘플러",
      "description": "5가지 다른 재질로 구 5개를 만들어 나란히 배치하고 렌더해요. 금속/유리/플라스틱/발광/질감 각 1개씩.",
      "checklist": [
        "5가지 재질 구 렌더 이미지",
        "각 재질의 핵심 파라미터 값 메모",
        "Shader Editor 노드 연결 스크린샷 1장",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "재질이 화면에서 안 보임 → Viewport Shading을 Material Preview 또는 Rendered로 변경",
      "노드 연결이 안 됨 → 소켓 색이 같은 것끼리 연결 (노란색끼리, 보라색끼리)",
      "Emission이 안 빛남 → Rendered 모드에서만 보여요. Material Preview에선 약하게 보임",
      "유리가 검게 보임 → 주변에 반사할 환경이 없으면 유리가 어두워요. HDRI 추가하면 해결",
      "여러 Material 할당이 안 됨 → Edit Mode에서 면을 선택한 뒤 Assign 버튼"
    ],
    "videos": [
      {
        "title": "Blender Studio - Materials and Shading",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/materials-and-shading/"
      }
    ],
    "docs": [
      {
        "title": "Materials",
        "url": "https://docs.blender.org/manual/en/latest/render/materials/introduction.html"
      },
      {
        "title": "Principled BSDF",
        "url": "https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html"
      },
      {
        "title": "Shader Editor",
        "url": "https://docs.blender.org/manual/en/latest/editors/shader_editor.html"
      },
      {
        "title": "Texture Nodes",
        "url": "https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/index.html"
      },
      {
        "title": "Color Ramp",
        "url": "https://docs.blender.org/manual/en/latest/render/shader_nodes/converter/color_ramp.html"
      }
    ],
    "summary": "Material의 원리와 Shader Editor를 이해하고 Principled BSDF로 다양한 재질을 표현해요."
  },
  {
    "week": 7,
    "status": "done",
    "title": "UV Unwrapping + AI Texture",
    "subtitle": "UV 펼치기 · 텍스처 매핑 · AI 이미지 활용",
    "duration": "~3시간",
    "topics": [
      "UV 개념과 필요성",
      "Seam 설정 전략",
      "Unwrap + UV Editor",
      "UV 섬 정리와 배치",
      "AI Texture 생성 및 적용",
      "Texture Painting 맛보기"
    ],
    "steps": [
      {
        "title": "UV 개념 이해",
        "copy": "옷을 만들려면 원단을 재단하잖아요. UV도 마찬가지예요. 3D 표면을 2D로 펼쳐야 이미지를 정확하게 붙일 수 있어요. Seam은 가위로 자르는 선이에요.",
        "goal": [
          "UV가 왜 필요한지 이해한다",
          "Seam의 역할을 안다"
        ],
        "done": [
          "빨간 Seam 선이 표시됐다",
          "Seam 위치를 의도적으로 정할 수 있다"
        ],
        "tasks": [
          {
            "id": "w7-t1",
            "label": "Edit Mode → Edge Select 모드(3) 전환",
            "detail": ""
          },
          {
            "id": "w7-t2",
            "label": "큐브의 모서리를 선택해서 Ctrl+E → Mark Seam",
            "detail": "빨간 선이 보이면 성공"
          },
          {
            "id": "w7-t3",
            "label": "잘못 표시한 Seam을 Ctrl+E → Clear Seam으로 지우기",
            "detail": ""
          }
        ],
        "image": "assets/images/week07/uv-seam.png",
        "showme": "uv-unwrapping"
      },
      {
        "title": "Unwrap & UV Editor",
        "copy": "Seam을 그은 경계선대로 메쉬가 펼쳐져서 UV Editor에 2D로 나와요. 종이 상자를 펼친 것처럼 생겼어요. 여기 보이는 모양대로 이미지가 입혀져요.",
        "goal": [
          "UV가 어떻게 펼쳐지는지 이해한다",
          "UV Editor에서 섬을 조작한다"
        ],
        "done": [
          "UV Editor에서 메쉬가 2D로 보인다",
          "UV 섬의 크기와 위치를 조절했다"
        ],
        "tasks": [
          {
            "id": "w7-t4",
            "label": "전체 선택(A) 후 U → Unwrap 실행",
            "detail": ""
          },
          {
            "id": "w7-t5",
            "label": "UV Editor 열어서 펼쳐진 결과 확인",
            "detail": "화면 분할 또는 워크스페이스 UV Editing"
          },
          {
            "id": "w7-t6",
            "label": "L로 UV Island 개별 선택 후 G/S/R로 이동/크기/회전",
            "detail": ""
          },
          {
            "id": "w7-t7",
            "label": "겹치는 UV 섬이 없는지 확인",
            "detail": "겹치면 텍스처가 이상하게 보여요"
          }
        ],
        "image": "assets/images/week07/uv-editor.png",
        "showme": "uv-editor"
      },
      {
        "title": "Smart UV Project로 빠른 펼침",
        "copy": "Seam을 하나하나 그리기 귀찮을 때가 있어요. Smart UV Project는 자동으로 적당히 잘라서 펼쳐줘요. 정밀하진 않지만 초안으로 충분해요.",
        "goal": [
          "수동 Unwrap과 자동 Unwrap을 비교한다"
        ],
        "done": [
          "Smart UV Project로 빠르게 UV를 만들었다"
        ],
        "tasks": [
          {
            "id": "w7-t8",
            "label": "전체 선택 후 U → Smart UV Project 실행",
            "detail": "Angle Limit 66° 정도가 기본값"
          },
          {
            "id": "w7-t9",
            "label": "수동 Unwrap 결과와 나란히 비교해보기",
            "detail": "어떤 게 더 깔끔한지 확인"
          }
        ],
        "image": "assets/images/week07/smart-uv.png"
      },
      {
        "title": "AI Texture 생성 및 적용",
        "copy": "AI가 만든 이미지를 메쉬 표면에 붙이는 거예요. UV가 제대로 펼쳐져 있어야 이미지가 자연스럽게 입혀져요. 재단이 잘 된 옷감 위에 프린트하는 것과 같아요.",
        "goal": [
          "Image Texture 노드 사용법을 안다",
          "AI 생성 이미지를 재질에 연결한다"
        ],
        "done": [
          "메쉬에 텍스처가 자연스럽게 입혀졌다"
        ],
        "tasks": [
          {
            "id": "w7-t10",
            "label": "AI 텍스처 이미지 파일 저장",
            "detail": "Adobe Firefly, Stable Diffusion 등"
          },
          {
            "id": "w7-t11",
            "label": "Shader Editor → Shift+A → Image Texture 노드 추가",
            "detail": ""
          },
          {
            "id": "w7-t12",
            "label": "Open으로 이미지 불러와서 Base Color에 연결",
            "detail": ""
          },
          {
            "id": "w7-t13",
            "label": "Material Preview에서 결과 확인",
            "detail": "텍스처가 늘어나면 UV를 다시 조정"
          }
        ],
        "image": "assets/images/week07/ai-texture.png"
      },
      {
        "title": "Texture Painting 맛보기",
        "copy": "UV가 펼쳐진 위에 직접 색을 칠할 수도 있어요. 3D 뷰에서 바로 칠하면 UV 위치가 자동으로 맞아서 편해요.",
        "goal": [
          "Texture Paint 모드의 존재를 안다"
        ],
        "done": [
          "3D 뷰에서 직접 색을 칠해봤다"
        ],
        "tasks": [
          {
            "id": "w7-t14",
            "label": "Image Editor에서 New → 빈 이미지 생성 (1024×1024)",
            "detail": "Base Color 노드에 연결"
          },
          {
            "id": "w7-t15",
            "label": "Texture Paint 모드로 전환해서 표면에 직접 색 칠하기",
            "detail": "브러시 색과 크기 바꿔가며 실험"
          }
        ],
        "image": "assets/images/week07/texture-paint.png"
      }
    ],
    "shortcuts": [
      {
        "keys": "Ctrl + E → Mark Seam",
        "action": "Seam 설정 (빨간 선)"
      },
      {
        "keys": "Ctrl + E → Clear Seam",
        "action": "Seam 제거"
      },
      {
        "keys": "U → Unwrap",
        "action": "수동 UV 전개"
      },
      {
        "keys": "U → Smart UV Project",
        "action": "자동 UV 전개"
      },
      {
        "keys": "U → Cube Projection",
        "action": "육면체 투영"
      },
      {
        "keys": "U → Cylinder Projection",
        "action": "원기둥 투영"
      },
      {
        "keys": "U → Sphere Projection",
        "action": "구형 투영"
      },
      {
        "keys": "G / R / S",
        "action": "UV Island 이동/회전/스케일"
      },
      {
        "keys": "A",
        "action": "전체 선택"
      },
      {
        "keys": "L",
        "action": "UV Island 개별 선택"
      },
      {
        "keys": "P",
        "action": "UV Pin 고정"
      },
      {
        "keys": "S + X/Y + 0",
        "action": "UV Island 정렬"
      },
      {
        "keys": "UV > Pack Islands",
        "action": "Island 자동 정리"
      },
      {
        "keys": "F",
        "action": "브러시 크기 조절"
      },
      {
        "keys": "Shift + F",
        "action": "브러시 강도 조절"
      },
      {
        "keys": "Tab",
        "action": "Object ↔ Edit Mode"
      },
      {
        "keys": "2",
        "action": "Edge 선택 모드 (Seam 작업)"
      },
      {
        "keys": "3",
        "action": "Face 선택 모드 (Assign 작업)"
      },
      {
        "keys": "Z",
        "action": "Shading 모드 전환"
      }
    ],
    "explore": [
      {
        "title": "로봇 전체 UV 펼치기",
        "hint": "로봇 몸통/팔/다리 각각 Seam을 넣고 한 번에 Unwrap해서 전체 UV 레이아웃 만들기"
      },
      {
        "title": "AI 텍스처 스타일 비교",
        "hint": "같은 메쉬에 3가지 다른 AI 텍스처를 입혀서 분위기 차이 비교"
      },
      {
        "title": "Texture Painting으로 데칼 추가",
        "hint": "로봇 가슴판이나 어깨에 로고나 번호를 직접 페인팅"
      },
      {
        "title": "Normal Map 체험",
        "hint": "AI로 생성한 Normal Map을 연결해서 표면에 가짜 요철 만들기"
      }
    ],
    "assignment": {
      "title": "텍스처 입힌 소품",
      "description": "Seam → Unwrap → AI Texture 순서로 텍스처를 입힌 소품을 제출해요. UV Editor 스크린샷도 함께.",
      "checklist": [
        "렌더 이미지 2장 이상",
        "UV Editor 스크린샷 1장",
        "한줄 코멘트",
        "필요하면 AI 텍스처 이미지 또는 Texture Paint 결과 함께 정리"
      ]
    },
    "mistakes": [
      "UV 맵을 확인하고 필요한 경우 UV 아일랜드의 크기를 조정합니다.",
      "오브젝트 스케일이 적용되었는지 확인합니다.",
      "심을 더 잘 보이지 않는 곳에 배치합니다.",
      "타일링 가능한 텍스처를 사용합니다.",
      "UV 아일랜드 간의 마진을 조정합니다.",
      "모델에 적절한 심을 추가합니다.",
      "또는 'Smart UV Project'와 같은 자동 언래핑 방법을 사용합니다.",
      "UV 아일랜드의 크기와 위치를 최적화합니다.",
      "'Pack Islands' 기능을 사용하여 자동으로 아일랜드를 재배치합니다.",
      "참고영상",
      "Unwrapping UVs addon",
      "mio3 addon :https://extensions.blender.org/add-ons/mio3-uv/",
      "텍스쳐가 늘어남 → Seam 위치를 조정하거나 UV 섬 크기를 맞춰 재언래핑",
      "텍스쳐가 뒤집혀 보임 → UV Editor에서 해당 섬 선택 후 S → Y → -1",
      "텍스쳐 연결이 안 됨 → UV Map 이름이 Material과 동일한지 확인"
    ],
    "videos": [
      {
        "title": "Blender Studio - UV Unwrapping",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/uv-unwrapping/"
      }
    ],
    "docs": [
      {
        "title": "UV Unwrapping",
        "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/index.html"
      },
      {
        "title": "UV Editor",
        "url": "https://docs.blender.org/manual/en/latest/editors/uv/introduction.html"
      },
      {
        "title": "Image Texture Node",
        "url": "https://docs.blender.org/manual/en/latest/render/shader_nodes/textures/image.html"
      },
      {
        "title": "Texture Painting",
        "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/texture_paint/index.html"
      }
    ],
    "summary": "UV Unwrapping으로 메쉬를 펼치고 AI 텍스처 이미지를 입혀요. 옷감 재단하듯 3D 표면을 2D로 펼치는 원리예요."
  },
  {
    "week": 8,
    "status": "done",
    "title": "중간고사",
    "subtitle": "지금까지 배운 것을 담은 작품 발표",
    "duration": "수업 전체 발표",
    "topics": [
      "3D 모델 완성",
      "Material/Texture 적용",
      "발표 준비"
    ],
    "steps": [
      {
        "title": "프로젝트 마무리",
        "copy": "발표 전날까지 렌더 이미지와 .blend 파일을 완성합니다.",
        "goal": [
          "발표 자료 완성"
        ],
        "done": [
          "렌더 이미지 3장 이상",
          ".blend 파일 깔끔하게 정리"
        ],
        "tasks": [
          {
            "id": "w8-t1",
            "label": "F12로 최종 렌더 이미지 3장 저장",
            "detail": ""
          },
          {
            "id": "w8-t2",
            "label": "발표 슬라이드 (선택사항) 준비",
            "detail": ""
          },
          {
            "id": "w8-t3",
            "label": ".blend 파일 이름 정리 후 제출 폴더에 넣기",
            "detail": ""
          }
        ]
      }
    ],
    "shortcuts": [],
    "explore": [],
    "assignment": {
      "title": "중간 프로젝트 발표",
      "description": "3D 모델 + 재질 + 본인만의 컨셉이 담긴 작품을 발표합니다. 3분 내외.",
      "checklist": [
        "렌더 이미지 3장 이상",
        ".blend 파일 1개",
        "사용한 기능 설명 (2~3가지)"
      ]
    },
    "mistakes": [],
    "videos": [],
    "docs": [
      {
        "title": "Blender Manual: Rendering",
        "url": "https://docs.blender.org/manual/en/latest/render/index.html"
      },
      {
        "title": "Blender 단축키 모음",
        "url": "../../resources/blender-shortcuts.md"
      }
    ],
    "summary": "Week 01~07에서 배운 모델링·재질·텍스처를 활용한 개인 프로젝트를 발표합니다."
  },
  {
    "week": 9,
    "status": "active",
    "title": "Lighting 기초 + MCP 설치",
    "subtitle": "빛의 종류 · HDRI · 3점 조명 · 카메라",
    "duration": "~3시간",
    "topics": [
      "Light 오브젝트 4종류",
      "HDRI 환경 조명",
      "3점 조명법",
      "카메라 세팅",
      "조명 색온도와 분위기",
      "배경 설정"
    ],
    "steps": [
      {
        "title": "Light 종류 탐색",
        "copy": "사진관에서 조명을 세팅하듯, 어떤 조명을 쓰냐에 따라 분위기가 완전히 달라져요. 같은 로봇이라도 조명만 바꾸면 다른 작품처럼 보여요.",
        "goal": [
          "4가지 Light 타입의 특성을 안다",
          "Energy와 Color를 조절한다"
        ],
        "done": [
          "4가지 Light를 각각 추가해서 차이를 느꼈다",
          "조명 색을 바꿔봤다"
        ],
        "tasks": [
          {
            "id": "w9-t1",
            "label": "Shift+A → Light → Point Light 추가",
            "detail": "전구처럼 모든 방향으로 빛"
          },
          {
            "id": "w9-t2",
            "label": "Sun Light로 전환해서 비교",
            "detail": "태양처럼 평행한 빛, 위치 무관"
          },
          {
            "id": "w9-t3",
            "label": "Area Light 추가해서 부드러운 그림자 확인",
            "detail": "스튜디오 조명 느낌"
          },
          {
            "id": "w9-t4",
            "label": "Spot Light로 무대 조명 효과 만들기",
            "detail": "Radius로 범위 조절"
          }
        ],
        "image": "assets/images/week09/light-types.png",
        "showme": "light-types"
      },
      {
        "title": "HDRI 환경 조명",
        "copy": "360도 파노라마 사진이 전구 역할을 해요. HDRI 파일 하나로 자연스러운 환경 조명과 반사가 동시에 생겨요. 실외 씬에 특히 효과적이에요.",
        "goal": [
          "HDRI의 역할과 장점을 안다",
          "HDRI를 교체해서 분위기를 바꾼다"
        ],
        "done": [
          "HDRI로 씬 분위기가 바뀌었다",
          "2가지 이상 HDRI를 비교했다"
        ],
        "tasks": [
          {
            "id": "w9-t5",
            "label": "Poly Haven에서 HDRI 파일 다운로드",
            "detail": "polyhaven.com → HDRIs"
          },
          {
            "id": "w9-t6",
            "label": "World Properties → Surface → Environment Texture 추가",
            "detail": "Properties 패널 좌측 빨간 지구본(World) 아이콘 → Color 옆 노란 점 클릭 → Environment Texture 선택"
          },
          {
            "id": "w9-t7",
            "label": "Open Image로 .exr/.hdr 파일 불러오기",
            "detail": "Environment Texture 노드의 Open 버튼 → 다운로드한 HDRI 선택"
          },
          {
            "id": "w9-t8",
            "label": "다른 HDRI로 교체해서 분위기 비교",
            "detail": "실내/실외/석양 등"
          }
        ],
        "image": "assets/images/week09/hdri-world.png",
        "showme": "hdri-lighting"
      },
      {
        "title": "HDRI 프로 팁 2가지 (제품 렌더 필수)",
        "copy": "Tip 1 — HDRI 자체를 회전시켜 조명 방향 잡기\n\n조명 방향이 어색하거나 그림자가 엉뚱한 곳에 생길 때, 오브젝트나 카메라를 움직이는 대신 HDRI를 회전시키세요. 카메라 애니메이션을 망치지 않고 조명 방향만 바꿀 수 있어요.\n\n💡 같은 HDRI도 Z 회전만으로 완전히 다른 분위기가 나와요. 렌더할 때마다 이 과정을 거쳐 최적의 조명 각도를 찾는 게 프로 루틴이에요.\n\nTip 2 — HDRI 색상 제거 (순수 조명만 활용)\n\n석양·노란 스튜디오 HDRI를 적용하면 씬 전체가 노랗게 물드는 경우가 있어요. 빛 방향과 강도는 그대로 유지하면서 색상 영향만 제거하는 방법이에요.\n\n💡 제품 렌더에서 중립적인 조명이 필요할 때 특히 유용해요. HDRI의 빛 방향·강도는 살리면서 색상 캐스트만 제거할 수 있어요.",
        "goal": [
          "3점 조명의 원리를 이해한다",
          "직접 3점 조명을 세팅한다"
        ],
        "done": [
          "오브젝트가 입체감 있게 보인다",
          "각 조명의 역할을 설명할 수 있다"
        ],
        "tasks": [
          {
            "id": "w9-t9",
            "label": "Shader Editor 열기 → 좌상단 드롭다운을 Object에서 World로 전환",
            "detail": ""
          },
          {
            "id": "w9-t10",
            "label": "HDRI 텍스처 노드 선택 → Ctrl + T → Mapping Node 자동 추가됨",
            "detail": ""
          },
          {
            "id": "w9-t11",
            "label": "Mapping 노드 > Rotation > Z 값 드래그 → 뷰포트에서 그림자·하이라이트 방향이 실시간으로 바뀌는 걸 확인",
            "detail": ""
          },
          {
            "id": "w9-t4-2",
            "label": "Shader Editor > World 탭",
            "detail": "HDRI 텍스처 노드와 Background 노드 사이의 연결선 확인"
          },
          {
            "id": "w9-t5-2",
            "label": "Shift+A > Color > Hue/Saturation/Value 노드 추가 → HDRI와 Background 사이에 연결",
            "detail": ""
          },
          {
            "id": "w9-t6-2",
            "label": "Saturation 값을 1 → 0으로 낮춤 → 색상 캐스트 완전 제거 (은은하게 남기고 싶으면 0.1~0.3 사이 조정)",
            "detail": ""
          }
        ],
        "image": "assets/images/week09/three-point-light.png",
        "showme": "three-point-light"
      },
      {
        "title": "3점 조명 세팅",
        "copy": "프로 사진사들이 꼭 쓰는 방법이에요. Key(주), Fill(보조), Rim(윤곽) 세 개만 잘 놓으면 어떤 오브젝트도 입체감 있게 보여요.",
        "goal": [
          "3점 조명의 원리를 이해한다",
          "직접 3점 조명을 세팅한다"
        ],
        "done": [
          "카메라 뷰에서 원하는 구도가 잡혔다"
        ],
        "tasks": [
          {
            "id": "w9-t12",
            "label": "Key Light 배치",
            "detail": "오브젝트 앞 45도 위 — 가장 밝은 주 광원"
          },
          {
            "id": "w9-t13",
            "label": "Fill Light 배치",
            "detail": "Key 반대편, Energy 절반 — 그림자가 너무 어두운 걸 보완"
          },
          {
            "id": "w9-t14",
            "label": "Rim Light 배치",
            "detail": "뒤쪽에서 윤곽 강조 — 배경과 오브젝트를 분리하는 효과"
          }
        ],
        "image": "assets/images/week09/camera-setup.png"
      },
      {
        "title": "카메라 세팅",
        "copy": "조명을 아무리 잘 잡아도 카메라 앵글이 안 좋으면 소용없어요. 카메라 위치와 렌즈를 조절하면 같은 씬도 완전히 다르게 보여요.",
        "goal": [
          "카메라를 원하는 위치에 세팅한다"
        ],
        "done": [
          "3가지 분위기 렌더를 만들었다"
        ],
        "tasks": [
          {
            "id": "w9-t15",
            "label": "Numpad 0으로 카메라 뷰 전환",
            "detail": "씬에 카메라가 없으면 먼저 Shift+A → Camera로 추가"
          },
          {
            "id": "w9-t16",
            "label": "Ctrl+Numpad 0으로 현재 시점을 카메라로 설정",
            "detail": "직접 돌아다니다가 마음에 드는 앵글에서"
          },
          {
            "id": "w9-t3-2",
            "label": "Focal Length 조절해서 원근감 비교",
            "detail": "35mm(광각) vs 85mm(망원) 차이 — Depth of Field도 같은 패널에서 켤 수 있어요"
          }
        ],
        "image": "assets/images/week09/mood-lighting.png",
        "showme": "mood-lighting"
      },
      {
        "title": "분위기 연출 실험",
        "copy": "조명 색온도(따뜻/차가움)와 세기를 바꿔서 같은 로봇으로 낮/저녁/밤 분위기를 만들어요. 같은 오브젝트인데 사진 3장이 완전히 달라 보이면 성공이에요.",
        "goal": [
          "조명으로 분위기를 의도적으로 바꾼다"
        ],
        "done": [],
        "tasks": [
          {
            "id": "w9-t1-2",
            "label": "따뜻한 색(주황) Key Light로 석양 분위기 만들기",
            "detail": "Color Temp 약 3200K 느낌"
          },
          {
            "id": "w9-t2-2",
            "label": "차가운 색(파랑) 한 개로 밤 분위기 만들기",
            "detail": "Energy 낮추고 Rim만 강하게"
          },
          {
            "id": "w9-t3-3",
            "label": "중성광(흰색) Key + Fill로 낮 분위기 만들기",
            "detail": "Color Temp 5500K 느낌, Energy 균등 — 비교군"
          }
        ]
      }
    ],
    "shortcuts": [
      {
        "keys": "Shift + A → Light",
        "action": "조명 추가"
      },
      {
        "keys": "Z → Rendered",
        "action": "렌더 미리보기"
      },
      {
        "keys": "Shift + Z",
        "action": "Rendered/Solid 토글"
      },
      {
        "keys": "Numpad 0",
        "action": "카메라 뷰 전환"
      },
      {
        "keys": "Ctrl + Numpad 0",
        "action": "현재 시점 → 카메라"
      },
      {
        "keys": "Numpad .",
        "action": "선택 항목으로 프레이밍 (View Selected)"
      }
    ],
    "explore": [
      {
        "title": "HDRI + 3점 조명 조합",
        "hint": "HDRI로 전체 분위기를 잡고 3점 조명으로 디테일만 보강해보기"
      },
      {
        "title": "색 조명으로 사이버펑크 느낌 내기",
        "hint": "빨강/파랑/보라 Spot Light를 교차로 배치해서 네온 분위기 연출"
      },
      {
        "title": "극적인 실루엣 렌더",
        "hint": "Rim Light만 켜고 나머지 끈 상태에서 렌더 — 영화 포스터 느낌"
      },
      {
        "title": "Depth of Field 맛보기",
        "hint": "카메라 → Depth of Field 켜고 F-stop을 낮춰서 배경 흐림 효과"
      }
    ],
    "assignment": {
      "title": "본인 학생 페이지에 업로드",
      "description": "동일한 오브젝트에 3가지 다른 조명 분위기 렌더 이미지를 제출해요.",
      "checklist": [
        "낮/저녁/밤 또는 다른 3가지 분위기 렌더",
        "각 렌더의 조명 구성 간단 메모",
        "카메라 구도 의식적으로 설정",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "AgX (권장): 채도 보존, 하이라이트 자연스러움 → 컬러풀한 로봇에 적합",
      "Filmic: 약간 desaturated, 색이 빠져 보일 수 있음",
      "확인: Render Properties > Color Management > View Transform",
      "방법 1: Render Properties > Film > Transparent 체크",
      "방법 2: World Properties > Settings > Ray Visibility > Camera 체크 해제"
    ],
    "videos": [
      {
        "title": "Blender Studio - Lighting Fundamentals",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/lighting/"
      },
      {
        "title": "Poly Haven Add-on 사용법 (HDRI 드래그 앤 드롭)",
        "url": "https://docs.polyhaven.com/en/guides/blender-addon"
      }
    ],
    "docs": [
      {
        "title": "Lighting",
        "url": "https://docs.blender.org/manual/en/latest/render/lights/light_object.html"
      },
      {
        "title": "World Environment",
        "url": "https://docs.blender.org/manual/en/latest/render/lights/world.html"
      },
      {
        "title": "Camera",
        "url": "https://docs.blender.org/manual/en/latest/render/cameras.html"
      },
      {
        "title": "Depth of Field",
        "url": "https://docs.blender.org/manual/en/latest/render/cameras.html#depth-of-field"
      }
    ],
    "summary": "Light 4종·HDRI·3점 조명·카메라까지 다루며 같은 오브젝트로 다양한 분위기를 연출해요."
  },
  {
    "week": 10,
    "status": "upcoming",
    "title": "Animation 기초",
    "subtitle": "키프레임 · Dope Sheet · Graph Editor · 루프",
    "duration": "~3시간",
    "topics": [
      "키프레임 삽입과 삭제",
      "Location / Rotation / Scale 애니메이션",
      "Dope Sheet 타이밍 편집",
      "Graph Editor 커브 조절",
      "자동 키프레임 모드",
      "루프 애니메이션"
    ],
    "steps": [
      {
        "title": "키프레임 기초",
        "copy": "줄 인형의 관절 위치를 프레임마다 사진 찍어두는 거예요. 1프레임에서 A 위치, 50프레임에서 B 위치를 찍으면 Blender가 둘 사이를 자동으로 이어줘요.",
        "goal": [
          "키프레임의 개념을 이해한다",
          "이동 키프레임을 직접 찍는다"
        ],
        "done": [
          "오브젝트가 A에서 B로 이동하는 애니메이션이 됐다"
        ],
        "tasks": [
          {
            "id": "w10-t1",
            "label": "Frame 1에서 오브젝트 위치 잡기 + I → Location",
            "detail": "노란 다이아몬드가 Timeline에 찍힘"
          },
          {
            "id": "w10-t2",
            "label": "Frame 50으로 이동 후 위치 바꾸고 I → Location",
            "detail": "화살표 키 또는 직접 프레임 번호 입력"
          },
          {
            "id": "w10-t3",
            "label": "Space로 재생해서 이동 확인",
            "detail": ""
          }
        ],
        "image": "assets/images/week10/keyframe-intro.png",
        "showme": "keyframe-basics"
      },
      {
        "title": "회전·크기 애니메이션",
        "copy": "이동만 되는 게 아니에요. 회전, 크기 변화도 키프레임으로 기록할 수 있어요. 로봇 팔이 돌아가거나, 안테나가 쭉 올라오는 움직임을 만들 수 있어요.",
        "goal": [
          "Rotation과 Scale 키프레임을 찍는다"
        ],
        "done": [
          "오브젝트가 회전하면서 커지는 애니메이션을 만들었다"
        ],
        "tasks": [
          {
            "id": "w10-t4",
            "label": "Frame 1에서 I → Rotation 키프레임 삽입",
            "detail": ""
          },
          {
            "id": "w10-t5",
            "label": "Frame 30에서 R → Z → 180 → I → Rotation",
            "detail": "Z축으로 180도 회전"
          },
          {
            "id": "w10-t6",
            "label": "Frame 60에서 S → 2 → I → Scale",
            "detail": "2배로 커지는 애니메이션"
          }
        ],
        "image": "assets/images/week10/rotation-scale.png"
      },
      {
        "title": "Dope Sheet 타이밍",
        "copy": "키프레임들이 시간 순서대로 나열된 타임라인이에요. 키프레임 사이 간격을 늘리면 느리게, 줄이면 빠르게 움직여요. 음악의 박자를 조절하는 것과 비슷해요.",
        "goal": [
          "Dope Sheet에서 키프레임을 이동/복사한다",
          "타이밍을 직접 조절한다"
        ],
        "done": [
          "빠르게/느리게 달라지는 걸 확인했다",
          "키프레임을 복사해서 반복 구간을 만들었다"
        ],
        "tasks": [
          {
            "id": "w10-t7",
            "label": "Dope Sheet 열기",
            "detail": "Editor Type → Dope Sheet"
          },
          {
            "id": "w10-t8",
            "label": "키프레임 선택 후 G로 타이밍 이동",
            "detail": "간격 넓히면 느려지고, 좁히면 빨라져요"
          },
          {
            "id": "w10-t9",
            "label": "키프레임 선택 → Shift+D로 복사",
            "detail": "반복 동작 만들기에 유용"
          }
        ],
        "image": "assets/images/week10/dope-sheet.png"
      },
      {
        "title": "Graph Editor 커브",
        "copy": "Graph Editor는 움직임의 속도 곡선을 보여줘요. 직선이면 일정 속도, S자 커브면 천천히 시작해서 빨라졌다 다시 느려지는 자연스러운 움직임이에요.",
        "goal": [
          "Graph Editor에서 보간 커브를 이해한다",
          "Ease In/Out을 적용한다"
        ],
        "done": [
          "직선 보간과 곡선 보간의 차이를 눈으로 구분할 수 있다"
        ],
        "tasks": [
          {
            "id": "w10-t10",
            "label": "Graph Editor 열기",
            "detail": "Editor Type → Graph Editor"
          },
          {
            "id": "w10-t11",
            "label": "커브 핸들 잡아서 Ease In/Out 만들기",
            "detail": "부드럽게 시작, 부드럽게 멈춤"
          },
          {
            "id": "w10-t12",
            "label": "T 키로 Interpolation을 Bezier/Linear/Constant 비교",
            "detail": "같은 움직임도 느낌이 완전히 달라요"
          }
        ],
        "image": "assets/images/week10/graph-editor.png",
        "showme": "graph-editor"
      },
      {
        "title": "루프 애니메이션",
        "copy": "끝나면 처음으로 돌아가서 무한 반복되는 움직임이에요. 로봇 눈이 깜빡이거나, 안테나가 흔들리는 걸 만들 때 써요.",
        "goal": [
          "루프 애니메이션을 만든다"
        ],
        "done": [
          "끝과 처음이 자연스럽게 이어지는 루프를 만들었다"
        ],
        "tasks": [
          {
            "id": "w10-t13",
            "label": "첫 프레임과 마지막 프레임에 같은 키프레임 넣기",
            "detail": "마지막 프레임 = 첫 프레임 복사"
          },
          {
            "id": "w10-t14",
            "label": "Graph Editor → Channel → Extrapolation → Cyclic",
            "detail": "자동 반복 설정"
          }
        ],
        "image": "assets/images/week10/loop-animation.png"
      }
    ],
    "shortcuts": [
      {
        "keys": "I",
        "action": "Insert Keyframe"
      },
      {
        "keys": "Alt + I",
        "action": "Delete Keyframe"
      },
      {
        "keys": "Space",
        "action": "재생/정지"
      },
      {
        "keys": "← / →",
        "action": "이전/다음 프레임"
      },
      {
        "keys": "Shift + ← / →",
        "action": "시작/끝 프레임으로 이동"
      },
      {
        "keys": "T",
        "action": "Interpolation 변경 (Bezier/Linear)"
      },
      {
        "keys": "V",
        "action": "핸들 타입 변경 (Free/Auto)"
      }
    ],
    "explore": [
      {
        "title": "로봇 걸음걸이 만들기",
        "hint": "양쪽 다리에 번갈아 Rotation 키프레임을 넣어서 걷는 동작 만들기"
      },
      {
        "title": "Bounce 효과",
        "hint": "공이 바닥에 부딪혀 튀는 애니메이션 — Graph Editor의 Ease 곡선 활용"
      },
      {
        "title": "카메라 애니메이션",
        "hint": "카메라에 키프레임을 넣어서 씬을 돌며 찍는 영상 만들기"
      },
      {
        "title": "자동 키프레임 활용",
        "hint": "Auto Keying 켜고 오브젝트를 움직이기만 해도 자동 기록되는지 확인"
      }
    ],
    "assignment": {
      "title": "본인 학생 페이지에 업로드",
      "description": "오브젝트 1개가 이동/회전/크기 변화 중 2가지 이상을 포함한 5초(120프레임) 이상 애니메이션을 만들어요.",
      "checklist": [
        "이동+회전 또는 이동+크기 중 2가지 이상 포함",
        "Ease In/Out 적용된 구간 1곳 이상",
        "애니메이션 비디오 파일 or GIF",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "애니메이션이 끊김 → Graph Editor에서 Bezier 보간인지 확인",
      "키프레임이 안 찍힘 → Auto Keying이 꺼져 있으면 I 키로 수동 삽입",
      "오브젝트가 안 움직임 → Timeline 프레임을 이동했는지 확인",
      "루프가 튀김 → 첫 프레임과 마지막 프레임의 값이 동일해야 해요",
      "속도가 너무 일정해서 어색 → Graph Editor에서 Ease In/Out 넣기"
    ],
    "videos": [
      {
        "title": "Blender Studio - Animation Fundamentals",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/animation/"
      }
    ],
    "docs": [
      {
        "title": "Keyframes",
        "url": "https://docs.blender.org/manual/en/latest/animation/keyframes/introduction.html"
      },
      {
        "title": "Dope Sheet",
        "url": "https://docs.blender.org/manual/en/latest/editors/dope_sheet/introduction.html"
      },
      {
        "title": "Graph Editor",
        "url": "https://docs.blender.org/manual/en/latest/editors/graph_editor/introduction.html"
      },
      {
        "title": "Cyclic Extrapolation",
        "url": "https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/modifiers.html"
      }
    ],
    "summary": "키프레임으로 움직임을 기록하고, Dope Sheet과 Graph Editor로 타이밍을 조절해요. 마리오네트 인형에 줄을 매달듯, 움직임을 하나씩 기록하는 거예요."
  },
  {
    "week": 11,
    "status": "upcoming",
    "title": "Rigging 기초",
    "subtitle": "Armature · 본 구조 · 웨이트 페인팅 · 포즈",
    "duration": "~3시간",
    "topics": [
      "Armature 추가와 구조",
      "Bone 편집 (Extrude/Subdivide)",
      "Mesh Parenting (Automatic Weights)",
      "Pose Mode로 포즈 잡기",
      "Weight Paint 기초 수정",
      "Bone Constraint 맛보기"
    ],
    "steps": [
      {
        "title": "Armature 추가와 본 만들기",
        "copy": "마리오네트 인형에 철사 뼈대를 넣는 것처럼, 메쉬 안에 Bone(뼈)을 만들어요. 뼈를 움직이면 연결된 메쉬도 따라와요. 부모 뼈가 움직이면 자식 뼈도 같이 움직여요.",
        "goal": [
          "Armature 구조를 이해한다",
          "부모-자식 관계를 만든다"
        ],
        "done": [
          "몸통-팔-다리 구조의 본 체인이 있다"
        ],
        "tasks": [
          {
            "id": "w11-t1",
            "label": "Shift+A → Armature → Single Bone",
            "detail": "몸통 뼈 하나가 생겨요"
          },
          {
            "id": "w11-t2",
            "label": "Edit Mode에서 E로 본 확장 (팔, 다리 방향)",
            "detail": "부모-자식 관계가 자동으로 연결돼요"
          },
          {
            "id": "w11-t3",
            "label": "Subdivide로 중간에 관절 추가",
            "detail": "팔 뼈를 2개로 나누면 팔꿈치가 됨"
          },
          {
            "id": "w11-t4",
            "label": "Bone 이름 정리 (Properties → Bone)",
            "detail": "spine, arm.L, leg.R 같은 규칙"
          }
        ],
        "image": "assets/images/week11/armature-structure.png",
        "showme": "armature-basics"
      },
      {
        "title": "메쉬와 연결 (Skinning)",
        "copy": "피부(메쉬)와 뼈대(Armature)를 연결하는 거예요. Ctrl+P로 붙여놓으면 본을 움직일 때 메쉬도 따라와요. Blender가 어떤 메쉬가 어떤 뼈를 따라갈지 자동으로 계산해줘요.",
        "goal": [
          "Armature Parent의 개념을 이해한다",
          "Automatic Weights를 적용한다"
        ],
        "done": [
          "본을 움직이면 메쉬도 자연스럽게 따라온다"
        ],
        "tasks": [
          {
            "id": "w11-t5",
            "label": "Mesh 먼저 선택 → Shift+클릭으로 Armature 추가 선택",
            "detail": "순서 중요: 메쉬 먼저, Armature 나중에"
          },
          {
            "id": "w11-t6",
            "label": "Ctrl+P → With Automatic Weights 선택",
            "detail": "Blender가 자동으로 Weight를 계산"
          },
          {
            "id": "w11-t7",
            "label": "Armature 선택 후 Ctrl+Tab → Pose Mode 전환",
            "detail": "본이 파란색이면 Pose Mode"
          }
        ],
        "image": "assets/images/week11/mesh-skinning.png"
      },
      {
        "title": "Pose Mode로 포즈 잡기",
        "copy": "피규어 관절을 돌리듯 본을 하나씩 회전시켜서 포즈를 만들어요. 팔을 들거나, 고개를 숙이거나, 다리를 벌리거나.",
        "goal": [
          "Pose Mode에서 본을 조작한다",
          "원하는 포즈를 만든다"
        ],
        "done": [
          "포즈 2개 이상을 만들었다",
          "Alt+R로 리셋할 수 있다"
        ],
        "tasks": [
          {
            "id": "w11-t8",
            "label": "Pose Mode에서 팔 본 선택 → R → X로 들어올리기",
            "detail": ""
          },
          {
            "id": "w11-t9",
            "label": "여러 본을 조합해서 인사하는 포즈 만들기",
            "detail": "팔 올리고, 고개 약간 숙이기"
          },
          {
            "id": "w11-t10",
            "label": "Alt+R로 선택한 본 회전 초기화",
            "detail": "전체 리셋은 A → Alt+R"
          }
        ],
        "image": "assets/images/week11/pose-mode.png"
      },
      {
        "title": "Weight Paint 수정",
        "copy": "자동 Weight가 완벽하지 않을 때가 있어요. 팔을 올렸는데 몸통이 같이 딸려온다면 Weight를 직접 수정해줘야 해요. 빨강이 강한 영향, 파랑이 약한 영향이에요.",
        "goal": [
          "Weight Paint의 색 의미를 안다",
          "문제 부분을 직접 수정한다"
        ],
        "done": [
          "딸려오던 메쉬가 수정 후 자연스러워졌다"
        ],
        "tasks": [
          {
            "id": "w11-t11",
            "label": "메쉬 선택 → Ctrl+Tab → Weight Paint 모드 전환",
            "detail": "빨강=1.0(강한 영향), 파랑=0.0(영향 없음)"
          },
          {
            "id": "w11-t12",
            "label": "문제 있는 본 Vertex Group 선택 후 브러시로 칠하기",
            "detail": "Weight: 0으로 칠하면 영향 제거"
          },
          {
            "id": "w11-t13",
            "label": "Pose Mode로 돌아가서 수정 결과 확인",
            "detail": "반복: 수정 → 확인 → 수정"
          }
        ],
        "image": "assets/images/week11/weight-paint.png",
        "showme": "weight-paint"
      }
    ],
    "shortcuts": [
      {
        "keys": "Shift + A → Armature",
        "action": "뼈대 추가"
      },
      {
        "keys": "E",
        "action": "Bone 확장 (Edit Mode)"
      },
      {
        "keys": "Ctrl + P",
        "action": "Armature Deform 연결"
      },
      {
        "keys": "Alt + P",
        "action": "Parent 해제"
      },
      {
        "keys": "Ctrl + Tab",
        "action": "Pose Mode 전환"
      },
      {
        "keys": "Alt + R",
        "action": "Rotation 초기화 (Pose)"
      },
      {
        "keys": "Alt + G",
        "action": "Location 초기화 (Pose)"
      }
    ],
    "explore": [
      {
        "title": "로봇 팔 IK 체험",
        "hint": "Inverse Kinematics Constraint를 추가해서 손을 잡아당기면 팔이 자동으로 따라오는지 확인"
      },
      {
        "title": "표정 리깅 맛보기",
        "hint": "얼굴에 작은 본을 넣어서 눈썹이나 눈꺼풀을 움직이는 실험"
      },
      {
        "title": "대칭 리깅",
        "hint": "본 이름에 .L을 붙이고 Symmetrize로 반대쪽 자동 생성"
      },
      {
        "title": "포즈 라이브러리 저장",
        "hint": "Pose Library에 자주 쓰는 포즈를 등록해두면 나중에 바로 불러올 수 있어요"
      }
    ],
    "assignment": {
      "title": "본인 학생 페이지에 업로드",
      "description": "간단한 캐릭터 메쉬에 Armature를 연결하고 포즈 3가지를 스크린샷으로 제출해요.",
      "checklist": [
        "뼈대 구조 스크린샷 1장 (Edit Mode)",
        "포즈 3가지 스크린샷",
        "Weight Paint 수정 전후 비교 (선택)",
        "리깅된 .blend 파일"
      ]
    },
    "mistakes": [
      "Automatic Weights 오류 → 메쉬에 구멍이 있거나 중복 정점 있음. Merge by Distance 먼저",
      "팔을 들면 몸이 딸려옴 → Weight Paint에서 해당 본의 Weight를 0으로 칠하기",
      "본이 안 움직임 → Pose Mode인지 확인 (Edit Mode에서는 구조만 바뀜)",
      "포즈가 뒤틀림 → 본 방향이 이상하면 Edit Mode에서 Recalculate Roll",
      "메쉬가 안 따라옴 → Parent가 제대로 됐는지 Outliner에서 확인"
    ],
    "videos": [
      {
        "title": "Blender Studio - Armature and Rigging",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/armature-and-rigging/"
      }
    ],
    "docs": [
      {
        "title": "Armatures",
        "url": "https://docs.blender.org/manual/en/latest/animation/armatures/index.html"
      },
      {
        "title": "Skinning",
        "url": "https://docs.blender.org/manual/en/latest/animation/armatures/skinning/index.html"
      },
      {
        "title": "Weight Paint",
        "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/weight_paint/index.html"
      },
      {
        "title": "Pose Mode",
        "url": "https://docs.blender.org/manual/en/latest/animation/armatures/posing/index.html"
      }
    ],
    "summary": "Armature(뼈대)를 세팅하고 메쉬에 연결해 캐릭터를 움직여요. 마리오네트 인형에 줄을 매다는 거예요."
  },
  {
    "week": 12,
    "status": "upcoming",
    "title": "AI 활용 리깅 (Mixamo)",
    "subtitle": "Mixamo 자동 리깅 · FBX 워크플로우 · NLA",
    "duration": "~3시간",
    "topics": [
      "Blender → FBX 익스포트 준비",
      "Mixamo 업로드 및 자동 리깅",
      "애니메이션 선택 및 다운로드",
      "Blender FBX 임포트",
      "NLA Editor로 애니메이션 관리",
      "수동 리깅 vs AI 리깅 비교"
    ],
    "steps": [
      {
        "title": "익스포트 준비",
        "copy": "Mixamo에 올리기 전에 메쉬를 깔끔하게 정리해야 해요. Modifier를 Apply하고, 파츠를 하나로 합치고, Transform을 정리하는 거예요.",
        "goal": [
          "Mixamo 업로드용 메쉬를 준비한다"
        ],
        "done": [
          "하나로 합쳐진 깔끔한 메쉬가 준비됐다"
        ],
        "tasks": [
          {
            "id": "w12-t1",
            "label": "모든 파츠 선택 → Ctrl+J로 합치기",
            "detail": "Mixamo는 단일 메쉬를 선호해요"
          },
          {
            "id": "w12-t2",
            "label": "Ctrl+A → All Transforms 적용",
            "detail": "Scale/Rotation이 꼬이면 리깅도 꼬여요"
          },
          {
            "id": "w12-t3",
            "label": "File → Export → FBX 내보내기",
            "detail": "Apply Scalings: FBX All"
          }
        ],
        "image": "assets/images/week12/export-prep.png"
      },
      {
        "title": "Mixamo 자동 리깅",
        "copy": "AI가 메쉬를 분석해서 자동으로 뼈대를 넣어줘요. 수동으로 본을 하나하나 넣던 시간이 없어져요. 관절 마커를 맞춰주기만 하면 돼요.",
        "goal": [
          "Mixamo 자동 리깅 워크플로우를 안다"
        ],
        "done": [
          "Mixamo에서 캐릭터가 리깅됐다",
          "미리보기에서 움직이는 걸 확인했다"
        ],
        "tasks": [
          {
            "id": "w12-t4",
            "label": "Mixamo.com 접속 후 FBX 파일 업로드",
            "detail": "Adobe 계정 필요 (무료)"
          },
          {
            "id": "w12-t5",
            "label": "Auto Rigger에서 관절 마커(턱/손목/팔꿈치/무릎/사타구니) 맞추기",
            "detail": "정확할수록 결과가 좋아요"
          },
          {
            "id": "w12-t6",
            "label": "리깅 결과 미리보기에서 이상한 부분 확인",
            "detail": ""
          }
        ],
        "image": "assets/images/week12/mixamo-upload.png"
      },
      {
        "title": "애니메이션 선택 및 임포트",
        "copy": "Mixamo에서 걷기, 달리기, 춤추기 등 수백 가지 무료 애니메이션을 골라서 Blender로 가져와요. 리깅된 캐릭터에 바로 적용돼요.",
        "goal": [
          "Mixamo 애니메이션을 Blender에서 재생한다"
        ],
        "done": [
          "캐릭터가 걷거나 뛰는 애니메이션이 재생된다"
        ],
        "tasks": [
          {
            "id": "w12-t7",
            "label": "Mixamo Animations 탭에서 걷기/달리기/춤 골라보기",
            "detail": "미리보기로 확인 후 다운로드"
          },
          {
            "id": "w12-t8",
            "label": "FBX로 다운로드 (With Skin 옵션)",
            "detail": "Keyframe Reduction: None 추천"
          },
          {
            "id": "w12-t9",
            "label": "Blender → File → Import → FBX로 가져오기",
            "detail": ""
          },
          {
            "id": "w12-t10",
            "label": "Space로 애니메이션 재생 확인",
            "detail": "Timeline 범위를 맞춰야 보여요"
          }
        ],
        "image": "assets/images/week12/mixamo-import.png"
      },
      {
        "title": "NLA Editor로 애니메이션 관리",
        "copy": "NLA Editor는 애니메이션 클립을 레이어처럼 쌓고 이어 붙이는 곳이에요. 걷기 → 달리기 → 정지를 순서대로 이어 붙이면 하나의 긴 애니메이션이 돼요.",
        "goal": [
          "NLA Editor의 기본 개념을 이해한다"
        ],
        "done": [
          "2개 이상 애니메이션 클립을 확인했다"
        ],
        "tasks": [
          {
            "id": "w12-t11",
            "label": "NLA Editor 열기",
            "detail": "Editor Type → Nonlinear Animation"
          },
          {
            "id": "w12-t12",
            "label": "애니메이션 스트립 확인 및 드래그로 이동",
            "detail": "Action을 NLA 스트립으로 Push Down"
          }
        ],
        "image": "assets/images/week12/nla-editor.png"
      }
    ],
    "shortcuts": [
      {
        "keys": "Ctrl + J",
        "action": "오브젝트 합치기 (Join)"
      },
      {
        "keys": "Ctrl + A → All Transforms",
        "action": "Transform 적용"
      },
      {
        "keys": "M (Merge by Distance)",
        "action": "중복 정점 제거"
      },
      {
        "keys": "Space",
        "action": "애니메이션 재생/정지"
      },
      {
        "keys": "Shift + N",
        "action": "법선 재계산"
      }
    ],
    "explore": [
      {
        "title": "Mixamo 애니메이션 3개 이어 붙이기",
        "hint": "걷기 → 달리기 → 점프를 NLA Editor에서 연결해 하나의 시퀀스 만들기"
      },
      {
        "title": "수동 리깅 vs Mixamo 비교",
        "hint": "같은 캐릭터를 수동 리깅과 Mixamo로 각각 해보고 Weight 품질 비교"
      },
      {
        "title": "자신의 로봇에 Mixamo 적용",
        "hint": "Week 3-4에서 만든 로봇에 Mixamo 리깅을 적용해보기 (인체형이어야 잘 됨)"
      },
      {
        "title": "배경 씬에 캐릭터 배치",
        "hint": "조명/카메라 세팅된 씬에 Mixamo 캐릭터를 배치하고 렌더"
      }
    ],
    "assignment": {
      "title": "본인 학생 페이지에 업로드",
      "description": "Mixamo로 리깅된 캐릭터에 애니메이션 2가지 이상을 적용해요.",
      "checklist": [
        "리깅 과정 스크린샷 (Mixamo 마커 화면)",
        "애니메이션 2가지 재생 영상 or GIF",
        "수동 리깅 vs Mixamo 차이 한 줄 메모",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "FBX 임포트가 회전됨 → Import 설정에서 Manual Orientation, Forward: -Z, Up: Y",
      "메쉬가 너무 큼/작음 → Import 시 Scale 조절 또는 Ctrl+A",
      "Mixamo 업로드 실패 → 메쉬에 구멍이나 뒤집힌 법선 확인 (Shift+N)",
      "애니메이션이 슬로우 모션 → Frame Rate가 24fps와 맞는지 확인",
      "관절이 이상하게 꺾임 → Mixamo 마커 위치를 더 정확히 맞추고 재시도"
    ],
    "videos": [
      {
        "title": "Blender Studio - Importing Animations",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/importing/"
      }
    ],
    "docs": [
      {
        "title": "Import/Export",
        "url": "https://docs.blender.org/manual/en/latest/files/import_export/index.html"
      },
      {
        "title": "FBX Import",
        "url": "https://docs.blender.org/manual/en/latest/addons/import_export/scene_fbx.html"
      },
      {
        "title": "NLA Editor",
        "url": "https://docs.blender.org/manual/en/latest/editors/nla/index.html"
      }
    ],
    "summary": "Mixamo를 사용해 자동으로 리깅하고 무료 애니메이션을 Blender에 임포트해요. 수동 리깅과 비교해서 AI 활용의 장단점을 체험해요."
  },
  {
    "week": 13,
    "status": "upcoming",
    "title": "AI 영상/사운드 + 렌더링 + MCP",
    "subtitle": "Cycles vs EEVEE · 출력 설정 · Compositing · AI 후처리",
    "duration": "~3시간",
    "topics": [
      "Cycles vs EEVEE 비교",
      "렌더 샘플링과 노이즈",
      "Output 해상도와 파일 형식",
      "Compositing 노드 기초",
      "애니메이션 렌더링",
      "AI 후처리 체험"
    ],
    "steps": [
      {
        "title": "렌더 엔진 비교",
        "copy": "Cycles는 사진 인화처럼 정밀하고 느리고, EEVEE는 게임 엔진처럼 빠르지만 덜 사실적이에요. 수정 중엔 EEVEE, 최종 제출엔 Cycles를 써요. 용도에 따라 골라 쓰면 돼요.",
        "goal": [
          "두 엔진의 차이를 안다",
          "각각 어떤 상황에 쓰는지 판단한다"
        ],
        "done": [
          "같은 씬을 두 엔진으로 렌더해서 비교했다"
        ],
        "tasks": [
          {
            "id": "w13-t1",
            "label": "Render Properties → Engine → Cycles로 전환 후 F12",
            "detail": "렌더 시간 기록해두기"
          },
          {
            "id": "w13-t2",
            "label": "EEVEE로 전환 후 같은 씬 F12 → 속도와 품질 비교",
            "detail": "그림자, 반사, 유리 차이 주목"
          },
          {
            "id": "w13-t3",
            "label": "Cycles Samples를 128 → 512로 바꿔서 노이즈 비교",
            "detail": "높을수록 깨끗하지만 느림"
          }
        ],
        "image": "assets/images/week13/cycles-eevee.png",
        "showme": "render-settings",
        "widgets": [
          {
            "type": "showme",
            "id": "volume-to-mesh"
          }
        ]
      },
      {
        "title": "렌더 출력 설정",
        "copy": "해상도, 파일 형식, 저장 경로를 설정하고 F12로 렌더해요. 한 번 설정해두면 계속 쓸 수 있어요. 포트폴리오용이면 1920×1080 이상이 좋아요.",
        "goal": [
          "Output Properties를 자유롭게 설정한다"
        ],
        "done": [
          "의도한 해상도와 파일 형식으로 렌더가 저장됐다"
        ],
        "tasks": [
          {
            "id": "w13-t4",
            "label": "Output Properties → Resolution 1920×1080 설정",
            "detail": "% 스케일로 미리보기 가능 (50%로 빠른 테스트)"
          },
          {
            "id": "w13-t5",
            "label": "Output Format → PNG (이미지) 또는 FFmpeg (영상) 선택",
            "detail": ""
          },
          {
            "id": "w13-t6",
            "label": "파일 출력 경로 설정 후 F12로 렌더",
            "detail": "Image → Save As로 원하는 위치에 저장"
          }
        ],
        "image": "assets/images/week13/render-output.png"
      },
      {
        "title": "Compositing 기초",
        "copy": "사진 찍고 나서 보정하듯, 렌더 후에 밝기, 색감, 글로우 효과를 추가할 수 있어요. Compositing 노드로 후처리를 하면 렌더를 다시 안 해도 돼요.",
        "goal": [
          "Compositing 노드의 기본 흐름을 이해한다"
        ],
        "done": [
          "Glare나 Color Balance 효과를 적용했다"
        ],
        "tasks": [
          {
            "id": "w13-t7",
            "label": "Compositing 워크스페이스로 전환, Use Nodes 켜기",
            "detail": "Render Layers → Composite 기본 연결 확인"
          },
          {
            "id": "w13-t8",
            "label": "Shift+A → Filter → Glare 추가해서 빛 번짐 효과",
            "detail": "Emission 재질이 있으면 효과가 잘 보여요"
          },
          {
            "id": "w13-t9",
            "label": "Color Balance 노드로 색감 조정",
            "detail": "Lift/Gamma/Gain으로 분위기 바꾸기"
          }
        ],
        "image": "assets/images/week13/compositing.png",
        "showme": "compositing-basics"
      },
      {
        "title": "애니메이션 렌더링",
        "copy": "프레임을 하나씩 렌더해서 영상으로 만드는 거예요. Ctrl+F12 하나로 시작돼요. 시간이 오래 걸리니까 범위와 해상도를 먼저 확인하세요.",
        "goal": [
          "애니메이션 렌더 파이프라인을 이해한다"
        ],
        "done": [
          "5초 이상 애니메이션 영상 파일이 생성됐다"
        ],
        "tasks": [
          {
            "id": "w13-t10",
            "label": "Frame Range 확인 (Start/End Frame)",
            "detail": "24fps 기준 5초 = 120프레임"
          },
          {
            "id": "w13-t11",
            "label": "Output Format → FFmpeg → MPEG-4 설정",
            "detail": ".mp4 파일로 출력"
          },
          {
            "id": "w13-t12",
            "label": "EEVEE로 먼저 테스트 렌더 후 Cycles로 최종 렌더",
            "detail": "Ctrl+F12로 시작"
          }
        ],
        "image": "assets/images/week13/animation-render.png"
      },
      {
        "title": "AI 후처리 체험",
        "copy": "렌더 이미지를 AI 이미지 생성 툴에 넣으면 스타일을 바꾸거나 디테일을 추가할 수 있어요. 3D + AI의 하이브리드 워크플로우예요.",
        "goal": [
          "AI 후처리의 가능성을 이해한다"
        ],
        "done": [
          "렌더 이미지를 AI로 변형해봤다"
        ],
        "tasks": [
          {
            "id": "w13-t13",
            "label": "렌더 이미지를 AI 이미지 툴에 업로드 (img2img)",
            "detail": "스타일 변형이나 디테일 추가"
          },
          {
            "id": "w13-t14",
            "label": "원본 렌더와 AI 후처리 결과 나란히 비교",
            "detail": ""
          }
        ],
        "image": "assets/images/week13/ai-postprocess.png"
      }
    ],
    "shortcuts": [
      {
        "keys": "F12",
        "action": "이미지 렌더링"
      },
      {
        "keys": "Ctrl + F12",
        "action": "애니메이션 렌더링"
      },
      {
        "keys": "F11",
        "action": "마지막 렌더 결과 보기"
      },
      {
        "keys": "Esc",
        "action": "렌더 중지"
      },
      {
        "keys": "Z → Rendered",
        "action": "실시간 렌더 미리보기"
      },
      {
        "keys": "Ctrl + B (카메라 뷰)",
        "action": "렌더 영역 지정 (부분 렌더)"
      }
    ],
    "explore": [
      {
        "title": "Denoising 비교",
        "hint": "Cycles Render → Denoising 켜기/끄기로 낮은 샘플에서 품질 차이 비교"
      },
      {
        "title": "턴테이블 렌더",
        "hint": "카메라를 오브젝트 주위로 360도 회전시켜 턴테이블 영상 만들기"
      },
      {
        "title": "Transparent Background",
        "hint": "Film → Transparent 켜고 PNG로 렌더하면 배경 없는 이미지 — 합성용으로 유용"
      },
      {
        "title": "AI로 스타일 변형",
        "hint": "같은 렌더를 3가지 다른 AI 스타일(사이버펑크/수채화/픽셀아트)로 변형해보기"
      }
    ],
    "assignment": {
      "title": "렌더링 포트폴리오",
      "description": "EEVEE와 Cycles로 동일한 씬을 렌더한 비교 이미지와 최종 고품질 렌더를 제출해요.",
      "checklist": [
        "EEVEE vs Cycles 비교 이미지 (같은 앵글)",
        "Compositing 후처리 적용된 최종 렌더",
        "애니메이션 영상 파일 (5초 이상)",
        "AI 후처리 비교 이미지 (선택)"
      ]
    },
    "mistakes": [
      "렌더가 너무 오래 걸림 → Sample 수 줄이기 (초안은 64~128, 최종은 256~512)",
      "렌더가 검게 나옴 → 조명이 없거나 카메라가 오브젝트를 안 보고 있을 수 있어요",
      "영상 파일이 안 열림 → Output Format이 FFmpeg Video인지 확인",
      "Compositing이 적용 안 됨 → Use Nodes 체크박스가 켜져 있는지 확인",
      "노이즈가 심함 → Cycles Samples 올리거나 Denoising 켜기"
    ],
    "videos": [
      {
        "title": "Blender Studio - Rendering",
        "url": "https://studio.blender.org/training/blender-2-8-fundamentals/rendering/"
      }
    ],
    "docs": [
      {
        "title": "Cycles",
        "url": "https://docs.blender.org/manual/en/latest/render/cycles/index.html"
      },
      {
        "title": "EEVEE",
        "url": "https://docs.blender.org/manual/en/latest/render/eevee/index.html"
      },
      {
        "title": "Render Output",
        "url": "https://docs.blender.org/manual/en/latest/render/output/index.html"
      },
      {
        "title": "Compositing",
        "url": "https://docs.blender.org/manual/en/latest/compositing/index.html"
      },
      {
        "title": "Denoising",
        "url": "https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html"
      }
    ],
    "summary": "Cycles와 EEVEE의 차이를 이해하고 렌더 설정을 최적화해요. 카메라 감독처럼 최종 출력을 결정하는 단계예요."
  },
  {
    "week": 14,
    "status": "upcoming",
    "title": "최종 프로젝트 제작",
    "subtitle": "개인 프로젝트 집중 작업",
    "duration": "수업 전체 작업 + 피드백",
    "topics": [
      "자유 주제 3D 작품 완성",
      "교수 피드백 반영",
      "렌더링 마무리"
    ],
    "steps": [
      {
        "title": "프로젝트 마무리",
        "copy": "모델링·재질·조명·렌더링을 종합해서 최종 작품을 완성합니다.",
        "goal": [
          "발표 가능한 완성 작품"
        ],
        "done": [
          "렌더 이미지 5장 이상",
          ".blend 파일 정리 완료"
        ],
        "tasks": [
          {
            "id": "w14-t1",
            "label": "미완성 부분 목록 작성 후 우선순위 결정",
            "detail": ""
          },
          {
            "id": "w14-t2",
            "label": "재질/조명 최종 조정",
            "detail": ""
          },
          {
            "id": "w14-t3",
            "label": "최종 렌더 5장 이상 저장",
            "detail": ""
          }
        ]
      }
    ],
    "shortcuts": [],
    "explore": [],
    "assignment": {
      "title": "최종 프로젝트 사전 제출",
      "description": "기말 발표 전 .blend + 렌더 이미지를 제출합니다.",
      "checklist": [
        "렌더 이미지 5장 이상",
        ".blend 파일 정리된 상태"
      ]
    },
    "mistakes": [],
    "videos": [],
    "docs": [
      {
        "title": "Blender Manual: Animation",
        "url": "https://docs.blender.org/manual/en/latest/animation/index.html"
      },
      {
        "title": "Blender Manual: Rendering",
        "url": "https://docs.blender.org/manual/en/latest/render/index.html"
      }
    ],
    "summary": "학기 전체에서 배운 기술을 종합해 최종 프로젝트를 완성합니다. 교수 피드백 세션."
  },
  {
    "week": 15,
    "status": "upcoming",
    "title": "기말고사 - 최종 프로젝트 발표",
    "subtitle": "학기 전체 결과물 발표",
    "duration": "수업 전체 발표",
    "topics": [
      "최종 발표 (5분)",
      "작품 설명",
      "배운 점 공유"
    ],
    "steps": [
      {
        "title": "발표 준비",
        "copy": "발표 순서와 내용을 정리하고 최종 점검합니다.",
        "goal": [
          "발표 자료 완성"
        ],
        "done": [
          "5분 발표 연습 완료"
        ],
        "tasks": [
          {
            "id": "w15-t1",
            "label": "발표 내용 정리 (1—작품 소개, 2—기술 설명, 3—배운 점)",
            "detail": ""
          },
          {
            "id": "w15-t2",
            "label": "렌더 이미지 최종 선정",
            "detail": ""
          },
          {
            "id": "w15-t3",
            "label": "5분 발표 연습 1회 이상",
            "detail": ""
          }
        ]
      }
    ],
    "shortcuts": [],
    "explore": [],
    "assignment": {
      "title": "기말 발표",
      "description": "최종 작품 발표. 작품 소개 + 사용한 기술 + 배운 점을 5분 내외로 발표.",
      "checklist": [
        "발표 진행",
        "최종 파일 제출 완료"
      ]
    },
    "mistakes": [],
    "videos": [],
    "docs": [
      {
        "title": "Blender Manual",
        "url": "https://docs.blender.org/manual/en/latest/"
      }
    ],
    "summary": "학기 내내 만들어온 최종 작품을 발표합니다. 5분 내외, 제작 과정과 사용 기술 설명 포함."
  }
];

// Node.js 환경 대응
if (typeof module !== "undefined") module.exports = CURRICULUM;
