// ============================================================
// 15주 블렌더 수업 커리큘럼 데이터
// 이 파일만 수정하면 메인 페이지와 각 주차 페이지가 자동 반영됨
// ============================================================

const CURRICULUM = [
  {
    "week": 1,
    "status": "done",
    "title": "수업 시작 준비",
    "subtitle": "오리엔테이션 · Blender 설치 · 컨셉 설정",
    "summary": "Blender 설치, Mixboard로 컨셉 설정.",
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
    "docs": []
  },
  {
    "week": 2,
    "status": "done",
    "title": "Blender 인터페이스 · 기초",
    "subtitle": "화면 조작 · 오브젝트 변형 · 첫 모델링",
    "summary": "Blender 인터페이스, 화면 조작, G/R/S 변형, Extrude/Bevel/LoopCut 실습.",
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
        "image": "assets/images/week02/ui-overview.png",
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
        "image": "assets/images/week02/ui-overview.png"
      },
      {
        "title": "화면 조작",
        "image": "assets/images/week02/navigation-gizmo.png",
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
        "image": "assets/images/week02/navigation-gizmo.png"
      },
      {
        "title": "기본 변형 (G/R/S)",
        "image": "assets/images/week02/transform-gizmo.png",
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
        "image": "assets/images/week02/transform-gizmo.png"
      },
      {
        "title": "Edit Mode 모델링",
        "image": "assets/images/week02/editmode-modeling.png",
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
        "image": "assets/images/week02/editmode-modeling.png"
      },
      {
        "title": "Bevel 마무리",
        "image": "assets/images/week02/bevel-tool.png",
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
        "image": "assets/images/week02/bevel-tool.png"
      }
    ],
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
    ]
  },
  {
    "week": 3,
    "status": "active",
    "title": "기초 모델링 1 — Edit + Modifier",
    "subtitle": "기본형 · 대칭 · 곡면 · 반복",
    "summary": "Edit Mode로 기본형을 만들고 Modifier로 더 빠르게 다듬는 흐름을 익힙니다.",
    "duration": "~3시간",
    "topics": [
      "Extrude / Loop Cut / Inset / Bevel",
      "Mirror Modifier",
      "Subdivision / Solidify",
      "Array / Boolean",
      "필수 추가: Bevel / Weighted Normal",
      "Join / Separate",
      "Apply 타이밍",
      "선택 심화: Simple Deform / Decimate"
    ],
    "steps": [
      {
        "title": "기본형 만들기",
        "image": "assets/images/week03/base-form.png",
        "copy": "점토를 손으로 만지듯 기본형은 Edit Mode에서 직접 만들어요. 큰 덩어리를 먼저 잡고 세부는 나중에 다듬으면 돼요.",
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
        "image": "assets/images/week03/base-form.png"
      },
      {
        "title": "Mirror Modifier",
        "image": "assets/images/week03/mirror-modifier.png",
        "copy": "거울처럼 한쪽만 편집하면 반대쪽이 자동으로 따라와요. 로봇처럼 좌우 대칭인 모델에 제일 먼저 떠올리면 좋아요.",
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
        "image": "assets/images/week03/mirror-modifier.png"
      },
      {
        "title": "곡면과 두께",
        "image": "assets/images/week03/subdivision-surface.png",
        "copy": "각진 박스를 더 부드럽게 만들거나 납작한 면에 두께를 줄 수 있어요. 큰 실루엣을 빠르게 다듬을 때 많이 써요.",
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
        "image": "assets/images/week03/subdivision-surface.png"
      },
      {
        "title": "반복과 구멍",
        "image": "assets/images/week03/array-boolean-detail.png",
        "copy": "도장을 찍듯 같은 부품을 반복하거나, 블록을 빼내듯 구멍을 만들 수 있어요. 디테일을 빠르게 늘릴 때 유용해요.",
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
        "image": "assets/images/week03/array-boolean-detail.png"
      },
      {
        "title": "필수 추가 Modifier",
        "image": "assets/images/week03/bevel-weighted-normal.png",
        "copy": "핵심 5개 다음으로 바로 써먹기 좋은 보조 Modifier예요. `Ctrl+B`는 부분 수정, Bevel Modifier는 전체 정리, Weighted Normal은 음영 정리라고 나눠 생각하면 이해가 쉬워요.",
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
        "image": "assets/images/week03/bevel-weighted-normal.png"
      }
    ],
    "shortcuts": [
      {
        "keys": "E",
        "action": "Extrude (면/선 돌출)"
      },
      {
        "keys": "Ctrl + R",
        "action": "Loop Cut (루프 분할)"
      },
      {
        "keys": "I",
        "action": "Inset (면 안쪽에 새 면)"
      },
      {
        "keys": "Ctrl + B",
        "action": "Bevel (모서리 둥글게)"
      },
      {
        "keys": "Ctrl + 1/2/3",
        "action": "Subdivision Level 빠른 설정"
      },
      {
        "keys": "Shift + E",
        "action": "Edge Crease (날카로운 모서리 유지)"
      },
      {
        "keys": "Ctrl + A",
        "action": "Apply All Transforms (Modifier 전에 필수)"
      },
      {
        "keys": "S + X + 0",
        "action": "Mirror 중심선 X축 0 정렬"
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
      "title": "Edit + Modifier 로봇",
      "description": "Edit Mode와 Modifier를 함께 써서 기본형과 디테일이 보이는 형태를 만드세요.",
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
    ]
  },
  {
    "week": 4,
    "status": "upcoming",
    "title": "기초 모델링 2 — 디테일 & 정리",
    "subtitle": "Bevel · Weighted Normal · Apply",
    "summary": "지난 주 배운 흐름을 바탕으로 디테일 추가와 음영 정리를 더 안정적으로 반복합니다.",
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
        "image": "assets/images/week04/transform-apply.png",
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
        ]
      },
      {
        "title": "얼굴과 패널 디테일",
        "image": "assets/images/week04/inset-panel-detail.png",
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
        ]
      },
      {
        "title": "Bevel 두 가지 비교",
        "image": "assets/images/week04/bevel-modifier.png",
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
        ]
      },
      {
        "title": "Weighted Normal과 음영 정리",
        "image": "assets/images/week04/weighted-normal.png",
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
        ]
      },
      {
        "title": "Apply 시점과 최종 점검",
        "image": "assets/images/week04/array-modifier.png",
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
        ]
      }
    ],
    "shortcuts": [
      {
        "keys": "I",
        "action": "Inset (면 안쪽에 디테일 시작점 만들기)"
      },
      {
        "keys": "Ctrl + B",
        "action": "Bevel (특정 모서리 직접 다듬기)"
      },
      {
        "keys": "Ctrl + A",
        "action": "Apply All Transforms (Modifier 전 수치 정리)"
      },
      {
        "keys": "P",
        "action": "Separate (선택 파츠 분리)"
      },
      {
        "keys": "Ctrl + J",
        "action": "Join (오브젝트 합치기)"
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
    ]
  },
  {
    "week": 5,
    "status": "upcoming",
    "title": "AI 3D 생성 + Sculpting + MCP",
    "subtitle": "AI 툴 활용 · Sculpt Mode 기초",
    "summary": "AI 기반 3D 생성 툴을 경험하고, Sculpt Mode로 유기적인 형태를 만듭니다. MCP 연동을 실습합니다.",
    "duration": "~3시간",
    "topics": [
      "AI 3D 생성 툴 (Meshy/Tripo)",
      "Sculpt Mode 기초 브러시",
      "기본 MCP 연동"
    ],
    "steps": [
      {
        "title": "AI 3D 생성 체험",
        "copy": "텍스트 몇 글자 입력하면 3D 메쉬가 뚝딱 나와요. AI가 초안을 만들어주면 우리는 거기서 다듬기만 하면 돼요.",
        "goal": [
          "AI 생성 워크플로우를 이해한다"
        ],
        "done": [
          "AI 생성 메쉬를 Blender에서 열었다"
        ],
        "tasks": [
          {
            "id": "w5-t1",
            "label": "Meshy 또는 Tripo에서 프롬프트 입력 후 생성",
            "detail": ""
          },
          {
            "id": "w5-t2",
            "label": ".glb 파일 Blender에서 Import",
            "detail": "File → Import → glTF"
          }
        ]
      },
      {
        "title": "Sculpt Mode 기초",
        "image": "assets/images/week05/sculpt-mode.png",
        "copy": "브러시로 메쉬를 직접 주무르는 모드예요. 마우스로 칠하듯이 형태를 만들어요. 점토 조각과 가장 비슷한 방식이에요.",
        "goal": [
          "기본 Sculpt 브러시를 안다"
        ],
        "done": [
          "Sphere에서 커스텀 형태를 만들었다"
        ],
        "tasks": [
          {
            "id": "w5-t3",
            "label": "Ctrl+Tab으로 Sculpt Mode 전환",
            "detail": ""
          },
          {
            "id": "w5-t4",
            "label": "F로 브러시 크기, Shift+F로 강도 조절",
            "detail": ""
          },
          {
            "id": "w5-t5",
            "label": "Draw/Grab/Smooth 각각 사용해보기",
            "detail": ""
          }
        ]
      }
    ],
    "assignment": {
      "title": "AI + 수동 하이브리드 오브젝트",
      "description": "AI 생성 메쉬를 Sculpt로 수정한 결과물을 제출합니다.",
      "checklist": [
        "AI 생성 → Sculpt 수정 흔적 있는 .blend",
        "완성 이미지 1장"
      ]
    },
    "mistakes": [
      "AI 메쉬 폴리곤이 너무 많음 → Decimate Modifier로 줄이기"
    ],
    "docs": [
      {
        "title": "Sculpt Mode",
        "url": "https://docs.blender.org/manual/en/latest/sculpt_paint/sculpting/introduction/index.html"
      }
    ]
  },
  {
    "week": 6,
    "status": "upcoming",
    "title": "Material & Shader Node",
    "subtitle": "재질 시스템 · Shader Editor",
    "summary": "Material의 원리와 Shader Editor(Node 기반)를 이해하고 Principled BSDF로 다양한 재질을 표현합니다.",
    "duration": "~3시간",
    "topics": [
      "Material 슬롯 구조",
      "Principled BSDF",
      "Shader Node Editor 기초",
      "Color Ramp / Mix Shader"
    ],
    "steps": [
      {
        "title": "Material 할당",
        "image": "assets/images/week06/material-assign.png",
        "copy": "오브젝트에 색이나 재질을 입히는 거예요. 색만 바꿔도 결과물이 완전히 달라 보여요.",
        "goal": [
          "Material 슬롯의 구조를 안다"
        ],
        "done": [
          "오브젝트 색이 바뀌었다"
        ],
        "tasks": [
          {
            "id": "w6-t1",
            "label": "Material Properties에서 + New 클릭",
            "detail": ""
          },
          {
            "id": "w6-t2",
            "label": "Base Color 바꿔보기",
            "detail": ""
          }
        ]
      },
      {
        "title": "Principled BSDF 탐색",
        "image": "assets/images/week06/principled-bsdf.png",
        "copy": "숫자 하나로 금속/유리/플라스틱이 바뀌어요. Metallic을 1로 올리면 금속, Transmission을 1로 올리면 유리처럼 보여요.",
        "goal": [
          "각 파라미터가 보여서 효과를 안다"
        ],
        "done": [
          "유리/금속/플라스틱 재질을 각각 흉내냈다"
        ],
        "tasks": [
          {
            "id": "w6-t3",
            "label": "Metallic 1.0 → 금속 재질 확인",
            "detail": ""
          },
          {
            "id": "w6-t4",
            "label": "Transmission 1.0 → 유리 재질 확인",
            "detail": ""
          },
          {
            "id": "w6-t5",
            "label": "Roughness 0 vs 1 비교",
            "detail": ""
          }
        ]
      },
      {
        "title": "Shader Node Editor",
        "image": "assets/images/week06/shader-editor.png",
        "copy": "노드는 레고 블록처럼 연결해서 재질을 만들어요. 색을 그라데이션으로 바꾸거나 질감을 섞는 등 복잡한 재질이 가능해요.",
        "goal": [
          "노드 기반 재질 편집 방식을 이해한다"
        ],
        "done": [
          "ColorRamp를 Principled BSDF에 연결했다"
        ],
        "tasks": [
          {
            "id": "w6-t6",
            "label": "Shader Editor 열기 (Space → Shader Editor)",
            "detail": ""
          },
          {
            "id": "w6-t7",
            "label": "Shift+A → Color → Color Ramp 추가",
            "detail": ""
          },
          {
            "id": "w6-t8",
            "label": "Color Ramp → Base Color 연결",
            "detail": ""
          }
        ]
      }
    ],
    "assignment": {
      "title": "재질 스타일 샘플러",
      "description": "5가지 다른 재질로 구 5개를 만들어 나란히 배치하고 렌더합니다.",
      "checklist": [
        "5가지 재질 구 렌더 이미지",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "재질이 화면에서 안 보임 → Viewport Shading을 Rendered로 변경"
    ],
    "docs": [
      {
        "title": "Principled BSDF",
        "url": "https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html"
      },
      {
        "title": "Shader Editor",
        "url": "https://docs.blender.org/manual/en/latest/editors/shader_editor.html"
      }
    ]
  },
  {
    "week": 7,
    "status": "upcoming",
    "title": "UV Unwrapping + AI Texture",
    "subtitle": "UV 펼치기 · 텍스처 매핑",
    "summary": "UV Unwrapping으로 메쉬를 펼치고 AI 텍스처 생성 툴로 만든 이미지를 입힙니다.",
    "duration": "~3시간",
    "topics": [
      "UV 개념",
      "Seam 설정 + Unwrap",
      "UV Editor",
      "AI Texture 적용"
    ],
    "steps": [
      {
        "title": "Seam 설정",
        "image": "assets/images/week07/uv-seam.png",
        "copy": "종이 박스를 펼치면 평평해지죠. UV Unwrap도 3D 메쉬를 종이처럼 바닥에 펼치는 거예요. 그 위에 이미지를 올리면 텍스처가 입혀져요.",
        "goal": [
          "Seam의 역할을 이해한다"
        ],
        "done": [
          "빨간 Seam 선이 표시됐다"
        ],
        "tasks": [
          {
            "id": "w7-t1",
            "label": "Edit Mode → Edge Select 모드",
            "detail": ""
          },
          {
            "id": "w7-t2",
            "label": "Edge 선택 후 Ctrl+E → Mark Seam",
            "detail": ""
          }
        ]
      },
      {
        "title": "Unwrap & UV Editor",
        "image": "assets/images/week07/uv-editor.png",
        "copy": "Seam을 그은 경계선대로 메쉬가 펼쳐져서 UV Editor에 2D로 나와요. 여기 보이는 모양대로 이미지가 입혀져요.",
        "goal": [
          "UV가 어떻게 펼쳐지는지 이해한다"
        ],
        "done": [
          "UV Editor에서 메쉬가 2D로 보인다"
        ],
        "tasks": [
          {
            "id": "w7-t3",
            "label": "U → Unwrap 실행",
            "detail": ""
          },
          {
            "id": "w7-t4",
            "label": "UV Editor 열어서 결과 확인",
            "detail": ""
          },
          {
            "id": "w7-t5",
            "label": "UV 섬 이동/크기 조절해보기",
            "detail": ""
          }
        ]
      },
      {
        "title": "AI Texture 적용",
        "copy": "AI가 만든 이미지를 메쉬 표면에 붙이는 거예요. UV가 제대로 펼쳐져 있어야 이미지가 자연스럽게 입혀져요.",
        "goal": [
          "Image Texture 노드 사용법을 안다"
        ],
        "done": [
          "메쉬에 텍스처가 입혀졌다"
        ],
        "tasks": [
          {
            "id": "w7-t6",
            "label": "AI 텍스처 이미지 파일 저장",
            "detail": "Stable Diffusion, Adobe Firefly 등"
          },
          {
            "id": "w7-t7",
            "label": "Shader Editor → Image Texture 노드 추가",
            "detail": ""
          },
          {
            "id": "w7-t8",
            "label": "이미지 파일 연결 후 Base Color에 연결",
            "detail": ""
          }
        ]
      }
    ],
    "assignment": {
      "title": "텍스처 입힌 소품",
      "description": "Seam → Unwrap → AI Texture 순서로 텍스처를 입힌 소품을 제출합니다.",
      "checklist": [
        "UV Unwrap이 완료된 .blend",
        "AI 텍스처 이미지 포함",
        "렌더 이미지 1장"
      ]
    },
    "mistakes": [
      "텍스처가 늘어남 → Seam 위치 조정 필요",
      "연결 끊김 → UV Map이 Material과 동일한지 확인"
    ],
    "docs": [
      {
        "title": "UV Unwrapping",
        "url": "https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/index.html"
      }
    ]
  },
  {
    "week": 8,
    "status": "upcoming",
    "title": "⭐ 중간고사 — 중간 프로젝트 발표",
    "subtitle": "지금까지 배운 것을 담은 작품 발표",
    "summary": "Week 01~07에서 배운 모델링·재질·텍스처를 활용한 개인 프로젝트를 발표합니다.",
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
    "docs": []
  },
  {
    "week": 9,
    "status": "upcoming",
    "title": "Lighting 기초 + MCP 조명 연출",
    "subtitle": "빛의 종류 · HDRI · 조명 연출",
    "summary": "Point/Sun/Area/Spot Light의 특성과 HDRI 환경 조명을 이해하고 씬 분위기를 연출합니다.",
    "duration": "~3시간",
    "topics": [
      "Light 오브젝트 종류",
      "HDRI 환경 조명",
      "3점 조명법",
      "MCP 조명 자동화"
    ],
    "steps": [
      {
        "title": "Light 종류 탐색",
        "image": "assets/images/week09/light-types.png",
        "copy": "요리사 스튜디오에서 조명을 세팅하듯, 어떤 조명을 쓰냐에 따라 분위기가 완전히 달라져요. 동일한 오브젝트라도 조명만 바꾸면 다른 작품처럼 보여요.",
        "goal": [
          "각 Light 타입의 특성을 안다"
        ],
        "done": [
          "4가지 Light를 각각 테스트해봤다"
        ],
        "tasks": [
          {
            "id": "w9-t1",
            "label": "Shift+A → Light → 4종류 각각 추가해보기",
            "detail": ""
          },
          {
            "id": "w9-t2",
            "label": "Energy/Color 값 조절해보기",
            "detail": ""
          }
        ]
      },
      {
        "title": "HDRI 환경 조명",
        "image": "assets/images/week09/hdri-world.png",
        "copy": "360도 파노라마 사진이 전구 역할을 해요. 텍스처 하나로 자연스러운 환경 조명을 만들 수 있어요.",
        "goal": [
          "HDRI의 역할과 장점을 안다"
        ],
        "done": [
          "HDRI로 씬 분위기가 바뀌었다"
        ],
        "tasks": [
          {
            "id": "w9-t3",
            "label": "World Properties → Environment Texture 추가",
            "detail": ""
          },
          {
            "id": "w9-t4",
            "label": "HDRI 이미지 파일 연결 (Poly Haven 등)",
            "detail": ""
          }
        ]
      },
      {
        "title": "3점 조명 세팅",
        "image": "assets/images/week09/three-point-light.png",
        "copy": "사진 체울린 사진처럼 Key(주), Fill(보조), Rim(윤곽) 세 개만 잘 놓으면 어떤 오브젝트도 입체감 있게 보여요.",
        "goal": [
          "3점 조명의 원리를 이해한다"
        ],
        "done": [
          "오브젝트가 입체감 있게 보인다"
        ],
        "tasks": [
          {
            "id": "w9-t5",
            "label": "Key Light (주 광원) 배치",
            "detail": "오브젝트 앞 45도 위치"
          },
          {
            "id": "w9-t6",
            "label": "Fill Light (보조 광원) 배치",
            "detail": "반대편 낮게"
          },
          {
            "id": "w9-t7",
            "label": "Rim Light (윤곽 광원) 배치",
            "detail": "뒤쪽에서 윤곽 강조"
          }
        ]
      }
    ],
    "assignment": {
      "title": "조명 포트폴리오",
      "description": "동일한 오브젝트에 3가지 다른 조명 분위기 렌더 이미지를 제출합니다.",
      "checklist": [
        "낮/저녁/밤 또는 다른 3가지 분위기 렌더",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "빛이 너무 강함 → Energy 값 줄이기",
      "그림자 없음 → Shadow 설정 확인"
    ],
    "docs": [
      {
        "title": "Lighting",
        "url": "https://docs.blender.org/manual/en/latest/render/lights/light_object.html"
      }
    ]
  },
  {
    "week": 10,
    "status": "upcoming",
    "title": "Animation 기초",
    "subtitle": "키프레임 · Dope Sheet · 그래프 편집",
    "summary": "키프레임의 개념과 Dope Sheet, Graph Editor를 사용해 기초 애니메이션을 만듭니다.",
    "duration": "~3시간",
    "topics": [
      "키프레임 삽입 (I 키)",
      "Dope Sheet",
      "Graph Editor",
      "자동 키프레임"
    ],
    "steps": [
      {
        "title": "키프레임 기초",
        "image": "assets/images/week10/keyframe-intro.png",
        "copy": "A 위치를 1프레임에 사진 찍고, B 위치를 50프레임에 사진 찍으면 Blender가 둘 사이를 자동으로 이어줘요. 그게 키프레임이에요.",
        "goal": [
          "키프레임의 개념을 이해한다"
        ],
        "done": [
          "오브젝트가 A에서 B로 이동하는 애니메이션이 됐다"
        ],
        "tasks": [
          {
            "id": "w10-t1",
            "label": "Frame 1에서 오브젝트 위치 잡기 + I → Location",
            "detail": ""
          },
          {
            "id": "w10-t2",
            "label": "Frame 50으로 이동 후 위치 바꾸고 I → Location",
            "detail": ""
          },
          {
            "id": "w10-t3",
            "label": "Space로 재생해서 이동 확인",
            "detail": ""
          }
        ]
      },
      {
        "title": "Dope Sheet",
        "image": "assets/images/week10/dope-sheet.png",
        "copy": "키프레임들이 시간 순서대로 나열된 타임라인이에요. 사진들 사이 간격을 늘리거나 줄여서 빠르게/느리게 움직이는 타이밍을 조절해요.",
        "goal": [
          "키프레임 위치를 드래그로 조절한다"
        ],
        "done": [
          "빠르게/느리게 달라지는 걸 확인했다"
        ],
        "tasks": [
          {
            "id": "w10-t4",
            "label": "Dope Sheet 열기 (Editor Type 변경)",
            "detail": ""
          },
          {
            "id": "w10-t5",
            "label": "키프레임 선택 후 G로 이동",
            "detail": ""
          }
        ]
      }
    ],
    "assignment": {
      "title": "간단한 움직임 애니메이션",
      "description": "오브젝트 1개가 이동/회전/크기 변화 중 2가지를 포함한 5초 이상 애니메이션.",
      "checklist": [
        "애니메이션 비디오 파일 or GIF",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "애니메이션이 끊김 → 보간 방식 Graph Editor에서 확인"
    ],
    "docs": [
      {
        "title": "Keyframes",
        "url": "https://docs.blender.org/manual/en/latest/animation/keyframes/introduction.html"
      }
    ]
  },
  {
    "week": 11,
    "status": "upcoming",
    "title": "Rigging 기초",
    "subtitle": "Armature · 본 구조 · 웨이트 페인팅",
    "summary": "Armature(뼈대)를 세팅하고 메쉬에 연결(Parent)해 캐릭터 리깅의 기초를 실습합니다.",
    "duration": "~3시간",
    "topics": [
      "Armature 추가",
      "Bone 편집",
      "Mesh Parenting",
      "Weight Paint 기초"
    ],
    "steps": [
      {
        "title": "Armature 추가",
        "image": "assets/images/week11/armature-structure.png",
        "copy": "인형에 철사 뼈대를 넣는 것처럼, 메쉬 안에 Bone(뼈)을 만들어요. 뼈를 움직이면 연결된 메쉬도 따라와요.",
        "goal": [
          "Armature 구조를 이해한다"
        ],
        "done": [
          "두 개 이상의 본이 연결된 구조가 있다"
        ],
        "tasks": [
          {
            "id": "w11-t1",
            "label": "Shift+A → Armature → Single Bone",
            "detail": ""
          },
          {
            "id": "w11-t2",
            "label": "Edit Mode로 본 추가 (E로 Extrude)",
            "detail": ""
          }
        ]
      },
      {
        "title": "메쉬 연결",
        "image": "assets/images/week11/mesh-skinning.png",
        "copy": "메쉬(피부)와 Armature(뼈대)를 연결하는 거예요. Ctrl+P로 붙여놓으면 본을 움직일 때 메쉬도 따라와요.",
        "goal": [
          "Armature Parent의 개념을 이해한다"
        ],
        "done": [
          "본을 움직이면 메쉬도 따라온다"
        ],
        "tasks": [
          {
            "id": "w11-t3",
            "label": "Mesh → Armature 순서로 선택",
            "detail": ""
          },
          {
            "id": "w11-t4",
            "label": "Ctrl+P → With Automatic Weights",
            "detail": ""
          },
          {
            "id": "w11-t5",
            "label": "Pose Mode에서 본 회전해보기 (R키)",
            "detail": ""
          }
        ]
      }
    ],
    "assignment": {
      "title": "기본 캐릭터 리깅",
      "description": "간단한 캐릭터 메쉬에 Armature를 연결하고 포즈 3가지를 스크린샷으로 제출합니다.",
      "checklist": [
        "포즈 3가지 스크린샷",
        "리깅된 .blend 파일"
      ]
    },
    "mistakes": [
      "Weight Paint가 이상 → Automatic Weights 재설정"
    ],
    "docs": [
      {
        "title": "Armatures",
        "url": "https://docs.blender.org/manual/en/latest/animation/armatures/index.html"
      }
    ]
  },
  {
    "week": 12,
    "status": "upcoming",
    "title": "AI 활용 리깅 (Mixamo)",
    "subtitle": "Mixamo 자동 리깅 · 애니메이션 임포트",
    "summary": "Mixamo를 사용해 자동으로 리깅하고 무료 애니메이션을 Blender에 임포트합니다.",
    "duration": "~3시간",
    "topics": [
      "Mixamo 업로드 및 리깅",
      "FBX 익스포트",
      "Blender 임포트",
      "애니메이션 재생"
    ],
    "steps": [
      {
        "title": "Mixamo 업로드",
        "copy": "AI가 파일을 불러와서 자동으로 뼈대를 넣어줘요. 수동으로 본을 하나하나 넣던 시간이 없어져요.",
        "goal": [
          "Mixamo 워크플로우를 안다"
        ],
        "done": [
          "Mixamo에서 캐릭터가 리깅됐다"
        ],
        "tasks": [
          {
            "id": "w12-t1",
            "label": "Blender에서 .obj 또는 .fbx 익스포트",
            "detail": ""
          },
          {
            "id": "w12-t2",
            "label": "Mixamo.com 에 파일 업로드",
            "detail": ""
          },
          {
            "id": "w12-t3",
            "label": "자동 리깅 후 확인",
            "detail": ""
          }
        ]
      },
      {
        "title": "애니메이션 다운로드 및 임포트",
        "image": "assets/images/week12/mixamo-import.png",
        "copy": "Mixamo에서 걷기, 달리기, 춤추기 등 애니메이션을 골라서 Blender로 가져와요.",
        "goal": [
          "FBX 임포트 방식을 안다"
        ],
        "done": [
          "캐릭터가 걷거나 뛰는 애니메이션이 재생된다"
        ],
        "tasks": [
          {
            "id": "w12-t4",
            "label": "Mixamo에서 애니메이션 선택 후 FBX 다운로드",
            "detail": ""
          },
          {
            "id": "w12-t5",
            "label": "Blender → File → Import → FBX",
            "detail": ""
          },
          {
            "id": "w12-t6",
            "label": "Dope Sheet에서 애니메이션 재생 확인",
            "detail": ""
          }
        ]
      }
    ],
    "assignment": {
      "title": "AI 리깅 캐릭터 애니메이션",
      "description": "Mixamo로 리깅된 캐릭터의 애니메이션이 재생되는 Blender 파일과 렌더 영상.",
      "checklist": [
        "애니메이션 재생 영상 or GIF",
        ".blend 파일"
      ]
    },
    "mistakes": [
      "FBX 임포트가 회전됨 → Import 설정에서 Forward/Up 방향 확인"
    ],
    "docs": []
  },
  {
    "week": 13,
    "status": "upcoming",
    "title": "AI 영상/사운드 + 렌더링 + MCP",
    "subtitle": "Cycles vs EEVEE · 출력 설정 · AI 후처리",
    "summary": "Cycles와 EEVEE의 차이를 이해하고 렌더 설정을 최적화합니다. AI 영상/사운드 연동을 실습합니다.",
    "duration": "~3시간",
    "topics": [
      "Cycles vs EEVEE",
      "렌더 출력 설정",
      "AI 영상 후처리",
      "사운드 연동"
    ],
    "steps": [
      {
        "title": "렌더 엔진 비교",
        "image": "assets/images/week13/cycles-eevee.png",
        "copy": "Cycles는 사진 인화처럼 정밀하고 느리고, EEVEE는 게임 엔진처럼 빠르지만 덜 사실적이에요. 수정 중엔 EEVEE, 최종 제출엔 Cycles를 써요.",
        "goal": [
          "두 엔진의 차이를 안다"
        ],
        "done": [
          "용도에 따라 어떤 엔진을 쓸지 선택할 수 있다"
        ],
        "tasks": [
          {
            "id": "w13-t1",
            "label": "Render Properties → Engine → Cycles로 전환",
            "detail": ""
          },
          {
            "id": "w13-t2",
            "label": "EEVEE로 전환 후 속도 차이 비교",
            "detail": ""
          }
        ]
      },
      {
        "title": "출력 설정 및 렌더",
        "image": "assets/images/week13/render-output.png",
        "copy": "해상도, 파일 형식, 저장 경로를 설정하고 F12로 렌더해요. 한 번 설정해두면 계속 쓸 수 있어요.",
        "goal": [
          "렌더 출력 파이프라인을 이해한다"
        ],
        "done": [
          "Output Properties에서 파일 형식과 경로를 설정했다"
        ],
        "tasks": [
          {
            "id": "w13-t3",
            "label": "Output Properties → 해상도 1920×1080 설정",
            "detail": ""
          },
          {
            "id": "w13-t4",
            "label": "파일 출력 경로 설정",
            "detail": ""
          },
          {
            "id": "w13-t5",
            "label": "F12로 단일 프레임 렌더 확인",
            "detail": ""
          }
        ]
      }
    ],
    "assignment": {
      "title": "렌더링 설정 포트폴리오",
      "description": "EEVEE와 Cycles로 동일한 씬을 렌더한 비교 이미지와 최종 고품질 렌더.",
      "checklist": [
        "두 엔진 비교 이미지",
        "최종 렌더 이미지"
      ]
    },
    "mistakes": [
      "렌더가 너무 오래 걸림 → Sample 수 줄이기 (초안은 64~128)"
    ],
    "docs": [
      {
        "title": "Cycles Render",
        "url": "https://docs.blender.org/manual/en/latest/render/cycles/index.html"
      }
    ]
  },
  {
    "week": 14,
    "status": "upcoming",
    "title": "최종 프로젝트 제작",
    "subtitle": "개인 프로젝트 집중 작업",
    "summary": "학기 전체에서 배운 기술을 종합해 최종 프로젝트를 완성합니다. 교수 피드백 세션.",
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
    "assignment": {
      "title": "최종 프로젝트 사전 제출",
      "description": "기말 발표 전 .blend + 렌더 이미지를 제출합니다.",
      "checklist": [
        "렌더 이미지 5장 이상",
        ".blend 파일 정리된 상태"
      ]
    },
    "mistakes": [],
    "docs": []
  },
  {
    "week": 15,
    "status": "upcoming",
    "title": "⭐ 기말고사 — 최종 프로젝트 발표",
    "subtitle": "학기 전체 결과물 발표",
    "summary": "학기 내내 만들어온 최종 작품을 발표합니다. 5분 내외, 제작 과정과 사용 기술 설명 포함.",
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
    "assignment": {
      "title": "기말 발표",
      "description": "최종 작품 발표. 작품 소개 + 사용한 기술 + 배운 점을 5분 내외로 발표.",
      "checklist": [
        "발표 진행",
        "최종 파일 제출 완료"
      ]
    },
    "mistakes": [],
    "docs": []
  }
];

// Node.js 환경 대응
if (typeof module !== "undefined") module.exports = CURRICULUM;
