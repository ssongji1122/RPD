# Week 4 카드 품질 업그레이드 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Week 4 Show Me 카드 19개의 보충 콘텐츠를 채우고, 핵심 3개 카드의 HTML을 transform-apply 수준으로 보강한다.

**Architecture:** `_supplements.json`에 19개 엔트리 추가(Phase 1) → `boolean-modifier.html`, `bevel-modifier.html`, `weighted-normal.html` HTML 보강(Phase 2). 각 카드에 원인→결과 섹션, 흔한 실수 카드, 사용법 보강을 추가.

**Tech Stack:** JSON (supplements), HTML/CSS/JS (카드), Canvas 2D (비주얼 데모)

---

## Phase 1: 보충 콘텐츠 (_supplements.json)

### Task 1: 핵심 카드 4개 보충 콘텐츠 추가

**Files:**
- Modify: `course-site/assets/showme/_supplements.json` (파일 끝 `}` 앞에 추가)

**Step 1: 기존 supplements.json 백업 확인**

Run: `git diff --stat` 으로 현재 변경 사항 없음 확인

**Step 2: boolean-modifier 보충 콘텐츠 추가**

`_supplements.json`의 마지막 엔트리 뒤에 추가:

```json
"boolean-modifier": {
  "title": "Boolean이 꼬였다면?",
  "analogy": {
    "emoji": "🍪",
    "headline": "쿠키 커터로 반죽을 찍어내는 거예요",
    "body": "Difference는 찍어서 빼고, Union은 두 덩어리를 합치고, Intersect는 겹치는 부분만 남기는 동작이에요. 커터(오브젝트)는 도구일 뿐이라 작업 후에도 남겨둬야 해요."
  },
  "before_after": {
    "before": "Boolean 적용 후 커터 오브젝트를 삭제하면 Boolean이 풀려서 원래 형태로 돌아간다.",
    "after": "커터는 H로 숨기고, 필요하면 나중에 수정할 수 있게 유지한다. Apply 후에야 안전하게 삭제 가능."
  },
  "confusion": [
    {
      "symptom": "Boolean 적용했는데 구멍 안쪽이 까맣게 보여요.",
      "reason": "Difference로 뚫린 면의 Normal이 뒤집혀 있기 때문이에요.",
      "fix": "Edit Mode → Mesh → Normals → Recalculate Outside (Shift+N)로 노말을 정리하세요."
    },
    {
      "symptom": "커터 오브젝트를 삭제했더니 Boolean이 풀렸어요.",
      "reason": "Modifier가 커터 오브젝트를 참조하고 있어서, 참조 대상이 사라지면 Modifier도 무효화돼요.",
      "fix": "커터는 H로 숨기되 삭제하지 마세요. Apply 후에야 안전하게 삭제할 수 있어요."
    }
  ],
  "takeaway": "Boolean은 오브젝트끼리 형태를 더하거나 빼는 도구예요. 커터는 숨기되 삭제하지 않는 게 핵심이에요.",
  "targets": ["boolean-modifier"]
}
```

**Step 3: bevel-modifier 보충 콘텐츠 추가**

```json
"bevel-modifier": {
  "title": "Bevel이 이상하다면?",
  "analogy": {
    "emoji": "🪵",
    "headline": "나무 가구의 모서리를 사포로 깎는 작업이에요",
    "body": "Segments는 사포질 횟수(많을수록 둥글게), Width는 깎는 폭이에요. Limit Method로 어떤 모서리만 깎을지 고를 수 있어요."
  },
  "before_after": {
    "before": "Limit Method가 None이면 모든 모서리에 Bevel이 걸려서 의도하지 않은 곳까지 변형된다.",
    "after": "Weight 방식으로 바꾸고 Ctrl+Shift+E로 원하는 엣지에만 가중치를 주면 선택적 Bevel이 가능하다."
  },
  "confusion": [
    {
      "symptom": "모든 모서리가 다 깎여버려요.",
      "reason": "Limit Method가 기본값(None)이라 전체 엣지에 적용되고 있기 때문이에요.",
      "fix": "Limit Method를 Weight로 바꾸고, 원하는 엣지에 Ctrl+Shift+E로 Bevel Weight를 지정하세요."
    },
    {
      "symptom": "Bevel 후 음영이 지저분해요.",
      "reason": "Bevel이 만든 좁은 면들의 Normal 방향이 불균일해서예요.",
      "fix": "Bevel 아래에 Weighted Normal Modifier를 추가하면 음영이 깨끗해져요."
    }
  ],
  "takeaway": "Bevel Modifier는 비파괴적으로 모서리를 다듬는 도구예요. Weight + Weighted Normal 조합이 실전 표준이에요.",
  "targets": ["bevel-modifier"]
}
```

**Step 4: weighted-normal 보충 콘텐츠 추가**

```json
"weighted-normal": {
  "title": "음영이 이상하다면?",
  "analogy": {
    "emoji": "🪞",
    "headline": "큰 거울 하나 vs 작은 거울 조각 여러 개",
    "body": "큰 면이 주변 작은 면의 음영 방향을 이끌어서, 평면은 깨끗하고 곡면만 부드럽게 보이게 해요. Shade Smooth만으로는 이 구분이 안 돼요."
  },
  "before_after": {
    "before": "Shade Smooth만 적용하면 평평해야 할 면까지 울퉁불퉁한 음영이 생긴다.",
    "after": "Weighted Normal을 추가하면 면 크기 기반으로 Normal이 재계산되어 평면은 깨끗, 곡면만 부드럽게 보인다."
  },
  "confusion": [
    {
      "symptom": "Weighted Normal을 추가했는데 변화가 없어요.",
      "reason": "Modifier 스택에서 Bevel보다 위에 있거나, Shade Smooth가 적용되지 않은 상태이기 때문이에요.",
      "fix": "Weighted Normal은 반드시 Bevel 아래에 놓고, 오브젝트에 Shade Smooth가 적용되어 있어야 해요."
    },
    {
      "symptom": "Shade Smooth 했는데 평평한 면이 울퉁불퉁해요.",
      "reason": "Auto Smooth 없이 Smooth만 적용하면 모든 면이 무차별적으로 부드러워져서예요.",
      "fix": "Properties → Object Data → Normals에서 Auto Smooth를 활성화하세요."
    }
  ],
  "takeaway": "Weighted Normal은 면 크기 기반으로 노말을 재계산해서 하드서페이스 음영을 정리하는 마무리 도구예요.",
  "targets": ["weighted-normal"]
}
```

**Step 5: join-separate 보충 콘텐츠 추가**

```json
"join-separate": {
  "title": "합치기·나누기가 꼬였다면?",
  "analogy": {
    "emoji": "🧱",
    "headline": "레고 블록을 합치거나 분리하는 거예요",
    "body": "Join(Ctrl+J)은 여러 블록을 하나로 합치고, Separate(P)는 하나의 덩어리에서 일부를 떼어내요. Active Object가 결과의 이름과 Origin을 결정해요."
  },
  "before_after": {
    "before": "Active Object를 신경 쓰지 않고 Join하면 Origin이 엉뚱한 위치로 가서 회전/스케일 기준점이 예상과 달라진다.",
    "after": "Join 전에 Active Object를 신중하게 선택하면 Origin 위치, 이름, 머티리얼 순서를 예측할 수 있다."
  },
  "confusion": [
    {
      "symptom": "Join 했더니 Origin이 이상한 곳으로 갔어요.",
      "reason": "Active Object의 Origin을 따라가기 때문이에요. 마지막에 선택한 오브젝트가 Active가 돼요.",
      "fix": "Join 전에 Shift+클릭 순서를 조절해서 원하는 오브젝트를 마지막에 선택하세요."
    },
    {
      "symptom": "Separate 했는데 메시가 안 나눠져요.",
      "reason": "Object Mode에서는 Separate가 불가능해요. Edit Mode에서만 작동해요.",
      "fix": "Tab으로 Edit Mode 진입 → 분리할 부분 선택 → P → Selection으로 분리하세요."
    }
  ],
  "takeaway": "Join은 합치기, Separate는 나누기. Active Object가 결과의 이름·Origin·머티리얼 순서를 결정해요.",
  "targets": ["join-separate"]
}
```

**Step 6: JSON 유효성 검증**

Run: `python3 -c "import json; json.load(open('course-site/assets/showme/_supplements.json')); print('OK')"`
Expected: `OK`

**Step 7: Commit**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "content: add supplements for 4 core Week 4 cards (boolean, bevel, weighted-normal, join-separate)"
```

---

### Task 2: 보조 카드 14개 보충 콘텐츠 추가

**Files:**
- Modify: `course-site/assets/showme/_supplements.json`

**Step 1: edge-split-modifier, triangulate-modifier, weld-modifier 추가**

```json
"edge-split-modifier": {
  "title": "엣지가 날카롭지 않다면?",
  "analogy": {
    "emoji": "✂️",
    "headline": "종이접기에서 접힌 선을 칼로 갈라놓는 거예요",
    "body": "Edge Split은 날카로워야 할 엣지에서 메시를 실제로 분리해서 Smooth가 넘어가지 않게 해요. Mark Sharp는 표시만 하는 것과 달리 실제 분리예요."
  },
  "before_after": {
    "before": "Auto Smooth만으로 날카로운 엣지가 표현 안 될 때, 각도를 줄이면 다른 곳까지 깨져 보인다.",
    "after": "문제가 되는 엣지에만 Edge Split을 적용하면 해당 엣지만 깔끔하게 갈라진다."
  },
  "confusion": [
    {
      "symptom": "Edge Split과 Mark Sharp의 차이를 모르겠어요.",
      "reason": "Edge Split은 메시를 실제로 분리(버텍스 복제)하고, Mark Sharp는 렌더링 힌트만 남겨요.",
      "fix": "먼저 Auto Smooth + Mark Sharp로 시도하고, 그래도 안 되면 Edge Split을 사용하세요."
    }
  ],
  "takeaway": "Edge Split은 날카로운 엣지를 강제로 만드는 도구예요. Auto Smooth로 해결 안 될 때만 사용하세요.",
  "targets": ["edge-split-modifier"]
},
"triangulate-modifier": {
  "title": "삼각형으로 바꿔야 하나요?",
  "analogy": {
    "emoji": "📐",
    "headline": "사각 타일을 대각선으로 잘라 삼각형으로 바꾸는 거예요",
    "body": "게임 엔진은 삼각형만 처리해요. Triangulate는 사각형 이상의 면을 삼각형으로 분할해서 내보내기에 적합하게 만들어요."
  },
  "before_after": {
    "before": "N-gon(5각형 이상)이 포함된 메시를 게임 엔진으로 내보내면 셰이딩이 깨지거나 면이 사라진다.",
    "after": "Export 직전에 Triangulate를 적용하면 모든 면이 삼각형으로 변환되어 호환성이 보장된다."
  },
  "confusion": [
    {
      "symptom": "모델링 중에 Triangulate를 써도 되나요?",
      "reason": "삼각형은 편집이 어렵고 루프컷 등이 안 돼서 모델링에 부적합해요.",
      "fix": "모델링 중에는 사용하지 말고, Export 직전 마지막 단계에서만 적용하세요."
    }
  ],
  "takeaway": "Triangulate는 내보내기 직전에 적용하는 호환성 도구예요. 모델링 중에는 사용하지 마세요.",
  "targets": ["triangulate-modifier"]
},
"weld-modifier": {
  "title": "버텍스가 겹쳐 있다면?",
  "analogy": {
    "emoji": "⚡",
    "headline": "겹쳐진 점들을 하나로 녹여 붙이는 용접이에요",
    "body": "Weld는 지정 거리 안의 중복 버텍스를 자동으로 합쳐요. Merge by Distance와 같은 효과지만, Modifier라서 비파괴적이에요."
  },
  "before_after": {
    "before": "Boolean이나 Array 후 겹친 버텍스가 남아서 음영 깨짐이나 구멍이 생긴다.",
    "after": "Weld Modifier를 추가하면 중복 버텍스가 자동 합쳐져서 메시가 깨끗해진다."
  },
  "confusion": [
    {
      "symptom": "Merge by Distance와 뭐가 다르나요?",
      "reason": "기능은 같지만, Weld는 Modifier(비파괴적)이고 Merge by Distance는 즉시 적용(파괴적)이에요.",
      "fix": "작업 중에는 Weld Modifier를 쓰고, 최종 정리 시에만 Merge by Distance를 직접 실행하세요."
    }
  ],
  "takeaway": "Weld는 중복 버텍스를 자동 정리하는 비파괴적 도구예요. Boolean·Array 후 정리용으로 사용하세요.",
  "targets": ["weld-modifier"]
}
```

**Step 2: build-modifier, decimate-modifier, remesh-modifier 추가**

```json
"build-modifier": {
  "title": "Build가 안 보인다면?",
  "analogy": {
    "emoji": "🏗️",
    "headline": "벽돌을 하나씩 쌓아올리는 타임랩스예요",
    "body": "Build는 면을 순서대로 하나씩 나타나게 하는 애니메이션 효과예요. 타임라인을 재생해야 효과가 보여요."
  },
  "before_after": {
    "before": "Build Modifier를 추가했는데 아무 변화가 없어서 고장난 줄 안다.",
    "after": "Space로 타임라인을 재생하면 면이 순서대로 나타나는 애니메이션을 확인할 수 있다."
  },
  "confusion": [
    {
      "symptom": "Build를 추가해도 아무것도 안 보여요.",
      "reason": "현재 프레임이 Build 시작 전이거나, 타임라인을 재생하지 않았기 때문이에요.",
      "fix": "타임라인을 1프레임으로 이동한 뒤 Space로 재생하세요."
    }
  ],
  "takeaway": "Build는 면을 순서대로 나타나게 하는 애니메이션 Modifier예요. 타임라인 재생이 필수예요.",
  "targets": ["build-modifier"]
},
"decimate-modifier": {
  "title": "폴리곤을 줄이고 싶다면?",
  "analogy": {
    "emoji": "📉",
    "headline": "고해상도 사진을 저해상도로 압축하는 거예요",
    "body": "Decimate는 메시의 폴리곤 수를 줄여서 파일 크기를 가볍게 해요. 게임이나 AR처럼 성능이 중요한 곳에서 사용해요."
  },
  "before_after": {
    "before": "Ratio를 너무 낮게 설정하면 형태가 무너져서 알아볼 수 없게 된다.",
    "after": "Ratio 0.5부터 시작해서 형태가 유지되는 최저 수준까지 점진적으로 낮추면 최적의 결과를 얻을 수 있다."
  },
  "confusion": [
    {
      "symptom": "폴리곤을 줄였더니 형태가 완전히 무너졌어요.",
      "reason": "Ratio를 한 번에 너무 낮게 설정했기 때문이에요.",
      "fix": "0.5부터 시작해서 0.1씩 줄이며 형태를 확인하세요. Planar 모드도 시도해 보세요."
    }
  ],
  "takeaway": "Decimate는 폴리곤 수를 줄이는 최적화 도구예요. Ratio를 점진적으로 조절하는 게 핵심이에요.",
  "targets": ["decimate-modifier"]
},
"remesh-modifier": {
  "title": "토폴로지가 엉망이라면?",
  "analogy": {
    "emoji": "🔲",
    "headline": "울퉁불퉁한 점토를 균일한 격자로 다시 찍어내는 거예요",
    "body": "Remesh는 기존 메시의 형태를 유지하면서 토폴로지를 균일한 격자로 재구성해요. 스컬프팅 준비에 많이 써요."
  },
  "before_after": {
    "before": "Voxel Size가 너무 크면 디테일이 뭉개져서 원래 형태를 잃는다.",
    "after": "Voxel Size를 작게(0.02~0.05) 설정하면 원래 형태를 유지하면서 균일한 토폴로지를 얻을 수 있다."
  },
  "confusion": [
    {
      "symptom": "Remesh 후 디테일이 다 사라졌어요.",
      "reason": "Voxel Size가 너무 커서 세부 형태가 뭉개진 거예요.",
      "fix": "Voxel Size 값을 줄이세요. 오브젝트 크기에 따라 0.01~0.05 범위가 적절해요."
    }
  ],
  "takeaway": "Remesh는 불규칙한 토폴로지를 균일한 격자로 재구성하는 도구예요. Voxel Size 조절이 핵심이에요.",
  "targets": ["remesh-modifier"]
}
```

**Step 3: screw-modifier, skin-modifier, wireframe-modifier 추가**

```json
"screw-modifier": {
  "title": "회전체가 안 만들어진다면?",
  "analogy": {
    "emoji": "🌀",
    "headline": "도자기 물레에 프로파일을 돌려 형태를 만드는 거예요",
    "body": "Screw는 단면(프로파일)을 축 중심으로 회전시켜 3D 형태를 만들어요. 컵, 꽃병, 나사처럼 축 대칭인 물체에 적합해요."
  },
  "before_after": {
    "before": "프로파일이 축 위에 있으면 회전해도 면이 생기지 않는다.",
    "after": "프로파일을 축에서 적절히 떨어뜨리면 회전 시 원하는 3D 형태가 만들어진다."
  },
  "confusion": [
    {
      "symptom": "Screw를 추가해도 회전체가 안 생겨요.",
      "reason": "프로파일(커브나 엣지)이 회전축 위에 있거나 Origin 위치가 잘못된 거예요.",
      "fix": "Origin을 회전축 중심에 놓고, 프로파일은 축에서 떨어뜨려 배치하세요."
    }
  ],
  "takeaway": "Screw는 단면을 축 중심으로 회전시켜 3D 형태를 만드는 도구예요. Origin 위치가 핵심이에요.",
  "targets": ["screw-modifier"]
},
"skin-modifier": {
  "title": "뼈대에 살을 입히고 싶다면?",
  "analogy": {
    "emoji": "🦠",
    "headline": "와이어 뼈대에 살을 입히는 거예요",
    "body": "Skin은 점과 선으로 이루어진 뼈대에 메시 표면을 자동으로 생성해요. 나뭇가지, 촉수, 유기체 형태에 적합해요."
  },
  "before_after": {
    "before": "모든 버텍스가 같은 두께라 밋밋하고 덩어리처럼 보인다.",
    "after": "버텍스마다 Ctrl+A로 두께를 조절하면 가지가 갈라지는 자연스러운 형태가 만들어진다."
  },
  "confusion": [
    {
      "symptom": "전체가 하나의 덩어리로 뭉쳐요.",
      "reason": "모든 버텍스의 반경이 동일하게 설정되어 있기 때문이에요.",
      "fix": "각 버텍스를 선택하고 Ctrl+A로 X/Y 반경을 개별 조절하세요."
    }
  ],
  "takeaway": "Skin은 뼈대에 메시 표면을 자동 생성하는 도구예요. 버텍스별 Ctrl+A 두께 조절이 핵심이에요.",
  "targets": ["skin-modifier"]
},
"wireframe-modifier": {
  "title": "와이어프레임을 만들고 싶다면?",
  "analogy": {
    "emoji": "🕸️",
    "headline": "건축 모형의 뼈대만 남기는 거예요",
    "body": "Wireframe은 엣지를 따라 와이어프레임 형태의 메시를 생성해요. 건축 모형, 장식 패턴, 과학 시각화에 사용해요."
  },
  "before_after": {
    "before": "Replace Original이 켜져 있으면 원래 면이 사라지고 와이어만 남는다.",
    "after": "Replace Original을 끄면 원래 오브젝트 위에 와이어프레임이 겹쳐서 장식 효과가 된다."
  },
  "confusion": [
    {
      "symptom": "면이 다 사라지고 선만 보여요.",
      "reason": "Replace Original이 기본 켜짐이라 원래 면이 와이어로 대체된 거예요.",
      "fix": "Modifier 패널에서 Replace Original 체크를 해제하세요."
    }
  ],
  "takeaway": "Wireframe은 엣지를 따라 와이어프레임 메시를 생성하는 도구예요. Replace Original 옵션에 주의하세요.",
  "targets": ["wireframe-modifier"]
}
```

**Step 4: mask-modifier, multiresolution-modifier, volume-to-mesh, curve-to-tube, scatter-on-surface 추가**

```json
"mask-modifier": {
  "title": "일부만 숨기고 싶다면?",
  "analogy": {
    "emoji": "🎭",
    "headline": "무대 조명처럼 원하는 부분만 비추는 거예요",
    "body": "Mask는 Vertex Group에 포함된 부분만 보여주고 나머지를 숨겨요. 복잡한 모델에서 특정 영역만 작업할 때 유용해요."
  },
  "before_after": {
    "before": "Vertex Group을 지정하지 않으면 Mask를 추가해도 아무 변화가 없다.",
    "after": "Vertex Group을 만들고 Mask에 지정하면 해당 그룹에 포함된 부분만 표시된다."
  },
  "confusion": [
    {
      "symptom": "Mask를 적용해도 아무것도 안 숨겨져요.",
      "reason": "Vertex Group이 비어 있거나 지정되지 않았기 때문이에요.",
      "fix": "먼저 Edit Mode에서 숨길/보여줄 영역을 Vertex Group으로 지정한 뒤 Mask에 연결하세요."
    }
  ],
  "takeaway": "Mask는 Vertex Group 기반으로 메시 일부를 숨기는 도구예요. Vertex Group 설정이 선행되어야 해요.",
  "targets": ["mask-modifier"]
},
"multiresolution-modifier": {
  "title": "스컬프팅 해상도를 조절하고 싶다면?",
  "analogy": {
    "emoji": "🔍",
    "headline": "지도의 줌 레벨처럼 디테일 단계를 조절하는 거예요",
    "body": "Multiresolution은 여러 해상도 레벨에서 독립적으로 스컬프팅할 수 있게 해요. 낮은 레벨에서 큰 형태, 높은 레벨에서 세부 디테일을 잡아요."
  },
  "before_after": {
    "before": "Subdivision 레벨을 안 올리면 Sculpt 모드에서 디테일을 잡을 수 없다.",
    "after": "Subdivide 버튼으로 레벨을 올린 뒤 각 레벨에서 독립적으로 디테일을 추가할 수 있다."
  },
  "confusion": [
    {
      "symptom": "Sculpt 모드에서 디테일이 안 잡혀요.",
      "reason": "Subdivision 레벨이 낮아서 버텍스가 부족한 거예요.",
      "fix": "Modifier 패널에서 Subdivide를 눌러 레벨을 올리세요. 레벨 3~4부터 디테일 작업이 가능해요."
    }
  ],
  "takeaway": "Multiresolution은 해상도 레벨별로 독립 스컬프팅이 가능한 도구예요. SubSurf와 달리 각 레벨을 따로 편집할 수 있어요.",
  "targets": ["multiresolution-modifier"]
},
"volume-to-mesh": {
  "title": "볼륨을 메시로 바꾸고 싶다면?",
  "analogy": {
    "emoji": "💨",
    "headline": "안개를 얼려서 고체로 만드는 거예요",
    "body": "Volume to Mesh는 볼륨 데이터(연기, 유체 등)를 메시 표면으로 변환해요. 시뮬레이션 결과를 편집 가능한 메시로 만들 때 사용해요."
  },
  "before_after": {
    "before": "Volume to Mesh가 메뉴에 안 보이거나 적용해도 결과가 없다.",
    "after": "먼저 Mesh to Volume으로 볼륨을 만든 뒤 Volume to Mesh를 적용하면 메시로 변환된다."
  },
  "confusion": [
    {
      "symptom": "Volume to Mesh가 메뉴에 없어요.",
      "reason": "선택한 오브젝트가 볼륨 타입이 아니기 때문이에요.",
      "fix": "먼저 Mesh to Volume Modifier로 볼륨 오브젝트를 만들거나, 시뮬레이션 캐시에서 볼륨을 가져오세요."
    }
  ],
  "takeaway": "Volume to Mesh는 볼륨 데이터를 편집 가능한 메시로 변환하는 도구예요. 볼륨 오브젝트가 선행되어야 해요.",
  "targets": ["volume-to-mesh"]
},
"curve-to-tube": {
  "title": "커브로 파이프를 만들고 싶다면?",
  "analogy": {
    "emoji": "🔄",
    "headline": "호스를 경로를 따라 배치하는 거예요",
    "body": "Curve에 Bevel Depth를 주면 경로를 따라 파이프 형태가 자동으로 생성돼요. 케이블, 파이프, 로프에 적합해요."
  },
  "before_after": {
    "before": "커브만 있고 Bevel Depth가 0이면 경로 선만 보이고 파이프가 안 만들어진다.",
    "after": "Curve Properties → Geometry → Bevel Depth를 0 이상으로 설정하면 파이프가 생성된다."
  },
  "confusion": [
    {
      "symptom": "커브가 보이는데 튜브가 안 생겨요.",
      "reason": "Bevel Depth가 기본값 0이라 두께가 없기 때문이에요.",
      "fix": "Properties → Object Data → Geometry → Bevel Depth 값을 0.01 이상으로 설정하세요."
    }
  ],
  "takeaway": "Curve to Tube는 커브 경로에 Bevel Depth를 줘서 파이프를 만드는 기법이에요. Depth 설정이 핵심이에요.",
  "targets": ["curve-to-tube"]
},
"scatter-on-surface": {
  "title": "표면에 오브젝트를 뿌리고 싶다면?",
  "analogy": {
    "emoji": "🌿",
    "headline": "잔디밭에 씨앗을 뿌리는 거예요",
    "body": "Geometry Nodes 기반으로 표면 위에 오브젝트를 자동 분산 배치해요. 풀, 돌, 나무 등 환경 구성에 적합해요."
  },
  "before_after": {
    "before": "인스턴스 설정 없이 Distribute Points만 하면 점만 보이고 오브젝트가 나타나지 않는다.",
    "after": "Instance on Points 노드로 오브젝트를 연결하면 각 점 위치에 인스턴스가 배치된다."
  },
  "confusion": [
    {
      "symptom": "오브젝트가 하나만 생기거나 점만 보여요.",
      "reason": "Geometry Nodes에서 Instance on Points 설정이 빠져 있기 때문이에요.",
      "fix": "Distribute Points on Faces → Instance on Points → 대상 오브젝트 연결 순서로 노드를 구성하세요."
    }
  ],
  "takeaway": "Scatter는 Geometry Nodes 기반 분산 배치 도구예요. Distribute + Instance on Points 조합이 기본이에요.",
  "targets": ["scatter-on-surface"]
}
```

**Step 5: JSON 유효성 검증**

Run: `python3 -c "import json; data=json.load(open('course-site/assets/showme/_supplements.json')); print(f'Total entries: {len(data)}'); print('OK')"`
Expected: `Total entries: [기존수+19]`, `OK`

**Step 6: Commit**

```bash
git add course-site/assets/showme/_supplements.json
git commit -m "content: add supplements for 14 auxiliary Week 4 cards"
```

---

## Phase 2: 핵심 카드 HTML 보강

### Task 3: boolean-modifier.html — 원인→결과 + 흔한 실수 섹션 추가

**Files:**
- Modify: `course-site/assets/showme/boolean-modifier.html`

**Step 1: Usage 탭에서 tip-box 앞에 원인→결과 섹션 삽입**

`boolean-modifier.html`의 Usage 탭(panel-when) 내부, `<div class="combo-section">` 앞에 아래 HTML 추가:

```html
<hr class="section-divider">

<div class="cause-effect">
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Scale 미적용 상태에서 Boolean Difference</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>비대칭 구멍 — 커터와 대상의 Scale이 달라 의도한 형태가 안 됨</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>커터 오브젝트를 Apply 전에 삭제</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>Boolean Modifier가 참조를 잃어 무효화 — 원래 형태로 복귀</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Overlap Threshold 미조정 (면이 정확히 겹칠 때)</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>면 깜빡임(Z-fighting) 또는 Boolean 실패</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Apply Scale 후 Exact Solver로 Boolean 적용</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-success"><span class="ce-label">결과</span>깨끗한 Boolean 결과 — 토폴로지도 예측 가능</div>
  </div>
</div>
```

**Step 2: combo-section을 "흔한 실수 & 해결법"으로 변경**

기존 `<div class="combo-section">`의 `<h4>` 내용과 카드를 아래로 교체:

```html
<div class="combo-section">
  <h4>흔한 실수 & 해결법</h4>
  <div class="combo-grid">
    <div class="combo-card">
      <div class="combo-name">커터를 삭제해서 Boolean이 풀림</div>
      <div class="combo-desc">커터는 <span class="kbd">H</span>로 숨기세요. Modifier Apply 후에야 삭제 가능합니다.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">Boolean 후 안쪽 면이 까맣게 보임</div>
      <div class="combo-desc">Normal이 뒤집힘. Edit Mode → <span class="kbd">Shift</span>+<span class="kbd">N</span> (Recalculate Outside).</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">복잡한 형태에서 Boolean 실패</div>
      <div class="combo-desc">Fast Solver 대신 Exact Solver를 사용하세요. 느리지만 정확합니다.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">Boolean 후 토폴로지가 지저분함</div>
      <div class="combo-desc">Apply 후 Edit Mode에서 불필요한 면 정리. LoopTools나 Grid Fill 활용.</div>
    </div>
  </div>
</div>
```

**Step 3: cause-effect CSS 확인**

boolean-modifier.html의 `<style>` 블록에 `.cause-effect`, `.ce-row`, `.ce-cause`, `.ce-result`, `.ce-arrow`, `.ce-label`, `.result-warn`, `.result-success`, `.section-divider` CSS가 있는지 확인. 없으면 transform-apply.html에서 해당 CSS 블록을 복사해 추가.

**Step 4: 브라우저에서 시각 확인**

boolean-modifier.html을 직접 열어 Usage 탭의 원인→결과 섹션과 흔한 실수 카드가 정상 렌더링되는지 확인.

**Step 5: Commit**

```bash
git add course-site/assets/showme/boolean-modifier.html
git commit -m "content(boolean): add cause-effect section and common mistakes to usage tab"
```

---

### Task 4: bevel-modifier.html — 원인→결과 + 흔한 실수 + "쓰지 말 것" 보강

**Files:**
- Modify: `course-site/assets/showme/bevel-modifier.html`

**Step 1: Usage 탭에 원인→결과 섹션 삽입**

combo-section 앞에 추가:

```html
<hr class="section-divider">

<div class="cause-effect">
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Scale 미적용 상태에서 Bevel Modifier</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>축마다 Bevel 폭이 달라져 비균일한 모서리</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Segments를 과도하게 높임 (6 이상)</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>불필요한 폴리곤 증가 — 성능 저하 및 편집 복잡도 상승</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Limit Method: None 상태</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>의도하지 않은 모서리까지 전부 Bevel 적용</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Weight 방식 + Weighted Normal 조합 적용</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-success"><span class="ce-label">결과</span>원하는 모서리만 깔끔하게 Bevel + 음영 정리</div>
  </div>
</div>
```

**Step 2: combo-section을 "흔한 실수 & 해결법"으로 교체**

```html
<div class="combo-section">
  <h4>흔한 실수 & 해결법</h4>
  <div class="combo-grid">
    <div class="combo-card">
      <div class="combo-name">모든 모서리에 균일 Bevel이 걸림</div>
      <div class="combo-desc">Limit Method를 Weight로 변경 → <span class="kbd">Ctrl</span>+<span class="kbd">Shift</span>+<span class="kbd">E</span>로 원하는 엣지에 가중치 부여.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">Bevel 후 음영이 지저분함</div>
      <div class="combo-desc">Bevel 아래에 Weighted Normal Modifier를 추가하세요. 스택 순서가 중요합니다.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">Bevel Tool과 Modifier 혼동</div>
      <div class="combo-desc">Tool(<span class="kbd">Ctrl</span>+<span class="kbd">B</span>)은 즉시 적용, Modifier는 비파괴적. 수정 가능성이 있으면 Modifier.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">비균일 Scale에서 Bevel 찌그러짐</div>
      <div class="combo-desc"><span class="kbd">Ctrl</span>+<span class="kbd">A</span> → Apply Scale 후 Bevel을 적용하세요.</div>
    </div>
  </div>
</div>
```

**Step 3: "쓰지 말 것" 항목 2개 추가**

Usage 탭의 "사용하지 말아야 할 때" 리스트에 2개 항목 추가:
- "유기체 모델링에는 Subdivision Surface가 더 적합"
- "모서리 하나만 깎을 때는 Bevel Tool(Ctrl+B)이 더 빠름"

**Step 4: cause-effect CSS 확인 및 추가** (Task 3과 동일 패턴)

**Step 5: 시각 확인 후 Commit**

```bash
git add course-site/assets/showme/bevel-modifier.html
git commit -m "content(bevel): add cause-effect, common mistakes, expand usage-not items"
```

---

### Task 5: weighted-normal.html — 개념 보강 + 원인→결과 + 흔한 실수 + 단축키 수정

**Files:**
- Modify: `course-site/assets/showme/weighted-normal.html`

**Step 1: 개념 탭에 3번째 개념 카드 추가**

기존 2개 concept-card 뒤에 추가:

```html
<div class="concept-card accent-b">
  <h4>Auto Smooth와의 관계</h4>
  <p>Shade Smooth는 모든 면을 부드럽게 만들지만, <strong>Auto Smooth</strong>는 각도 기준으로 날카로운 엣지를 보존해요.</p>
  <p>Weighted Normal은 여기서 한 단계 더 나아가서, <strong>면 크기(Face Area)</strong> 기반으로 Normal을 재계산해요. 큰 면이 주변 작은 면의 음영 방향을 이끌어서 하드서페이스에 적합한 깨끗한 음영을 만들어요.</p>
  <p><strong>적용 순서:</strong> Shade Smooth → Auto Smooth 활성화 → Weighted Normal Modifier 추가</p>
</div>
```

**Step 2: 단축키 섹션 수정**

Ctrl+1~5 항목을 제거하고, 정확한 접근 경로로 교체:

```html
<div class="shortcut-list">
  <div class="shortcut-row">
    <span class="kbd">Right-click</span> <span class="shortcut-desc">→ Shade Smooth (Object Mode에서 오브젝트 우클릭)</span>
  </div>
  <div class="shortcut-row">
    <span class="shortcut-desc">Properties → Object Data → Normals → Auto Smooth 활성화</span>
  </div>
  <div class="shortcut-row">
    <span class="shortcut-desc">Properties → Modifier → Add Modifier → Weighted Normal</span>
  </div>
</div>
```

**Step 3: Usage 탭에 원인→결과 섹션 삽입**

```html
<hr class="section-divider">

<div class="cause-effect">
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Shade Smooth만 적용, WN 없음</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>평면에 울퉁불퉁한 음영 왜곡 발생</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>WN이 Bevel 위에 위치 (스택 순서 오류)</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>Bevel이 만든 면에 WN 효과가 적용되지 않음</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Shade Flat 상태에서 WN 추가</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-warn"><span class="ce-label">결과</span>WN은 Smooth 기반이라 Flat에서는 효과 없음</div>
  </div>
  <div class="ce-row">
    <div class="ce-cause"><span class="ce-label">원인</span>Bevel 아래에 WN + Face Influence 활성화</div>
    <div class="ce-arrow">→</div>
    <div class="ce-result result-success"><span class="ce-label">결과</span>Bevel 면까지 깨끗한 음영 — 하드서페이스 마무리 완성</div>
  </div>
</div>
```

**Step 4: 흔한 실수 & 해결법 섹션 추가**

combo-section 내용을 교체 또는 추가:

```html
<div class="combo-section">
  <h4>흔한 실수 & 해결법</h4>
  <div class="combo-grid">
    <div class="combo-card">
      <div class="combo-name">Modifier 스택 순서가 잘못됨</div>
      <div class="combo-desc">Weighted Normal은 반드시 Bevel 아래에 놓으세요. 가장 마지막 Modifier여야 합니다.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">Shade Smooth를 빼먹음</div>
      <div class="combo-desc">WN은 Smooth Shading 기반이에요. Object Mode에서 Right-click → Shade Smooth 필수.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">Auto Smooth 미활성화</div>
      <div class="combo-desc">Properties → Object Data → Normals에서 Auto Smooth를 켜야 WN이 제대로 작동합니다.</div>
    </div>
    <div class="combo-card">
      <div class="combo-name">Bevel 조합 시 Face Influence 미사용</div>
      <div class="combo-desc">WN Modifier에서 Face Influence 체크를 켜면 Bevel 면까지 깨끗한 음영이 적용됩니다.</div>
    </div>
  </div>
</div>
```

**Step 5: cause-effect CSS 확인 및 추가**

**Step 6: 시각 확인 후 Commit**

```bash
git add course-site/assets/showme/weighted-normal.html
git commit -m "content(weighted-normal): add concept card, fix shortcuts, add cause-effect and common mistakes"
```

---

### Task 6: 전체 검증

**Files:**
- Verify: `course-site/assets/showme/_supplements.json`
- Verify: `course-site/assets/showme/boolean-modifier.html`
- Verify: `course-site/assets/showme/bevel-modifier.html`
- Verify: `course-site/assets/showme/weighted-normal.html`

**Step 1: JSON 유효성 최종 확인**

Run: `python3 -c "import json; data=json.load(open('course-site/assets/showme/_supplements.json')); print(f'Total: {len(data)} entries'); [print(f'  {k}') for k in sorted(data.keys()) if k in ['boolean-modifier','bevel-modifier','weighted-normal','join-separate','edge-split-modifier','triangulate-modifier','weld-modifier','build-modifier','decimate-modifier','remesh-modifier','screw-modifier','skin-modifier','wireframe-modifier','mask-modifier','multiresolution-modifier','volume-to-mesh','curve-to-tube','scatter-on-surface']]"`

**Step 2: HTML 구문 확인**

Run: `for f in boolean-modifier bevel-modifier weighted-normal; do python3 -c "from html.parser import HTMLParser; p=HTMLParser(); p.feed(open('course-site/assets/showme/$f.html').read()); print('$f: OK')"; done`

**Step 3: 브라우저에서 각 카드의 Usage 탭 시각 확인**

각 카드를 직접 열어:
- 원인→결과 섹션의 레이아웃이 transform-apply와 동일한지
- 흔한 실수 카드 4개가 정상 렌더링되는지
- 반응형(모바일)에서 깨지지 않는지

**Step 4: 최종 Commit (필요 시)**

```bash
git add -A
git commit -m "content: Week 4 card quality upgrade complete — 19 supplements + 3 HTML enhancements"
```
