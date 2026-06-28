import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// 소스: course-site/assets/showme/ (Show Me 카드 시스템, Notion 생성물).
//  - _registry.js: SHOWME_REGISTRY = { id: { label, icon, week, category?, toolName? } } (메타 SSoT)
//  - _catalog.json: categoryOrder / categoryMap (분류·정렬)
// 카드 본문 HTML 과 _helpers.js 는 web/public/showme/ 로 복사돼 정적 서빙된다.
// 인덱스만 빌드타임에 메타를 읽어 생성한다. 데이터는 중복 저장하지 않는다.
function pick(rel: string): string {
  const candidates = [
    resolve(process.cwd(), `../course-site/assets/showme/${rel}`),
    resolve(process.cwd(), `course-site/assets/showme/${rel}`),
  ];
  for (const p of candidates) {
    try {
      return readFileSync(p, 'utf-8');
    } catch {
      /* 다음 후보 */
    }
  }
  throw new Error(`showme 소스 없음: ${rel} (시도: ${candidates.join(', ')})`);
}

export interface ShowmeCard {
  id: string;
  label: string;
  week: number | number[] | null;
  category: string;
}

interface RegistryEntry {
  label: string;
  week: number | number[] | null;
  category?: string;
}

// _registry.js 는 `var SHOWME_REGISTRY = {...}` (따옴표 없는 키)라 JSON.parse 불가.
// eval/new Function 은 쓰지 않는다. 각 항목이 중첩 없는 평탄한 객체라
// 정규식으로 id·label·week·category 만 안전하게 추출한다.
function loadRegistry(): Record<string, RegistryEntry> {
  const src = pick('_registry.js');
  const out: Record<string, RegistryEntry> = {};
  // "id": { ...flat... }
  const entryRe = /"([a-z0-9-]+)"\s*:\s*\{([^}]*)\}/g;
  let m: RegExpExecArray | null;
  while ((m = entryRe.exec(src)) !== null) {
    const [, id, body] = m;
    const label = body.match(/\blabel\s*:\s*"((?:[^"\\]|\\.)*)"/)?.[1];
    if (!label) continue;
    const weekRaw = body.match(/\bweek\s*:\s*(\[[^\]]*\]|\d+)/)?.[1];
    let week: number | number[] | null = null;
    if (weekRaw) {
      week = weekRaw.startsWith('[')
        ? weekRaw.slice(1, -1).split(',').map((n) => Number(n.trim())).filter((n) => !Number.isNaN(n))
        : Number(weekRaw);
    }
    const category = body.match(/\bcategory\s*:\s*"([^"]*)"/)?.[1];
    out[id] = { label, week, category };
  }
  return out;
}

interface Catalog {
  categoryOrder: string[];
  categoryMap: Record<string, string>;
}

function loadCatalog(): Catalog {
  return JSON.parse(pick('_catalog.json')) as Catalog;
}

const registry = loadRegistry();
const catalog = loadCatalog();
const FALLBACK_CATEGORY = '기타';

// 분류는 categoryMap(표시명) 만 신뢰한다. registry 의 category 는 슬러그(edit-mode 등)라
// categoryOrder(표시명)와 매칭되지 않아 그룹에서 누락되므로 쓰지 않는다. 미분류는 '기타'.
export const cards: ShowmeCard[] = Object.entries(registry).map(([id, e]) => ({
  id,
  label: e.label,
  week: e.week ?? null,
  category: catalog.categoryMap[id] || FALLBACK_CATEGORY,
}));

// '전체'(All) 탭은 그룹이 아니라 필터이므로 그룹 순서에서 제외한다.
const order = catalog.categoryOrder.filter((c) => c !== '전체');

export interface CategoryGroup {
  category: string;
  items: ShowmeCard[];
}

export const cardGroups: CategoryGroup[] = [...order, FALLBACK_CATEGORY]
  .filter((c, i, arr) => arr.indexOf(c) === i)
  .map((category) => ({
    category,
    items: cards.filter((c) => c.category === category),
  }))
  .filter((g) => g.items.length > 0);

export const cardCount = cards.length;
