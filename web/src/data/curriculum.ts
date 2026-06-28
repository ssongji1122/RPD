import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// SSoT: Notion → tools/*sync* → weeks/site-data.json (canonical).
// 이 사이트는 빌드 타임에 canonical 을 읽어 렌더한다. 데이터는 여기서 손대지 않는다.
// course-site/ 와 동일한 원본을 공유하므로 드리프트가 발생하지 않는다.
//
// 경로는 빌드 cwd 기준으로 잡는다. astro 는 프로젝트 루트(web/)에서 실행되므로
// 보통 ../weeks/site-data.json 이지만, 루트(RPD/)에서 실행되는 경우도 폴백으로 둔다.
// import.meta.url 은 번들링 시 dist 로 이동해 깨지므로 쓰지 않는다.
const CANONICAL_CANDIDATES = [
  resolve(process.cwd(), '../weeks/site-data.json'),
  resolve(process.cwd(), 'weeks/site-data.json'),
];

function resolveCanonicalPath(): string {
  for (const p of CANONICAL_CANDIDATES) {
    try {
      readFileSync(p);
      return p;
    } catch {
      // 다음 후보 시도
    }
  }
  throw new Error(
    `canonical 데이터(weeks/site-data.json)를 찾을 수 없습니다. 시도: ${CANONICAL_CANDIDATES.join(', ')}`,
  );
}

const CANONICAL_PATH = resolveCanonicalPath();

export interface StepTask {
  id: string;
  label: string;
  detail: string;
}

export interface Step {
  title: string;
  copy: string;
  goal: string[];
  done: string[];
  tasks: StepTask[];
}

export interface LinkRef {
  title: string;
  url: string;
}

export interface Assignment {
  title: string;
  description: string;
  checklist: string[];
}

export interface Shortcut {
  keys: string;
  action: string;
}

export interface WeekRaw {
  week: number;
  status: string;
  title: string;
  subtitle: string;
  duration: string;
  topics: string[];
  steps: Step[];
  shortcuts: Shortcut[];
  explore: unknown[];
  assignment: Assignment | null;
  mistakes: string[];
  videos: LinkRef[];
  docs: LinkRef[];
  summary: string;
}

export interface Week extends WeekRaw {
  /** "W01" 형식 (zero-padded) */
  id: string;
  /** 커리큘럼 단계 라벨 */
  phaseLabel: string;
}

// 커리큘럼 단계 구분 (CLAUDE.md Curriculum 표 기준).
// 매직 넘버를 피하기 위해 범위를 상수로 둔다.
const PHASES: { label: string; from: number; to: number }[] = [
  { label: '기초', from: 1, to: 4 },
  { label: '디테일', from: 5, to: 7 },
  { label: '중간', from: 8, to: 8 },
  { label: '고급', from: 9, to: 14 },
  { label: '마무리', from: 15, to: 16 },
];

function phaseFor(week: number): string {
  const p = PHASES.find((x) => week >= x.from && week <= x.to);
  return p ? p.label : '';
}

function pad(week: number): string {
  return `W${String(week).padStart(2, '0')}`;
}

const raw = JSON.parse(readFileSync(CANONICAL_PATH, 'utf-8')) as WeekRaw[];

export const weeks: Week[] = raw
  .slice()
  .sort((a, b) => a.week - b.week)
  .map((w) => ({ ...w, id: pad(w.week), phaseLabel: phaseFor(w.week) }));

/** 현재 진행 주차 (canonical status === 'active'). 없으면 마지막 주차. */
export const currentWeek: Week =
  weeks.find((w) => w.status === 'active') ?? weeks[weeks.length - 1];

export function getWeek(id: string | undefined): Week | undefined {
  return weeks.find((w) => w.id === id);
}

export const phaseLabels = PHASES.map((p) => p.label);
