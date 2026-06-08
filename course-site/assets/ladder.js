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
    rows = rows || Math.max(n * 2, 6);
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

  // DOM 바인딩은 파일 하단 init()에서 (다음 Task).

})();
