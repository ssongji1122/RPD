import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// 소스: course-site/data/final-projects.js (Week 15 기말 작품 아카이브, 생성물).
// `window.RPDFinalProjects = { ... };` 형태라 래퍼를 벗기고 JSON 파싱한다.
// 데이터는 중복 저장하지 않고 빌드 타임에 공유 소스를 읽는다.
// 미디어 바이너리(webp/mp4)도 커밋하지 않는다 — predev/prebuild 훅의
// scripts/sync-final-assets.mjs 가 course-site 에서 public/ 으로 동기화한다.
const CANDIDATES = [
  resolve(process.cwd(), '../course-site/data/final-projects.js'),
  resolve(process.cwd(), 'course-site/data/final-projects.js'),
];

export interface FPMedia {
  type: 'image' | 'video';
  src: string;
  videoSrc?: string;
  role: string;
}
export interface FPVideo {
  src: string;
  poster: string;
}
export interface FPLink {
  label: string;
  url: string;
  kind: string;
  /** 빌드 데이터에 미리 해석해 둔 임베드 URL (예: Canva view?embed) */
  embedUrl?: string;
}
export interface FPNote {
  section: string | null;
  text: string;
}
export interface FPProject {
  id: string;
  code: string;
  title: string;
  media: FPMedia[];
  videos: FPVideo[];
  links: FPLink[];
  coverSrc?: string;
  /** 학생 발표 사이트·Behance에서 수집한 작품명 (없으면 익명 코드 유지) */
  workTitle?: string;
  /** 학생이 노션 제출 페이지에 남긴 제작 노트 (원문) */
  notes?: FPNote[];
}
export interface FinalProjects {
  generatedAt: string;
  source: string;
  stats: Record<string, number | string>;
  projects: FPProject[];
}

function load(): FinalProjects {
  let raw = '';
  for (const p of CANDIDATES) {
    try {
      raw = readFileSync(p, 'utf-8');
      break;
    } catch {
      /* 다음 후보 */
    }
  }
  if (!raw) {
    throw new Error(
      `final-projects.js 를 찾을 수 없습니다. 시도: ${CANDIDATES.join(', ')}`,
    );
  }
  const match = raw.match(/=\s*(\{[\s\S]*\})\s*;?\s*$/);
  if (!match) throw new Error('final-projects.js 파싱 실패: 객체 리터럴을 찾지 못함');
  return JSON.parse(match[1]) as FinalProjects;
}

// 데이터의 상대 경로(assets/...)를 배포 base 를 반영한 절대 경로로 보정한다.
const BASE = import.meta.env.BASE_URL.replace(/\/$/, '');
function toPublic(src: string | undefined): string | undefined {
  if (!src) return src;
  return src.startsWith('assets/') ? `${BASE}/${src}` : src;
}

const data = load();

// 대표 이미지 교정: 원본 coverSrc 가 대표성 없는 경우(웹 스크린샷 등)
// 히어로감 이미지로 덮어쓴다. 값은 relative(assets/...) — toPublic 이 base 를 붙인다.
//  - project-16: 원본이 웹 스크린샷(image-07) → 캐릭터 렌더(image-01)
// project-03 검은 포스터 건은 데이터(coverSrc=cover.webp)에서 해결돼 override 불필요.
const COVER_OVERRIDES: Record<string, string> = {
  'project-16': 'assets/final-projects/project-16/image-01.webp',
};

export const finalProjects: FPProject[] = data.projects.map((p) => ({
  ...p,
  coverSrc: toPublic(COVER_OVERRIDES[p.id] ?? p.coverSrc),
  media: p.media.map((m) => ({ ...m, src: toPublic(m.src)!, videoSrc: toPublic(m.videoSrc) })),
  videos: p.videos.map((v) => ({ src: toPublic(v.src)!, poster: toPublic(v.poster)! })),
}));

export const finalProjectsMeta = {
  generatedAt: data.generatedAt,
  source: data.source,
  stats: data.stats,
};
