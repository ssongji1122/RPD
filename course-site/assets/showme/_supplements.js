// ============================================================
// Show Me 보충 설명 데이터
// 개념이해 탭 하단 "아직 헷갈린다면?" accordion에 표시
// targets 배열로 여러 카드에서 재사용 가능
// ============================================================

const SHOWME_SUPPLEMENTS = {
  // /brainstormC 스킬로 항목 추가
  // 구조:
  // "supplement-id": {
  //   title: "아직 헷갈린다면?",
  //   analogy: { source: "요리|일상|게임|디지털", emoji: "🍕", headline: "...", body: "..." } | null,
  //   before_after: { before: "...", after: "..." },
  //   takeaway: "핵심 한 줄",
  //   targets: ["card-id-1", "card-id-2"]
  // }
  "extrude": {
    title: "아직 헷갈린다면?",
    analogy: null,
    before_after: {
      before: "큐브 하나에서 팔 모양을 만들려면 별도 오브젝트를 추가한 뒤 붙여야 해서, 한 오브젝트 안에서 형태를 이어가기 어렵다.",
      after: "팔이 될 면을 선택하고 E를 누르면, 그 면에서 새 지오메트리가 기존 메시에 연결된 채로 뽑혀 나와 하나의 오브젝트 안에서 형태를 계속 키울 수 있다."
    },
    takeaway: "Extrude는 기존 메시에서 새 부분을 연결된 채로 뽑아내는 작업이라, 같은 오브젝트 안에서 형태를 계속 늘려나갈 수 있다.",
    targets: ["extrude"]
  }
};
