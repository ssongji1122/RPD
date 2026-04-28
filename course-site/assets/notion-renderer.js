(function () {
  'use strict';

  // ---------------------------------------------------------------------------
  // Rich text → inline HTML
  // ---------------------------------------------------------------------------
  function renderRichText(richText) {
    if (!Array.isArray(richText) || richText.length === 0) return '';
    return richText.map(function (span) {
      var content = span.plain_text || '';
      if (!content) return '';
      content = content
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      var ann = span.annotations || {};
      var href = (span.href) || (span.text && span.text.link && span.text.link.url) || '';
      if (ann.code) content = '<code>' + content + '</code>';
      if (ann.bold) content = '<strong>' + content + '</strong>';
      if (ann.italic) content = '<em>' + content + '</em>';
      if (ann.strikethrough) content = '<s>' + content + '</s>';
      if (ann.underline) content = '<span style="text-decoration:underline">' + content + '</span>';
      if (ann.color && ann.color !== 'default') {
        content = '<span class="nb-color-' + ann.color + '">' + content + '</span>';
      }
      if (href) content = '<a href="' + href + '" target="_blank" rel="noopener">' + content + '</a>';
      return content;
    }).join('');
  }

  // ---------------------------------------------------------------------------
  // Block renderers — simple
  // ---------------------------------------------------------------------------

  function renderHeading(block, level) {
    var tag = 'h' + level;
    var cls = 'nb-h' + level;
    var key = 'heading_' + level;
    var rt = (block[key] && block[key].rich_text) || [];
    return '<' + tag + ' class="' + cls + '">' + renderRichText(rt) + '</' + tag + '>';
  }

  function renderParagraph(block) {
    var rt = (block.paragraph && block.paragraph.rich_text) || [];
    var inner = renderRichText(rt);
    if (!inner.trim()) return '<span class="nb-spacer"></span>';
    var html = '<p class="nb-p">' + inner + '</p>';
    if (block.children && block.children.length) {
      html += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return html;
  }

  function renderDivider() {
    return '<hr class="nb-divider">';
  }

  function renderQuote(block) {
    var rt = (block.quote && block.quote.rich_text) || [];
    return '<blockquote class="nb-quote">' + renderRichText(rt) + '</blockquote>';
  }

  // ---------------------------------------------------------------------------
  // Block renderers — lists
  // ---------------------------------------------------------------------------

  function renderBulletedListItem(block) {
    var rt = (block.bulleted_list_item && block.bulleted_list_item.rich_text) || [];
    var inner = renderRichText(rt);
    if (block.children && block.children.length) {
      inner += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return '<li>' + inner + '</li>';
  }

  function renderNumberedListItem(block) {
    var rt = (block.numbered_list_item && block.numbered_list_item.rich_text) || [];
    var inner = renderRichText(rt);
    if (block.children && block.children.length) {
      inner += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return '<li>' + inner + '</li>';
  }

  // Groups consecutive same-type list items into { _grouped, tag, items[] }.
  function groupLists(blocks) {
    var result = [];
    var i = 0;
    while (i < blocks.length) {
      var b = blocks[i];
      if (b.type === 'bulleted_list_item' || b.type === 'numbered_list_item') {
        var tag = b.type === 'bulleted_list_item' ? 'ul' : 'ol';
        var group = { _grouped: true, tag: tag, items: [] };
        while (i < blocks.length && blocks[i].type === b.type) {
          group.items.push(blocks[i]);
          i++;
        }
        result.push(group);
      } else {
        result.push(b);
        i++;
      }
    }
    return result;
  }

  // ---------------------------------------------------------------------------
  // Block renderers — toggle, callout, to_do
  // ---------------------------------------------------------------------------

  function renderToggle(block) {
    var rt = (block.toggle && block.toggle.rich_text) || [];
    var summary = '<summary>' + renderRichText(rt) + '</summary>';
    var body = '';
    if (block.children && block.children.length) {
      body = '<div class="nb-toggle-body">' + renderBlockList(block.children) + '</div>';
    }
    return '<details class="nb-toggle">' + summary + body + '</details>';
  }

  function renderCallout(block) {
    var data = block.callout || {};
    var rt = data.rich_text || [];
    var icon = '';
    if (data.icon) {
      if (data.icon.type === 'emoji') icon = data.icon.emoji || '';
      else if (data.icon.type === 'external') {
        icon = '<img src="' + (data.icon.external && data.icon.external.url || '') + '" style="width:1.2em;height:1.2em;vertical-align:middle">';
      }
    }
    var color = (data.color && data.color !== 'default') ? data.color.replace('_background', '') : '';
    var colorClass = color ? ' nb-callout--' + color : '';
    var bodyHtml = '<p class="nb-p">' + renderRichText(rt) + '</p>';
    if (block.children && block.children.length) {
      bodyHtml += renderBlockList(block.children);
    }
    return '<div class="nb-callout' + colorClass + '">' +
      (icon ? '<span class="nb-callout-icon">' + icon + '</span>' : '') +
      '<div class="nb-callout-body">' + bodyHtml + '</div>' +
      '</div>';
  }

  function renderTodo(block) {
    var data = block.to_do || {};
    var rt = data.rich_text || [];
    var checked = Boolean(data.checked);
    return '<label class="nb-todo' + (checked ? ' nb-todo--checked' : '') + '">' +
      '<input type="checkbox" disabled' + (checked ? ' checked' : '') + '>' +
      '<span class="nb-todo-text">' + renderRichText(rt) + '</span>' +
      '</label>';
  }

  // ---------------------------------------------------------------------------
  // Block renderers — code, image, video, table
  // ---------------------------------------------------------------------------

  function renderCode(block) {
    var data = block.code || {};
    var rt = data.rich_text || [];
    var lang = data.language || '';
    var code = rt.map(function (s) { return s.plain_text || ''; }).join('');
    var escaped = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    var langClass = lang ? ' class="language-' + lang + '"' : '';
    var langLabel = lang ? '<span class="nb-code-lang">' + lang + '</span>' : '';
    var copyBtn = '<button class="nb-code-copy" type="button" onclick="(function(btn){var pre=btn.closest(\'.nb-code-wrap\').querySelector(\'code\');navigator.clipboard&&navigator.clipboard.writeText(pre.textContent).then(function(){btn.textContent=\'✓\';setTimeout(function(){btn.textContent=\'복사\'},1500)})})(this)">복사</button>';
    return '<div class="nb-code-wrap">' + langLabel + copyBtn +
      '<pre class="nb-code"><code' + langClass + '>' + escaped + '</code></pre></div>';
  }

  function renderImage(block) {
    var data = block.image || {};
    var src = block.local_url || '';
    if (!src) {
      if (data.type === 'file' && data.file) src = data.file.url || '';
      else if (data.type === 'external' && data.external) src = data.external.url || '';
    }
    if (!src) return '<!-- notion-block: image (no src) -->';
    var caption = (data.caption || []).map(function (s) { return s.plain_text || ''; }).join('');
    return '<figure class="nb-image"><img src="' + src + '" alt="' + (caption || 'image') + '" loading="lazy">' +
      (caption ? '<figcaption>' + caption + '</figcaption>' : '') + '</figure>';
  }

  function renderVideo(block) {
    var data = block.video || {};
    var src = '';
    if (data.type === 'external' && data.external) src = data.external.url || '';
    else if (data.type === 'file' && data.file) src = data.file.url || '';
    if (!src) return '<!-- notion-block: video (no src) -->';
    var ytMatch = src.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/))([A-Za-z0-9_-]{11})/);
    if (ytMatch) {
      return '<div class="nb-video-wrap"><iframe src="https://www.youtube.com/embed/' + ytMatch[1] + '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen title="video"></iframe></div>';
    }
    return '<div class="nb-video-wrap"><video controls preload="metadata"><source src="' + src + '"></video></div>';
  }

  function renderTable(block) {
    var hasHeader = block.table && block.table.has_column_header;
    var rows = (block.children || []).filter(function (b) { return b.type === 'table_row'; });
    if (!rows.length) return '<div class="nb-table-wrap"><table class="nb-table"></table></div>';

    var html = '<div class="nb-table-wrap"><table class="nb-table">';
    if (hasHeader && rows.length > 0) {
      var headerCells = (rows[0].table_row && rows[0].table_row.cells) || [];
      html += '<thead><tr>' + headerCells.map(function (c) { return '<th>' + renderRichText(c) + '</th>'; }).join('') + '</tr></thead>';
      html += '<tbody>';
      rows.slice(1).forEach(function (row) {
        var cells = (row.table_row && row.table_row.cells) || [];
        html += '<tr>' + cells.map(function (c) { return '<td>' + renderRichText(c) + '</td>'; }).join('') + '</tr>';
      });
      html += '</tbody>';
    } else {
      html += '<tbody>';
      rows.forEach(function (row) {
        var cells = (row.table_row && row.table_row.cells) || [];
        html += '<tr>' + cells.map(function (c) { return '<td>' + renderRichText(c) + '</td>'; }).join('') + '</tr>';
      });
      html += '</tbody>';
    }
    html += '</table></div>';
    return html;
  }

  function renderLinkToPage(block) {
    var data = block.link_to_page || {};
    var label = data.page_id ? '→ 페이지 링크' : '→ 데이터베이스 링크';
    return '<p class="nb-p"><a class="nb-link-page" href="#">' + label + '</a></p>';
  }

  // ---------------------------------------------------------------------------
  // Core dispatcher
  // ---------------------------------------------------------------------------

  function renderBlock(block) {
    var type = block.type;
    switch (type) {
      case 'heading_1':  return renderHeading(block, 1);
      case 'heading_2':  return renderHeading(block, 2);
      case 'heading_3':  return renderHeading(block, 3);
      case 'paragraph':  return renderParagraph(block);
      case 'bulleted_list_item': return renderBulletedListItem(block);
      case 'numbered_list_item': return renderNumberedListItem(block);
      case 'toggle':     return renderToggle(block);
      case 'callout':    return renderCallout(block);
      case 'to_do':      return renderTodo(block);
      case 'code':       return renderCode(block);
      case 'image':      return renderImage(block);
      case 'video':      return renderVideo(block);
      case 'table':      return renderTable(block);
      case 'table_row':  return '';
      case 'quote':      return renderQuote(block);
      case 'divider':    return renderDivider();
      case 'link_to_page': return renderLinkToPage(block);
      default:
        return '<!-- notion-block: ' + type + ' -->';
    }
  }

  // Renders a flat array of blocks, grouping consecutive list items.
  function renderBlockList(blocks) {
    var grouped = groupLists(blocks);
    return grouped.map(function (item) {
      if (item._grouped) {
        var cls = item.tag === 'ul' ? 'nb-ul' : 'nb-ol';
        return '<' + item.tag + ' class="' + cls + '">' +
          item.items.map(function (b) { return renderBlock(b); }).join('') +
          '</' + item.tag + '>';
      }
      return renderBlock(item);
    }).join('');
  }

  // Renders blocks into a DOM container element.
  function renderBlocks(blocks, container) {
    container.innerHTML = renderBlockList(blocks);
  }

  // ---------------------------------------------------------------------------
  // Page entry point
  // ---------------------------------------------------------------------------

  // Renders the full Notion block page into #pageContent.
  // notionData: { week, page_id, blocks[] }
  // weekMeta:   raw curriculum.js week object (for title, sidebar data, nav links)
  function renderNotionPage(notionData, weekMeta) {
    var w = weekMeta;
    var blocks = notionData.blocks || [];

    document.title = 'Week ' + w.week + ' — ' + w.title + ' | Blender Archive';
    var brandBadge = document.getElementById('brandBadge');
    var brandTitle = document.getElementById('brandTitle');
    if (brandBadge) brandBadge.textContent = String(w.week).padStart(2, '0');
    if (brandTitle) brandTitle.textContent = 'Week ' + String(w.week).padStart(2, '0');

    var heroHtml = '<section class="hero" id="hero-section">' +
      '<div class="hero-card rpd-panel rpd-panel--soft">' +
      '<div class="hero-header">' +
      '<span class="hero-week-well rpd-icon-well">' + String(w.week).padStart(2, '0') + '</span>' +
      '<div class="hero-copy">' +
      '<span class="hero-kicker">Week ' + String(w.week).padStart(2, '0') + '</span>' +
      '<h1>Week ' + String(w.week).padStart(2, '0') + ' \xb7 ' + (w.title || '') + '</h1>' +
      (w.subtitle ? '<p>' + w.subtitle + '</p>' : '') +
      '</div></div></div></section>';

    var contentHtml = '<section class="content-block" id="notion-body">' +
      renderBlockList(blocks) +
      '</section>';

    var refHtml = (typeof buildSidebar === 'function') ? buildSidebar(w) : '';

    var CURRICULUM = window.CURRICULUM || [];
    var prev = CURRICULUM.find(function (item) { return item.week === w.week - 1; });
    var next = CURRICULUM.find(function (item) { return item.week === w.week + 1; });
    var prevLink = prev
      ? '<a href="week.html?week=' + prev.week + '">← Week ' + prev.week + '</a>'
      : '<a href="inha.html?panel=weeks">홀으로</a>';
    var nextLink = next
      ? '<a href="week.html?week=' + next.week + '">Week ' + next.week + ' →</a>'
      : '<span style="opacity:.4">마지막 주차</span>';
    var navHtml = '<section class="content-block"><div class="week-nav">' +
      prevLink +
      '<a href="inha.html?panel=weeks" style="color:var(--muted)">전체 목록</a>' +
      nextLink +
      '</div></section>';

    var pageContent = document.getElementById('pageContent');
    if (pageContent) {
      pageContent.innerHTML = heroHtml + contentHtml + refHtml + navHtml + '<div style="height:28px"></div>';
    }
  }

  window.renderNotionPage = renderNotionPage;
  window.renderBlocks = renderBlocks;
}());
