// 기말 작품을 화면에 보여 줄 때 쓰는 공통 규칙. 필름스트립과 작품 상세가 같은 함수를
// 써야 제목·개수가 화면마다 달라지지 않는다. 규칙 문서: docs/final-projects-rules.md
import type { FPLink, FPMedia, FPNote, FPProject } from './finalProjects';
import { FP_EXCLUDE } from './fpCuration';

const CURATION_ROOT = 'assets/final-projects/';

// 로더가 src 앞에 배포 base(/RPD/)를 붙이므로 큐레이션 키는 데이터 원형으로 되돌려 대조한다.
export const curationKey = (src: string) => src.slice(src.indexOf(CURATION_ROOT));
export const isExcluded = (m: FPMedia) => FP_EXCLUDE.has(curationKey(m.src));

/** 작품명이 확인된 작품은 작품명, 아니면 익명 코드(Project NN). */
export const displayTitle = (p: FPProject) => p.workTitle ?? p.title;

/** 화면에 실제로 보이는 것만 센다. 이미지는 완성 컷만, 과정 캡처는 따로 센다. */
export function projectCounts(p: FPProject) {
  const shown = p.media.filter((m) => !isExcluded(m));
  return {
    images: shown.filter((m) => m.type === 'image' && m.role !== 'process').length,
    videos: p.videos.length || shown.filter((m) => m.type === 'video').length,
    process: shown.filter((m) => m.role === 'process').length,
  };
}

// Canva 단축 링크(canva.link)는 학생 공유 설정에 따라 누구에게나 편집 화면으로 열리므로,
// 빌드 데이터에 해석해 둔 보기 전용 주소(view)로 연다.
const CANVA_EMBED_SUFFIX = /\?embed$/;
export const canvaViewUrl = (l: FPLink) => (l.embedUrl ? l.embedUrl.replace(CANVA_EMBED_SUFFIX, '') : null);
export const publicLinkUrl = (l: FPLink) => canvaViewUrl(l) ?? (l.url ?? '').trim();

// 학생 PC의 로컬 경로는 사용자명이 드러나고 방문자가 열 수도 없으므로 노트에서 뺀다.
const LOCAL_PATH = /file:\/\/|[A-Za-z]:[\\/]Users[\\/]|\/Users\/[^/\s]+\//;
export const isPublicNote = (n: FPNote) => !LOCAL_PATH.test(n.text ?? '');
