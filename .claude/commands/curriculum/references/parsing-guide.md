# curriculum.js 파싱 패턴

```javascript
// 헤더: "const CURRICULUM = "
// 본문: JSON 배열 (주석 포함, trailing comma 허용)
// 푸터: "];\n\nif (typeof module !== \"undefined\") module.exports = CURRICULUM;"
```

**읽기**: `const CURRICULUM = ` 이후부터 `];` 까지 추출 → JS→JSON 변환 → parse
**쓰기**: JSON.stringify(indent=2) → 헤더/푸터 재부착 → 파일 저장

---

## 주의사항 (Generated Files)

1. curriculum.json, curriculum-notion.json, curriculum.js는 generated file — 직접 수정 금지
2. 콘텐츠(title/copy/tasks) 수정은 반드시 Notion MCP 경로로
3. 에셋(image/showme/status/done) 수정은 overrides.json만
4. sync 실행 시 NOTION_TOKEN 환경변수 필요
