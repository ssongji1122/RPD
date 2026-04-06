/* student-detail-drawer.js — RPD Admin: student profile detail drawer
 * Exposes: window.RPDStudentDrawer.open(data), .close()
 * data = { student: {name, classNum, attendance, submissionCount, midterm, final, weeks},
 *           total: number, grade: string }
 */
(function () {
  'use strict';

  var TOTAL_WEEKS = 15;

  function calcGrade(total) {
    if (total >= 95) return 'A+';
    if (total >= 90) return 'A';
    if (total >= 85) return 'B+';
    if (total >= 80) return 'B';
    if (total >= 75) return 'C+';
    if (total >= 70) return 'C';
    if (total >= 65) return 'D+';
    if (total >= 60) return 'D';
    return 'F';
  }

  function gradeClass(grade) {
    if (grade[0] === 'A') return 'grade-a';
    if (grade[0] === 'B') return 'grade-b';
    if (grade[0] === 'C') return 'grade-c';
    if (grade[0] === 'D') return 'grade-d';
    return 'grade-f';
  }

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'className') node.className = attrs[k];
      else if (k === 'textContent') node.textContent = attrs[k];
      else node.setAttribute(k, attrs[k]);
    });
    if (children) children.forEach(function (c) { node.appendChild(c); });
    return node;
  }

  function clear(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
  }

  function open(data) {
    var drawerEl   = document.getElementById('student-detail-drawer');
    var backdropEl = document.getElementById('student-detail-backdrop');
    if (!drawerEl) return;

    var student   = data.student;
    var assignPct = student.submissionCount / TOTAL_WEEKS * 100;
    var total     = student.attendance * 0.1 + assignPct * 0.2 +
                    student.midterm * 0.35 + student.final * 0.35;
    var grade     = calcGrade(total);

    var content = drawerEl.querySelector('.sdd-content');
    if (!content) return;
    clear(content);

    /* ── header ── */
    var hdr = el('div', {className: 'sdd-header'});
    hdr.appendChild(el('h2', {className: 'sdd-name', textContent: student.name}));
    var meta = el('div', {className: 'sdd-meta'});
    meta.appendChild(el('span', {
      className: 'sdd-class',
      textContent: student.classNum ? student.classNum + '반' : '—'
    }));
    meta.appendChild(el('span', {
      className: 'sdd-grade-badge ' + gradeClass(grade),
      textContent: grade
    }));
    hdr.appendChild(meta);
    content.appendChild(hdr);

    /* ── grade breakdown ── */
    var breakdown = el('section', {className: 'sdd-section'});
    breakdown.appendChild(el('h3', {className: 'sdd-section-title', textContent: '성적 분석'}));

    var rows = [
      {label: '출석 (×10%)',     val: student.attendance + '%',
       contrib: (student.attendance * 0.1).toFixed(1)},
      {label: '과제 (×20%)',     val: student.submissionCount + '/' + TOTAL_WEEKS +
       ' (' + assignPct.toFixed(0) + '%)',
       contrib: (assignPct * 0.2).toFixed(1)},
      {label: '중간고사 (×35%)', val: student.midterm + '점',
       contrib: (student.midterm * 0.35).toFixed(1)},
      {label: '기말고사 (×35%)', val: student.final + '점',
       contrib: (student.final * 0.35).toFixed(1)},
    ];

    var table = el('table', {className: 'sdd-table'});
    var tbody = el('tbody');
    rows.forEach(function (row) {
      var tr = el('tr');
      tr.appendChild(el('td', {textContent: row.label}));
      tr.appendChild(el('td', {className: 'sdd-td-val', textContent: row.val}));
      tr.appendChild(el('td', {className: 'sdd-td-contrib', textContent: '+' + row.contrib + '점'}));
      tbody.appendChild(tr);
    });
    /* total row */
    var totalRow = el('tr', {className: 'sdd-row-total'});
    totalRow.appendChild(el('td', {textContent: '총점'}));
    totalRow.appendChild(el('td'));
    totalRow.appendChild(el('td', {className: 'sdd-td-contrib', textContent: total.toFixed(1) + '점'}));
    tbody.appendChild(totalRow);
    table.appendChild(tbody);
    breakdown.appendChild(table);
    content.appendChild(breakdown);

    /* ── weekly submissions ── */
    var weekly = el('section', {className: 'sdd-section'});
    weekly.appendChild(el('h3', {className: 'sdd-section-title', textContent: '주차별 과제 제출'}));

    var weekGrid = el('div', {className: 'sdd-week-grid'});
    for (var i = 1; i <= TOTAL_WEEKS; i++) {
      var wn  = String(i).padStart(2, '0');
      var sub = student.weeks[wn];
      var cls = sub === true ? 'sdd-week-cell hm-yes' :
                sub === false ? 'sdd-week-cell hm-no' :
                'sdd-week-cell hm-na';
      var cell = el('div', {className: cls});
      cell.appendChild(el('span', {className: 'sdd-wk-num', textContent: 'W' + i}));
      cell.appendChild(el('span', {
        className: 'sdd-wk-icon',
        textContent: sub === true ? '✓' : sub === false ? '✗' : '—'
      }));
      weekGrid.appendChild(cell);
    }
    weekly.appendChild(weekGrid);
    content.appendChild(weekly);

    /* ── show ── */
    drawerEl.classList.add('is-open');
    drawerEl.setAttribute('aria-hidden', 'false');
    if (backdropEl) {
      backdropEl.classList.add('is-visible');
      backdropEl.setAttribute('aria-hidden', 'false');
    }

    var closeBtn = drawerEl.querySelector('.sdd-close');
    if (closeBtn) setTimeout(function () { closeBtn.focus(); }, 60);
  }

  function close() {
    var drawerEl   = document.getElementById('student-detail-drawer');
    var backdropEl = document.getElementById('student-detail-backdrop');
    if (drawerEl) {
      drawerEl.classList.remove('is-open');
      drawerEl.setAttribute('aria-hidden', 'true');
    }
    if (backdropEl) {
      backdropEl.classList.remove('is-visible');
      backdropEl.setAttribute('aria-hidden', 'true');
    }
  }

  /* wire close button + backdrop + Escape after DOM ready */
  document.addEventListener('DOMContentLoaded', function () {
    var drawerEl   = document.getElementById('student-detail-drawer');
    var backdropEl = document.getElementById('student-detail-backdrop');
    if (!drawerEl) return;

    var closeBtn = drawerEl.querySelector('.sdd-close');
    if (closeBtn) closeBtn.addEventListener('click', close);
    if (backdropEl) backdropEl.addEventListener('click', close);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      var drawerEl = document.getElementById('student-detail-drawer');
      if (drawerEl && drawerEl.classList.contains('is-open')) close();
    }
  });

  window.RPDStudentDrawer = {open: open, close: close};
})();
