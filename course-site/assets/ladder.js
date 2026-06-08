/* course-site/assets/ladder.js
   발표순서 사다리타기 게임 — 로직(window.Ladder) + UI */
(function () {
  'use strict';

  var Ladder = {};
  window.Ladder = Ladder;

  /* ── 순수 로직 ─────────────────────────────────────── */

  Ladder.parseParticipants = function (text) {
    return String(text || '')
      .split('\n')
      .map(function (s) { return s.trim(); })
      .filter(function (s) { return s.length > 0; });
  };

  // rungs[r] = [i, ...] : row r 에서 col i 와 col i+1 사이 가로줄
  Ladder.generateLadder = function (n, rows) {
    rows = rows || Math.min(Math.max(n * 2, 6), 24); // 가로줄 상한 — 과밀/세로 과길이 방지
    var rungs = [];
    for (var r = 0; r < rows; r++) {
      var row = [];
      var i = 0;
      while (i < n - 1) {
        if (Math.random() < 0.5) {
          row.push(i);
          i += 2; // 인접 충돌 방지: i+1 건너뜀
        } else {
          i += 1;
        }
      }
      rungs.push(row);
    }
    return { n: n, rows: rows, rungs: rungs };
  };

  Ladder.tracePath = function (ladder, startCol) {
    var col = startCol;
    var path = [{ row: -1, col: col }];
    for (var r = 0; r < ladder.rows; r++) {
      var row = ladder.rungs[r];
      if (row.indexOf(col) !== -1) {
        col = col + 1;        // 오른쪽 가로줄 → 우이동
      } else if (row.indexOf(col - 1) !== -1) {
        col = col - 1;        // 왼쪽 가로줄 → 좌이동
      }
      path.push({ row: r, col: col });
    }
    return { endCol: col, path: path };
  };

  // 하단 순번 1..N 고정. participant[i] → 도착 col 의 (col+1)번
  Ladder.computeResults = function (ladder, participants) {
    return participants.map(function (name, i) {
      var t = Ladder.tracePath(ladder, i);
      return { name: name, startCol: i, endCol: t.endCol, slot: t.endCol + 1, path: t.path };
    });
  };

  /* ── 렌더 / UI ─────────────────────────────────────── */

  var NS = 'http://www.w3.org/2000/svg';
  var GEO = { padX: 44, padY: 28, gapY: 22, colGap: 88 }; // colGap: 라벨 폭 수용 / padX: 끝 라벨 반폭 수용
  var state = null; // { names, ladder, results }

  function el(id) { return document.getElementById(id); }
  function colX(i) { return GEO.padX + i * GEO.colGap; }
  function rowY(r) { return GEO.padY + (r + 1) * GEO.gapY; } // r=-1 → top

  function reducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function buildLadderSVG(ladder) {
    var w = GEO.padX * 2 + (ladder.n - 1) * GEO.colGap;
    var h = GEO.padY * 2 + (ladder.rows + 1) * GEO.gapY;
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    svg.setAttribute('class', 'ladder-svg');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', '사다리');
    for (var c = 0; c < ladder.n; c++) {
      var v = document.createElementNS(NS, 'line');
      v.setAttribute('class', 'ladder-col');
      v.setAttribute('x1', colX(c)); v.setAttribute('x2', colX(c));
      v.setAttribute('y1', rowY(-1)); v.setAttribute('y2', rowY(ladder.rows - 1));
      svg.appendChild(v);
    }
    for (var r = 0; r < ladder.rows; r++) {
      ladder.rungs[r].forEach(function (i) {
        var hr = document.createElementNS(NS, 'line');
        hr.setAttribute('class', 'ladder-rung');
        hr.setAttribute('x1', colX(i)); hr.setAttribute('x2', colX(i + 1));
        hr.setAttribute('y1', rowY(r)); hr.setAttribute('y2', rowY(r));
        svg.appendChild(hr);
      });
    }
    return { svg: svg, w: w, h: h };
  }

  function pathPoints(result) {
    var p = result.path, pts = [];
    for (var i = 0; i < p.length; i++) {
      var y = (p[i].row < 0) ? rowY(-1) : rowY(p[i].row);
      if (i > 0 && p[i].col !== p[i - 1].col) {
        // 직각 꺾임: 이전 칸 x에서 현재 높이까지 수직 → 현재 칸으로 수평 (대각선 금지)
        pts.push(colX(p[i - 1].col) + ',' + y);
      }
      pts.push(colX(p[i].col) + ',' + y);
    }
    return pts.join(' ');
  }

  function svgEl() { return el('board').querySelector('svg'); }

  function drawPath(svg, result, animate) {
    var pl = document.createElementNS(NS, 'polyline');
    pl.setAttribute('class', 'ladder-path');
    pl.setAttribute('points', pathPoints(result));
    svg.appendChild(pl);
    if (animate && !reducedMotion()) {
      var len = pl.getTotalLength();
      var dur = Math.min(3, Math.max(0.7, len / 600)); // 길이 비례 — 일정 속도로 또박또박 진행
      pl.style.strokeDasharray = len;
      pl.style.strokeDashoffset = len;
      pl.getBoundingClientRect(); // 강제 reflow 후 transition
      pl.style.transition = 'stroke-dashoffset ' + dur + 's linear';
      pl.style.strokeDashoffset = '0';
    }
    return pl;
  }

  function drawControls() {
    var wrap = document.createElement('div'); wrap.className = 'ladder-actions ladder-draw';
    var all = document.createElement('button');
    all.type = 'button'; all.className = 'btn-primary'; all.id = 'drawAllBtn';
    all.textContent = '전체 공개';
    all.addEventListener('click', revealAll);
    wrap.appendChild(all);
    return wrap;
  }

  function renderBoard() {
    var board = el('board');
    board.textContent = '';
    var built = buildLadderSVG(state.ladder);
    var pct = function (c) { return (colX(c) / built.w * 100) + '%'; }; // 라벨↔줄 정렬 핵심

    // 자연 폭 inner — 축소하지 않고, 넘치면 board가 가로 스크롤
    var inner = document.createElement('div');
    inner.className = 'ladder-inner';
    inner.style.width = built.w + 'px';

    // 상단 이름 라벨 — colX 기준 절대위치(중앙정렬은 CSS translateX). textContent=XSS 안전
    var top = document.createElement('div'); top.className = 'ladder-tops';
    state.names.forEach(function (name, idx) {
      var s = document.createElement('span'); s.className = 'ladder-name'; s.textContent = name;
      s.style.left = pct(idx);
      s.setAttribute('role', 'button'); s.setAttribute('tabindex', '0');
      s.setAttribute('title', name + ' 순서 보기');
      s.addEventListener('click', function () { revealOne(state.results[idx]); });
      s.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); revealOne(state.results[idx]); }
      });
      top.appendChild(s);
    });
    // 하단 순번 1..N — 같은 colX 기준
    var bot = document.createElement('div'); bot.className = 'ladder-bottoms';
    for (var k = 0; k < state.ladder.n; k++) {
      var b = document.createElement('span'); b.className = 'ladder-slot'; b.textContent = (k + 1) + '번';
      b.style.left = pct(k);
      bot.appendChild(b);
    }
    inner.appendChild(top);
    inner.appendChild(built.svg);
    inner.appendChild(bot);

    board.appendChild(inner);
    board.appendChild(drawControls());
    board.hidden = false;
  }

  function renderResults(list) {
    list = list || state.results;
    var box = el('results');
    var existing = {};
    Array.prototype.forEach.call(box.querySelectorAll('.result-row'), function (row) {
      existing[row.getAttribute('data-slot')] = true;
    });
    list.slice().sort(function (a, b) { return a.slot - b.slot; }).forEach(function (r) {
      if (existing[r.slot]) return; // 누적 공개: 이미 있는 slot 건너뜀
      var row = document.createElement('div'); row.className = 'result-row';
      row.setAttribute('data-slot', r.slot);
      var slot = document.createElement('span'); slot.className = 'result-slot'; slot.textContent = r.slot;
      var name = document.createElement('span'); name.className = 'result-name'; name.textContent = r.name;
      row.appendChild(slot); row.appendChild(name);
      box.appendChild(row);
    });
    box.hidden = false;
  }

  function revealOne(result) {
    drawPath(svgEl(), result, true);
    renderResults([result]);
  }

  function revealAll() {
    var svg = svgEl();
    state.results.forEach(function (r) { drawPath(svg, r, true); });
    renderResults(state.results);
  }

  function build() {
    var names = Ladder.parseParticipants(el('names').value);
    if (names.length < 2) { el('hint').textContent = '최소 2명이 필요합니다.'; return; }
    el('hint').textContent = '';
    var ladder = Ladder.generateLadder(names.length);
    state = { names: names, ladder: ladder, results: Ladder.computeResults(ladder, names) };
    el('results').textContent = ''; el('results').hidden = true;
    renderBoard();
    el('resetBtn').hidden = false;
  }

  function reset() {
    state = null;
    el('board').hidden = true; el('board').textContent = '';
    el('results').hidden = true; el('results').textContent = '';
    el('resetBtn').hidden = true;
    el('hint').textContent = '';
  }

  function init() {
    if (!el('buildBtn')) return;
    el('buildBtn').addEventListener('click', build);
    el('resetBtn').addEventListener('click', reset);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }

})();
