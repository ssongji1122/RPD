# 리서치 브리프: 미러 모디파이어 (Mirror Modifier)
> 생성일: 2026-03-17 | Blender 4.3+ 기준

## 1. 공식 정의
- **영문**: The Mirror modifier mirrors a mesh along its local X, Y and/or Z axes, across the Object Origin. It allows modeling with symmetry — you model one half of an object and the modifier automatically generates the opposite half.
- **한글 풀이**: 오브젝트의 원점(Origin)을 기준으로 메시를 X, Y, Z 축 중 선택한 축에 대해 거울처럼 복사해요. 한쪽만 모델링하면 반대쪽이 자동으로 만들어지는 비파괴 방식이에요.
- **공식 문서**: [Mirror Modifier — Blender Manual](https://docs.blender.org/manual/en/latest/modeling/modifiers/generate/mirror.html)

## 2. 핵심 파라미터
| 파라미터 | 기본값 | 설명 | 학생에게 중요한 이유 |
|---------|-------|------|-------------------|
| Axis (X/Y/Z) | X만 활성 | 미러할 축 선택. 복수 선택 가능 | 캐릭터는 X축, 바닥 반사는 Z축 — 축이 뒤바뀌면 결과가 완전히 달라져요 |
| Bisect | Off | 기존 메시를 미러 평면에서 잘라내기 | 이미 양쪽이 있는 오브젝트에 미러를 걸 때 한쪽을 자동으로 잘라줘요 |
| Flip | Off | Bisect로 남길 쪽을 반전 | Bisect와 세트로 사용 — 잘못된 쪽이 남았을 때 토글 |
| Mirror Object | None | 외부 오브젝트(보통 Empty)를 미러 중심으로 사용 | 원점이 아닌 다른 위치를 기준으로 미러하고 싶을 때. 애니메이션에도 활용 가능 |
| Clipping | Off | Edit Mode에서 버텍스가 미러 평면을 넘지 못하게 차단 | **반드시 켜야 하는 옵션** — 안 켜면 중앙 이음새가 벌어져요 |
| Merge | On | 미러 경계의 가까운 버텍스를 자동 병합 | 중앙선에 틈이 생기는 걸 방지. Merge Distance와 함께 조절 |
| Merge Distance | 0.001m | 병합 거리 임계값 | 너무 크면 의도치 않은 버텍스가 합쳐지고, 너무 작으면 틈이 생겨요 |
| UV Offset (U/V) | Off | 미러된 쪽의 UV를 U 또는 V 방향으로 오프셋 | UV 베이킹 시 좌우가 겹치는 문제를 해결. 텍스처 작업에서 중요 |
| Vertex Groups | Off | .L/.R 명명규칙에 따라 버텍스 그룹을 미러 | 리깅/웨이트 페인팅에서 좌우 대칭 작업 시 필수 |

## 3. 단축키
| 키 | 동작 | 컨텍스트 | 비고 |
|----|------|---------|------|
| Ctrl+1~5 | 모디파이어 스택 N번째 추가 | Object Mode | Subdivision에 주로 사용, Mirror는 직접 메뉴에서 추가 |
| Ctrl+A | Apply All Transforms | Object Mode | Mirror 추가 전에 반드시 실행 — 스케일/회전 초기화 |
| Shift+S → Cursor to World Origin | 3D 커서를 월드 원점으로 | 모든 모드 | 원점 리셋 시 자주 사용 |
| 우클릭 → Set Origin → Origin to 3D Cursor | 원점을 3D 커서 위치로 | Object Mode | 미러 기준점 조정의 핵심 |
| Shift+Ctrl+M | Mirror (Mesh) | Edit Mode | 선택한 메시를 축 기준으로 뒤집기 (모디파이어와 다름) |

## 4. 연관 개념 그래프

### 선수 지식 (이걸 모르면 이해 불가)
- **오브젝트 원점 (Object Origin)**: Mirror 모디파이어의 미러 기준점. 원점이 어디 있느냐에 따라 미러 결과가 완전히 달라져요. "미러가 이상해요" 질문의 90%는 원점 문제예요.
- **Transform Apply (Ctrl+A)**: 스케일이나 회전을 적용하지 않으면 미러 축이 예상과 다르게 동작해요. 모디파이어 추가 전 반드시 Apply.
- **Edit Mode vs Object Mode**: Edit Mode에서 움직여야 미러가 유지되고, Object Mode에서 움직이면 원점이 따라 이동해서 미러가 깨져요.

### 연결 개념 (함께 쓰이는 것)
- **Subdivision Surface**: Mirror로 반쪽 → Subdivision으로 매끄럽게. 모디파이어 스택에서 Mirror가 위, Subdivision이 아래.
- **Clipping + Merge**: 중앙선 이음새를 깔끔하게 만드는 세트. 둘 다 켜야 완벽.
- **Empty Object**: Mirror Object로 지정하면 원점과 무관하게 미러 기준을 자유롭게 배치 가능.

### 심화 (알면 이해가 깊어지는 것)
- **모디파이어 스택 순서**: Mirror → Subdivision 순서가 중요. 순서가 바뀌면 Subdivision이 먼저 적용된 후 미러되어 에지 흐름이 꼬여요.
- **비파괴 워크플로우**: Apply 하지 않고 작업하면 언제든 미러를 끄거나 축을 바꿀 수 있어요. 최대한 늦게 Apply.
- **대칭 토폴로지의 원리**: 미러는 단순 복사가 아니라 버텍스 좌표의 부호를 반전시키는 거예요 (X축 미러 → x좌표 × -1).

## 5. 학생 혼란 포인트
| # | 질문 (실제) | 출처 | 핵심 원인 | 검증된 답변 |
|---|-----------|------|----------|-----------|
| 1 | "미러가 안되는데 왜 이러죠?" | [DC블렌더갤](https://m.dcinside.com/board/blender/17275) | 원점(Origin)이 메시 중심이 아닌 곳에 있음 | Shift+S → Cursor to World Origin → 우클릭 Set Origin → Origin to 3D Cursor |
| 2 | "미러가 이상한 방향으로 돼요" | [DC블렌더갤](https://gall.dcinside.com/mgallery/board/view/?id=blender&no=14122) | Object Mode에서 회전/스케일 후 Apply 안 함 | Ctrl+A → All Transforms 적용 후 미러 추가 |
| 3 | "중앙에 선이 벌어져요 / 틈이 생겨요" | 커뮤니티 공통 | Clipping 미활성 + 버텍스가 미러 평면을 넘음 | Clipping 체크, Merge Distance 조정 (0.001m) |
| 4 | "양쪽 다 있는데 미러 걸었더니 4배가 돼요" | [KatsBits](https://www.katsbits.com/codex/mirror/) | 미러 전에 한쪽을 삭제하지 않음 | 미러 추가 전 반대편 메시를 삭제하거나, Bisect 옵션 활용 |
| 5 | "Edit Mode에서 한쪽만 움직이는데 반대쪽은 안 따라와요" | 커뮤니티 공통 | 미러된 쪽은 프로시저럴(자동생성)이라 직접 편집 불가 | 정상 동작. 원본 쪽을 편집하면 반대쪽이 자동 반영됨 |
| 6 | "미러 적용(Apply) 후 반대쪽 버텍스가 분리돼 있어요" | StackExchange 패턴 | Apply 시 Merge가 적용되지만 Distance 밖의 버텍스는 분리 상태 | Apply 전에 Merge Distance 확인. Apply 후 Merge by Distance (M키) 추가 실행 |

## 6. 흔한 실수 & 해결
| 증상 | 원인 | 해결 |
|------|------|------|
| 미러가 엉뚱한 위치에 나타남 | 원점이 메시 중심이 아님 | Shift+S → Cursor to World Origin, Set Origin → Origin to 3D Cursor |
| 미러 축이 틀어져 있음 | Object Mode에서 회전 후 Apply 안 함 | Ctrl+A → All Transforms 적용 |
| 중앙 이음새가 벌어짐 | Clipping 비활성 | Mirror 모디파이어에서 Clipping ✅ 체크 |
| 미러 추가 후 오브젝트가 2배가 됨 | 이미 완성된 대칭 모델에 미러 추가 | 한쪽 절반 삭제 후 미러 추가, 또는 Bisect 사용 |
| Edit Mode에서 버텍스가 미러선을 넘어감 | Clipping이 꺼져 있음 | Clipping 켜기 — 켜면 미러 평면이 "벽"처럼 작용 |
| Apply 후 중앙에 이중 버텍스 | Merge Distance가 너무 작았음 | Apply 후 전체 선택 → M → Merge by Distance |

## 7. 추천 비유 후보
1. **거울 앞에 선 자신** — 거울(미러 평면) 앞에 서면 반대쪽이 똑같이 움직이죠? 오른손을 올리면 거울 속 왼손이 올라가요. Mirror Modifier가 정확히 이거예요. 거울 위치(원점)가 어디냐에 따라 반사 결과가 달라지는 것까지 같아요.
2. **종이 반 접기** — 종이를 반으로 접고 한쪽에만 그림을 그리면 펼쳤을 때 양쪽이 똑같아요. Bisect = 종이를 접는 선, Clipping = 접힌 선 너머로 펜이 안 넘어가게 막는 거예요.
3. **잉크 블롯 테스트 (로르샤흐)** — 잉크를 한쪽에 떨어뜨리고 접으면 양쪽이 대칭. 잉크가 아직 마르지 않았을 때(Apply 전)는 한쪽을 고치면 반대쪽도 바뀌지만, 마른 후(Apply 후)에는 각각 독립이에요.

## 8. 크로스체크 로그
| 주장 | 소스 | 검증 | 결과 |
|------|------|------|------|
| Mirror 기본 축은 X | [Polyfable](https://polyfable.com/tutorials/blender-mirror-modifier/), [GameDevTraum](https://gamedevtraum.com/en/blender-tutorials-and-curiosities/how-to-mirror-objects-in-blender-mirror-modifier/) | Blender 공식 문서 확인 | ✅ 정확 — 기본값 X축만 활성 |
| Clipping은 기본 Off | [Polyfable](https://polyfable.com/tutorials/blender-mirror-modifier/) | 공식 문서 기본값 대조 | ✅ 정확 — 기본 Off, 수동 활성 필요 |
| Merge Distance 기본값 0.001m | 커뮤니티 공통 | Blender 4.3 기본값 확인 | ✅ 정확 |
| "Object Mode 변환이 미러 문제의 주원인" | [Skillademia](https://www.skillademia.com/3d/blender/how-to-use-the-mirror-modifier-in-blender/) | 공식 문서 + 커뮤니티 패턴 | ✅ 정확 — Apply Transforms가 선행 필수 |
| "Clipping 켜면 되돌릴 수 없다" | [KatsBits](https://www.katsbits.com/codex/mirror/) | 공식 문서 확인 | ⚠️ 부분 정확 — Clipping 자체는 토글 가능. 단, Clipping 상태에서 미러선 위로 이동한 버텍스는 미러선에 "붙어" 버려서, Clipping을 끄더라도 원위치로 자동 복귀하지 않음 |
| "미러 중심은 항상 오브젝트 원점" | [유정통 3D](https://yujungtong.com/%EB%B8%94%EB%A0%8C%EB%8D%94-%EB%AF%B8%EB%9F%AC-mirror-%EC%A2%8C%EC%9A%B0%EB%B0%98%EC%A0%84%ED%95%98%EA%B8%B0/) | 공식 문서 확인 | ⚠️ 부분 정확 — 기본적으로 원점 기준이지만 Mirror Object 설정으로 다른 오브젝트를 기준으로 변경 가능 |
