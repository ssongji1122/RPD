/* student-card.js — RPD Admin: student profile card grid renderer
 * Exposes: window.RPDStudentCard.render(submissions, grades, container, onCardClick)
 */
(function () {
  'use strict';

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

  /* Build per-student map from flat submissions + grades arrays */
  function buildStudents(submissions, grades) {
    var students = {};

    grades.forEach(function (g) {
      var key = g.student_name;
      if (!students[key]) {
        students[key] = {
          name: g.student_name,
          classNum: g.class_num,
          attendance: g.attendance || 0,
          submissionCount: g.submissions || 0,
          midterm: g.midterm || 0,
          final: g.final || 0,
          weeks: {}
        };
      }
    });

    submissions.forEach(function (s) {
      var key = s.student_name;
      if (!students[key]) {
        students[key] = {
          name: s.student_name,
          classNum: s.class_num || '',
          attendance: 0,
          submissionCount: 0,
          midterm: 0,
          final: 0,
          weeks: {}
        };
      }
      var wn = s.week.replace('Week ', '');
      students[key].weeks[wn] = s.submitted;
    });

    return Object.values(students).sort(function (a, b) {
      if (a.classNum !== b.classNum) return (a.classNum || '') < (b.classNum || '') ? -1 : 1;
      return a.name < b.name ? -1 : 1;
    });
  }

  function makeProgressBar(pct, modifier) {
    var wrap = el('div', {className: 'sc-bar'});
    var fill = el('div', {className: 'sc-bar-fill' + (modifier ? ' ' + modifier : '')});
    fill.style.width = Math.min(100, Math.max(0, pct)) + '%';
    wrap.appendChild(fill);
    return wrap;
  }

  function renderStudentGrid(submissions, grades, container, onCardClick) {
    var studentList = buildStudents(submissions, grades);

    /* clear */
    while (container.firstChild) container.removeChild(container.firstChild);

    if (studentList.length === 0) {
      container.appendChild(el('p', {className: 'sc-empty',
        textContent: '학생 데이터가 없습니다. init_grading_db.py를 먼저 실행하세요.'}));
      return;
    }

    var grid = el('div', {className: 'student-grid'});

    studentList.forEach(function (student) {
      var assignPct = student.submissionCount / 15 * 100;
      var total = student.attendance * 0.1 + assignPct * 0.2 +
                  student.midterm * 0.35 + student.final * 0.35;
      var grade = calcGrade(total);

      var card = el('button', {
        className: 'student-card',
        type: 'button',
        'aria-label': student.name + ' 상세 보기'
      });

      /* ── header ── */
      var hdr = el('div', {className: 'sc-header'});
      hdr.appendChild(el('span', {className: 'sc-name', textContent: student.name}));
      hdr.appendChild(el('span', {
        className: 'sc-class',
        textContent: student.classNum ? student.classNum + '반' : '—'
      }));
      card.appendChild(hdr);

      /* ── stats ── */
      var stats = el('div', {className: 'sc-stats'});

      /* attendance row */
      var attRow = el('div', {className: 'sc-stat-row'});
      attRow.appendChild(el('span', {className: 'sc-stat-label', textContent: '출석률'}));
      attRow.appendChild(makeProgressBar(student.attendance));
      attRow.appendChild(el('span', {className: 'sc-stat-val',
        textContent: student.attendance + '%'}));
      stats.appendChild(attRow);

      /* assignment row */
      var assRow = el('div', {className: 'sc-stat-row'});
      assRow.appendChild(el('span', {className: 'sc-stat-label', textContent: '과제'}));
      assRow.appendChild(makeProgressBar(assignPct, 'sc-bar-fill--assign'));
      assRow.appendChild(el('span', {className: 'sc-stat-val',
        textContent: student.submissionCount + '/15'}));
      stats.appendChild(assRow);

      card.appendChild(stats);

      /* ── footer ── */
      var footer = el('div', {className: 'sc-footer'});
      footer.appendChild(el('span', {
        className: 'sc-grade ' + gradeClass(grade),
        textContent: grade
      }));
      footer.appendChild(el('span', {
        className: 'sc-total',
        textContent: total.toFixed(1) + '점'
      }));
      card.appendChild(footer);

      card.addEventListener('click', function () {
        if (onCardClick) onCardClick({student: student, total: total, grade: grade});
      });

      grid.appendChild(card);
    });

    container.appendChild(grid);
  }

  window.RPDStudentCard = {render: renderStudentGrid};
})();
