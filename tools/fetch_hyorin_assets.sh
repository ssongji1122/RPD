#!/usr/bin/env bash
# usage: ./tools/fetch_hyorin_assets.sh <fresh_notion_fetch.txt> <out_dir>
# 주의: Notion S3 URL은 ~1시간 만료. fresh notion-fetch 직후 즉시 실행.
set -euo pipefail
SRC="$1"; OUT="${2:-portfolio/hyorin/assets/raw}"
mkdir -p "$OUT"
# 문서 순서 보존(= 주차 순서, 큐레이션 키). sort 금지. URL 중복만 awk로 제거.
grep -oE 'https://prod-files-secure[^])"<> ]+' "$SRC" | awk '!seen[$0]++' > "$OUT/_urls.txt"
echo "추출된 URL: $(wc -l < "$OUT/_urls.txt")개"
i=0
: > "$OUT/_manifest.tsv"
while IFS= read -r u; do
  # URL 경로의 원본 파일명 디코드 → 의미 보존(shot1_studio.png 등). 순번 prefix로 순서 보존 + 충돌(image.png 중복) 방지
  base="$(python3 -c "import sys,os,urllib.parse as p; print(os.path.basename(p.urlparse(p.unquote(sys.argv[1])).path) or 'asset.bin')" "$u")"
  out="$(printf '%03d_%s' "$i" "$base")"
  printf '%03d\t%s\n' "$i" "$base" >> "$OUT/_manifest.tsv"
  curl -fsS --max-time 90 -o "$OUT/$out" "$u" || echo "  FAIL $i $base"
  i=$((i+1))
done < "$OUT/_urls.txt"
echo "다운로드 완료 ($i개). _manifest.tsv = 순번→원본파일명(주차 큐레이션 lookup 키)."
ls -lhS "$OUT" | head
