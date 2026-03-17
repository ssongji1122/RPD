#!/usr/bin/env node

/**
 * 웹 → 노션 동기화 스크립트
 * ===========================
 * 학생 진행도 데이터를 읽어 Notion 페이지에 동기화합니다.
 *
 * 사용법:
 *   node tools/web-to-notion.js --progress-file data/student-progress.json
 *   node tools/web-to-notion.js --week 3
 *   node tools/web-to-notion.js --all
 */

const fs = require('fs');
const path = require('path');

// ═════════════════════════════════════════════════════════════════════════
// 설정 및 경로
// ═════════════════════════════════════════════════════════════════════════

const ROOT = path.resolve(__dirname, '..');
const NOTION_CONFIG = path.join(ROOT, 'course-site', 'data', 'notion-config.json');
const SYNC_CONFIG = path.join(__dirname, 'sync-config.json');
const PROGRESS_FILE = path.join(ROOT, 'course-site', 'data', 'student-progress.json');

// ═════════════════════════════════════════════════════════════════════════
// Notion API 헬퍼
// ═════════════════════════════════════════════════════════════════════════

/**
 * Notion API 요청을 수행합니다.
 * @param {string} method - HTTP 메서드
 * @param {string} endpoint - API 엔드포인트
 * @param {object|null} body - 요청 본문
 * @param {string} token - Notion API 토큰
 * @returns {Promise<object>} API 응답
 */
async function notionRequest(method, endpoint, body, token) {
  const url = `https://api.notion.com/v1${endpoint}`;
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Notion-Version': '2022-06-28',
    'Content-Type': 'application/json',
  };

  const options = {
    method,
    headers,
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Notion API error: ${response.status} ${errorText}`);
    }
    return await response.json();
  } catch (error) {
    console.warn(`⚠ Notion API 요청 실패 (${endpoint}): ${error.message}`);
    throw error;
  }
}

/**
 * 페이지의 모든 블록을 가져옵니다.
 * @param {string} pageId - Notion 페이지 ID
 * @param {string} token - Notion API 토큰
 * @returns {Promise<object[]>} 블록 목록
 */
async function getPageBlocks(pageId, token) {
  const blocks = [];
  let cursor = undefined;

  try {
    while (true) {
      const response = await notionRequest(
        'GET',
        `/blocks/${pageId}/children?page_size=100${cursor ? `&start_cursor=${cursor}` : ''}`,
        null,
        token
      );

      if (!response.results) {
        break;
      }

      blocks.push(...response.results);

      if (!response.has_more) {
        break;
      }

      cursor = response.next_cursor;
    }
  } catch (error) {
    console.warn(`⚠ 블록 로드 실패 (${pageId}): ${error.message}`);
  }

  return blocks;
}

/**
 * 모든 블록을 삭제합니다.
 * @param {object[]} blocks - 삭제할 블록 목록
 * @param {string} token - Notion API 토큰
 */
async function deleteAllBlocks(blocks, token) {
  for (const block of blocks) {
    try {
      await notionRequest('DELETE', `/blocks/${block.id}`, null, token);
    } catch (error) {
      console.warn(`⚠ 블록 삭제 실패 (${block.id}): ${error.message}`);
    }
  }
}

/**
 * 단락 블록을 추가합니다.
 * @param {string} pageId - 부모 페이지 ID
 * @param {string} text - 단락 텍스트
 * @param {string} token - Notion API 토큰
 */
async function addParagraph(pageId, text, token) {
  await notionRequest(
    'PATCH',
    `/blocks/${pageId}/children`,
    {
      children: [
        {
          object: 'block',
          type: 'paragraph',
          paragraph: {
            rich_text: [
              {
                type: 'text',
                text: {
                  content: text,
                },
              },
            ],
          },
        },
      ],
    },
    token
  );
}

/**
 * 제목 블록을 추가합니다.
 * @param {string} pageId - 부모 페이지 ID
 * @param {string} text - 제목 텍스트
 * @param {number} level - 제목 수준 (1, 2, 3)
 * @param {string} token - Notion API 토큰
 */
async function addHeading(pageId, text, level, token) {
  const headingType = `heading_${level}`;
  await notionRequest(
    'PATCH',
    `/blocks/${pageId}/children`,
    {
      children: [
        {
          object: 'block',
          type: headingType,
          [headingType]: {
            rich_text: [
              {
                type: 'text',
                text: {
                  content: text,
                },
              },
            ],
          },
        },
      ],
    },
    token
  );
}

/**
 * 불릿 리스트 항목을 추가합니다.
 * @param {string} pageId - 부모 페이지 ID
 * @param {string[]} items - 항목 목록
 * @param {string} token - Notion API 토큰
 */
async function addBulletList(pageId, items, token) {
  const children = items.map(text => ({
    object: 'block',
    type: 'bulleted_list_item',
    bulleted_list_item: {
      rich_text: [
        {
          type: 'text',
          text: {
            content: text,
          },
        },
      ],
    },
  }));

  await notionRequest(
    'PATCH',
    `/blocks/${pageId}/children`,
    { children },
    token
  );
}

// ═════════════════════════════════════════════════════════════════════════
// 학생 진행도 처리
// ═════════════════════════════════════════════════════════════════════════

/**
 * 학생 진행도 파일을 로드합니다.
 * @returns {object} 진행도 데이터
 */
function loadProgressData() {
  if (!fs.existsSync(PROGRESS_FILE)) {
    console.warn(`⚠ ${PROGRESS_FILE} 파일을 찾을 수 없습니다.`);
    return { weeks: {} };
  }

  try {
    return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf-8'));
  } catch (error) {
    console.warn(`⚠ 진행도 데이터 로드 실패: ${error.message}`);
    return { weeks: {} };
  }
}

/**
 * Notion 설정을 로드합니다.
 * @returns {object|null} 설정
 */
function loadNotionConfig() {
  if (!fs.existsSync(NOTION_CONFIG)) {
    console.error(`✗ ${NOTION_CONFIG} 파일을 찾을 수 없습니다.`);
    return null;
  }

  try {
    const config = JSON.parse(fs.readFileSync(NOTION_CONFIG, 'utf-8'));
    return config;
  } catch (error) {
    console.error(`✗ Notion 설정 로드 실패: ${error.message}`);
    return null;
  }
}

/**
 * 동기화 설정을 로드합니다.
 * @returns {object} 동기화 설정
 */
function loadSyncConfig() {
  if (!fs.existsSync(SYNC_CONFIG)) {
    console.warn(`⚠ ${SYNC_CONFIG} 파일을 찾을 수 없습니다.`);
    return { weeks: {} };
  }

  try {
    const config = JSON.parse(fs.readFileSync(SYNC_CONFIG, 'utf-8'));
    return config;
  } catch (error) {
    console.warn(`⚠ 동기화 설정 로드 실패: ${error.message}`);
    return { weeks: {} };
  }
}

// ═════════════════════════════════════════════════════════════════════════
// Notion 업데이트 로직
// ═════════════════════════════════════════════════════════════════════════

/**
 * 주차를 Notion에 동기화합니다.
 * @param {number} weekNum - 주차 번호
 * @param {object} progressData - 진행도 데이터
 * @param {string} pageId - Notion 페이지 ID
 * @param {string} token - Notion API 토큰
 */
async function syncWeekToNotion(weekNum, progressData, pageId, token) {
  console.log(`  → Week ${weekNum} 업데이트 중...`);

  try {
    // 기존 블록을 모두 삭제합니다.
    const existingBlocks = await getPageBlocks(pageId, token);
    if (existingBlocks.length > 0) {
      await deleteAllBlocks(existingBlocks, token);
    }

    // 주차 데이터 추출
    const weekData = progressData.weeks[String(weekNum)] || {};
    const status = weekData.status || 'upcoming';
    const checklist = weekData.checklist || [];
    const completedCount = checklist.filter(item => item.completed).length;
    const totalCount = checklist.length;

    // 진행도 섹션 추가
    await addHeading(pageId, '진행도', 2, token);
    await addParagraph(pageId, `상태: ${status}`, token);
    await addParagraph(pageId, `완료: ${completedCount} / ${totalCount}`, token);

    // 체크리스트 섹션 추가
    if (checklist.length > 0) {
      await addHeading(pageId, '체크리스트', 2, token);
      const checklistItems = checklist.map(item => {
        const checked = item.completed ? '✓' : '☐';
        return `${checked} ${item.label}`;
      });
      await addBulletList(pageId, checklistItems, token);
    }

    // 메타데이터 추가
    await addHeading(pageId, '동기화 정보', 3, token);
    await addParagraph(pageId, `마지막 업데이트: ${new Date().toISOString()}`, token);

    console.log(`    ✓ Week ${weekNum}: 완료됨 (${completedCount}/${totalCount})`);
  } catch (error) {
    console.error(`✗ Week ${weekNum} 업데이트 실패: ${error.message}`);
  }
}

// ═════════════════════════════════════════════════════════════════════════
// 메인 함수
// ═════════════════════════════════════════════════════════════════════════

/**
 * 메인 함수
 */
async function main() {
  // 명령줄 인자 파싱
  const args = process.argv.slice(2);
  let targetWeeks = null;

  if (args.includes('--week')) {
    const idx = args.indexOf('--week');
    if (idx + 1 < args.length) {
      const weekNum = parseInt(args[idx + 1], 10);
      if (!isNaN(weekNum)) {
        targetWeeks = [weekNum];
      }
    }
  } else if (args.includes('--all') || args.length === 0) {
    targetWeeks = Array.from({ length: 15 }, (_, i) => i + 1);
  }

  if (!targetWeeks || targetWeeks.length === 0) {
    console.error('❌ 사용법: node tools/web-to-notion.js [--week N | --all]');
    process.exit(1);
  }

  // 설정 로드
  const notionConfig = loadNotionConfig();
  if (!notionConfig || !notionConfig.token) {
    console.error('❌ Notion 토큰을 찾을 수 없습니다.');
    process.exit(1);
  }

  const syncConfig = loadSyncConfig();
  const progressData = loadProgressData();

  console.log(`\n📤 웹 → Notion 동기화`);
  console.log(`   주차: ${targetWeeks.join(', ')}`);
  console.log(`   진행도 파일: ${PROGRESS_FILE}\n`);

  let syncedCount = 0;

  // 각 주차를 동기화합니다.
  for (const weekNum of targetWeeks) {
    const weekKey = String(weekNum);
    const pageId = syncConfig.weeks[weekKey];

    if (!pageId) {
      console.warn(`⚠ Week ${weekNum}: 페이지 ID가 sync-config.json에 없습니다.`);
      continue;
    }

    try {
      await syncWeekToNotion(weekNum, progressData, pageId, notionConfig.token);
      syncedCount++;
    } catch (error) {
      console.error(`✗ Week ${weekNum} 동기화 실패: ${error.message}`);
    }
  }

  console.log(`\n✓ ${syncedCount}개 주차가 Notion에 업데이트되었습니다.`);
  process.exit(0);
}

// 실행
main().catch(error => {
  console.error(`❌ 동기화 실패: ${error.message}`);
  process.exit(1);
});
