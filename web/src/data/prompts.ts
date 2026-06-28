import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

// 소스: course-site/data/notion-blocks/weekNN.json (Notion 원본 블록).
// 주차별 code 블록 = 학생이 복붙하는 AI 프롬프트. 이것만 추출해 렌더한다.
// (notion-blocks 의 image 블록은 대부분 만료된 S3 서명 URL이라 쓰지 않는다 —
//  주차 이미지는 site-data 의 step.image(로컬 안정 자산)를 쓴다.)
function blocksDir(): string[] {
  return [
    resolve(process.cwd(), '../course-site/data/notion-blocks'),
    resolve(process.cwd(), 'course-site/data/notion-blocks'),
  ];
}

export interface Prompt {
  language: string;
  text: string;
}

function richText(rt: { plain_text?: string }[] | undefined): string {
  return (rt ?? []).map((x) => x.plain_text ?? '').join('');
}

/** 주차 번호(int)의 프롬프트(code 블록) 목록. 파일이 없으면 빈 배열. */
export function loadPrompts(week: number): Prompt[] {
  const file = `week${String(week).padStart(2, '0')}.json`;
  for (const dir of blocksDir()) {
    try {
      const raw = readFileSync(resolve(dir, file), 'utf-8');
      const data = JSON.parse(raw) as { blocks?: any[] };
      return (data.blocks ?? [])
        .filter((b) => b?.type === 'code')
        .map((b) => ({
          language: b.code?.language ?? 'plain text',
          text: richText(b.code?.rich_text).trim(),
        }))
        .filter((p) => p.text.length > 0);
    } catch {
      // 다음 후보 디렉토리
    }
  }
  return [];
}
