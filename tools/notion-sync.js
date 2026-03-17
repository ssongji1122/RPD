#!/usr/bin/env node

/**
 * 노션 → 웹 동기화 스크립트
 * ===========================
 * Notion 주차별 페이지에서 구조화된 콘텐츠를 읽어
 * course-site/data/overrides.json을 생성/업데이트합니다.
 *
 * 사용법:
 *   node tools/notion-sync.js --week 3          # 3주차만 동기화
 *   node tools/notion-sync.js --all              # 모든 주차 동기화
 *   node tools/notion-sync.js                    # 기본값: --all
 */

const fs = require('fs');
const path = require('path');

// ═════════════════════════════════════════════════════════════════════════
// 설정 및 경로
// ═════════════════════════════════════════════════════════════════════════

const ROOT = path.resolve(__dirname, '..');
const NOTION_CONFIG = path.join(ROOT, 'course-site', 'data', 'notion-config.json');
const SYNC_CONFIG = path.join(__dirname, 'sync-config.json');
const OVERRIDES_FILE = path.join(ROOT, 'course-site', 'data', 'overrides.json');

// ═════════════════════════════════════════════════════════════════════════
// Notion API 헬퍼
// ═════════════════════════════════════════════════════════════════════════

/**
 * Notion API 요청을 수행합니다.
 * @param {string} method - HTTP 메서드 (GET, POST, PATCH, DELETE)
 * @param {string} endpoint - API 엔드포인트 (e.g., /pages/{id}, /blocks/{id}/children)
 * @param {object|null} body - 요청 본문 (선택사항)
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
 * 텍스트 블록에서 텍스트를 추출합니다.
 * @param {object} block - Notion 블록
 * @returns {string} 추출된 텍스트
 */
function extractText(block) {
  // paragraph, heading_1, heading_2, heading_3, bulleted_list_item, numbered_list_item 등
  const type = block.type;
  const content = block[type];

  if (!content || !content.rich_text) {
    return '';
  }

  return content.rich_text
    .map(text => text.plain_text)
    .join('');
}

/**
 * 블록의 모든 자식 블록을 재귀적으로 가져옵니다.
 * @param {string} blockId - 부모 블록 ID
 * @param {string} token - Notion API 토큰
 * @returns {Promise<object[]>} 블록 목록
 */
async function getPageBlocksRecursive(blockId, token) {
  const blocks = [];
  let cursor = undefined;

  try {
    while (true) {
      // 블록의 자식 목록을 가져옵니다.
      const response = await notionRequest(
        'GET',
        `/blocks/${blockId}/children?page_size=100${cursor ? `&start_cursor=${cursor}` : ''}`,
        null,
        token
      );

      if (!response.results) {
        break;
      }

      blocks.push(...response.results);

      // 더 이상 페이지가 없으면 반복을 종료합니다.
      if (!response.has_more) {
        break;
      }

      cursor = response.next_cursor;
    }
  } catch (error) {
    console.warn(`⚠ 블록 로드 실패 (${blockId}): ${error.message}`);
  }

  return blocks;
}

// ═════════════════════════════════════════════════════════════════════════
// Notion 콘텐츠 파싱
// ═════════════════════════════════════════════════════════════════════════

/**
 * Notion 페이지에서 주차 데이터를 추출합니다.
 * @param {string} pageId - Notion 페이지 ID
 * @param {number} weekNumber - 주차 번호
 * @param {string} token - Notion API 토큰
 * @returns {Promise<object>} 주차 오버라이드 데이터
 */
async function extractWeekFromNotion(pageId, weekNumber, token) {
  console.log(`  → Week ${weekNumber} 로드 중...`);

  const weekOverride = {
    status: 'upcoming',
    summary: '',
    videos: [],
    steps: {},
    explore: [],
  };

  try {
    // 페이지의 모든 블록을 가져옵니다.
    const blocks = await getPageBlocksRecursive(pageId, token);

    if (!blocks || blocks.length === 0) {
      console.warn(`⚠ Week ${weekNumber}: 블록을 찾을 수 없습니다.`);
      return weekOverride;
    }

    let currentSection = null;
    let currentStepIndex = 0;
    let collectingSteps = false;

    // 블록을 순서대로 처리합니다.
    for (let i = 0; i < blocks.length; i++) {
      const block = blocks[i];

      // 제목 블록: 섹션 판별
      if (block.type === 'heading_1' || block.type === 'heading_2') {
        const title = extractText(block).trim().toLowerCase();

        if (title.includes('요약') || title.includes('summary')) {
          currentSection = 'summary';
        } else if (title.includes('비디오') || title.includes('video')) {
          currentSection = 'videos';
        } else if (title.includes('단계') || title.includes('step')) {
          currentSection = 'steps';
          collectingSteps = true;
          currentStepIndex = 0;
        } else if (title.includes('탐색') || title.includes('explore')) {
          currentSection = 'explore';
        } else if (title.includes('상태') || title.includes('status')) {
          currentSection = 'status';
        }
        continue;
      }

      // 단락: 콘텐츠 수집
      if (block.type === 'paragraph') {
        const text = extractText(block).trim();
        if (!text) continue;

        if (currentSection === 'summary') {
          weekOverride.summary = text;
        } else if (currentSection === 'status') {
          const lowerText = text.toLowerCase();
          if (lowerText.includes('done') || lowerText.includes('완료')) {
            weekOverride.status = 'done';
          } else if (lowerText.includes('active') || lowerText.includes('진행중')) {
            weekOverride.status = 'active';
          } else if (lowerText.includes('upcoming') || lowerText.includes('예정')) {
            weekOverride.status = 'upcoming';
          }
        }
        continue;
      }

      // 북마크: 비디오 URL 수집
      if (block.type === 'bookmark') {
        if (currentSection === 'videos') {
          const bookmarkContent = block.bookmark;
          if (bookmarkContent && bookmarkContent.url) {
            // 페이지 제목에서 비디오 제목 추출 시도
            let videoTitle = '비디오';

            // 이전 블록에서 제목을 가져옵니다.
            if (i > 0 && (blocks[i - 1].type === 'paragraph' || blocks[i - 1].type === 'heading_3')) {
              videoTitle = extractText(blocks[i - 1]).trim() || '비디오';
            }

            weekOverride.videos.push({
              title: videoTitle,
              url: bookmarkContent.url,
            });
          }
        }
        continue;
      }

      // 이미지: 단계의 이미지 수집
      if (block.type === 'image') {
        if (currentSection === 'steps' && weekOverride.steps[currentStepIndex]) {
          const imageContent = block.image;
          if (imageContent) {
            const imageUrl = imageContent.type === 'external'
              ? imageContent.external.url
              : imageContent.file?.url;

            if (imageUrl) {
              weekOverride.steps[currentStepIndex].image = imageUrl;
            }
          }
        }
        continue;
      }

      // 불릿 리스트: 여러 용도로 사용
      if (block.type === 'bulleted_list_item') {
        const text = extractText(block).trim();
        if (!text) continue;

        if (currentSection === 'explore') {
          // 탐색 항목 수집
          weekOverride.explore.push({
            title: text,
            hint: '',
          });
        } else if (currentSection === 'steps' && collectingSteps) {
          // 단계의 완료 항목 수집
          if (!weekOverride.steps[currentStepIndex]) {
            weekOverride.steps[currentStepIndex] = { done: [] };
          }
          if (!Array.isArray(weekOverride.steps[currentStepIndex].done)) {
            weekOverride.steps[currentStepIndex].done = [];
          }
          weekOverride.steps[currentStepIndex].done.push(text);
        }
        continue;
      }
    }

    console.log(`    ✓ Week ${weekNumber}: 요약=${!!weekOverride.summary}, 비디오=${weekOverride.videos.length}개, 단계=${Object.keys(weekOverride.steps).length}개`);
  } catch (error) {
    console.warn(`⚠ Week ${weekNumber} 파싱 실패: ${error.message}`);
  }

  return weekOverride;
}

// ═════════════════════════════════════════════════════════════════════════
// 파일 읽기/쓰기
// ═════════════════════════════════════════════════════════════════════════

/**
 * Notion 설정을 로드합니다.
 * @returns {object|null} 설정 (token, databaseId)
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
 * @returns {object} 동기화 설정 (주차별 페이지 ID)
 */
function loadSyncConfig() {
  if (!fs.existsSync(SYNC_CONFIG)) {
    console.warn(`⚠ ${SYNC_CONFIG} 파일을 찾을 수 없습니다. 빈 설정으로 진행합니다.`);
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

/**
 * 기존 오버라이드를 로드합니다.
 * @returns {object} 오버라이드 데이터
 */
function loadExistingOverrides() {
  if (!fs.existsSync(OVERRIDES_FILE)) {
    return { _comment: '어드민 전용 필드. 노션 동기화 시 이 값이 우선함.', weeks: {} };
  }

  try {
    return JSON.parse(fs.readFileSync(OVERRIDES_FILE, 'utf-8'));
  } catch (error) {
    console.warn(`⚠ 기존 오버라이드 로드 실패: ${error.message}`);
    return { _comment: '어드민 전용 필드. 노션 동기화 시 이 값이 우선함.', weeks: {} };
  }
}

/**
 * 오버라이드를 파일에 저장합니다.
 * @param {object} overrides - 저장할 오버라이드 데이터
 */
function saveOverrides(overrides) {
  try {
    fs.writeFileSync(OVERRIDES_FILE, JSON.stringify(overrides, null, 2), 'utf-8');
    console.log(`\n✓ 저장 완료: ${OVERRIDES_FILE}`);
  } catch (error) {
    console.error(`✗ 오버라이드 저장 실패: ${error.message}`);
  }
}

// ═════════════════════════════════════════════════════════════════════════
// 메인 동기화 로직
// ═════════════════════════════════════════════════════════════════════════

/**
 * 변경 사항을 감지합니다.
 * @param {object} old - 기존 데이터
 * @param {object} new_ - 새 데이터
 * @returns {boolean} 변경 사항 여부
 */
function hasChanges(old, new_) {
  return JSON.stringify(old) !== JSON.stringify(new_);
}

/**
 * 메인 동기화 함수
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
    console.error('❌ 사용법: node tools/notion-sync.js [--week N | --all]');
    process.exit(1);
  }

  // 설정 로드
  const notionConfig = loadNotionConfig();
  if (!notionConfig || !notionConfig.token) {
    console.error('❌ Notion 토큰을 찾을 수 없습니다.');
    process.exit(1);
  }

  const syncConfig = loadSyncConfig();
  const existingOverrides = loadExistingOverrides();

  console.log(`\n📋 Notion → overrides.json 동기화`);
  console.log(`   주차: ${targetWeeks.join(', ')}`);
  console.log(`   동기화 설정: ${Object.keys(syncConfig.weeks).length}개 주차 매핑됨\n`);

  let changedCount = 0;

  // 각 주차를 동기화합니다.
  for (const weekNum of targetWeeks) {
    const weekKey = String(weekNum);
    const pageId = syncConfig.weeks[weekKey];

    if (!pageId) {
      console.warn(`⚠ Week ${weekNum}: 페이지 ID가 sync-config.json에 없습니다.`);
      continue;
    }

    try {
      // Notion 페이지에서 데이터 추출
      const newWeekData = await extractWeekFromNotion(pageId, weekNum, notionConfig.token);

      // 기존 데이터와 비교
      const oldWeekData = existingOverrides.weeks[weekKey] || {};

      if (hasChanges(oldWeekData, newWeekData)) {
        existingOverrides.weeks[weekKey] = newWeekData;
        changedCount++;
        console.log(`    → 변경됨`);
      } else {
        console.log(`    → 변경 없음`);
      }
    } catch (error) {
      console.error(`✗ Week ${weekNum} 동기화 실패: ${error.message}`);
    }
  }

  // 결과 저장
  if (changedCount > 0) {
    saveOverrides(existingOverrides);
    console.log(`\n✓ ${changedCount}개 주차가 업데이트되었습니다.`);
    process.exit(0);
  } else {
    console.log(`\n✓ 모든 주차가 최신 상태입니다.`);
    process.exit(2); // 변경 없음을 나타내는 코드
  }
}

// 실행
main().catch(error => {
  console.error(`❌ 동기화 실패: ${error.message}`);
  process.exit(1);
});
