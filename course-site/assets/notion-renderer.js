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
    var data = block[key] || {};
    var rt = data.rich_text || [];
    var isToggleable = Boolean(data.is_toggleable);
    var hasChildren = block.children && block.children.length;

    if (isToggleable) {
      var body = hasChildren
        ? '<div class="nb-toggle-body">' + renderBlockList(block.children) + '</div>'
        : '';
      return '<details class="nb-toggle nb-toggle-h' + level + '">' +
        '<summary class="' + cls + '">' + renderRichText(rt) + '</summary>' +
        body + '</details>';
    }

    var html = '<' + tag + ' class="' + cls + '">' + renderRichText(rt) + '</' + tag + '>';
    if (hasChildren) {
      html += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return html;
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
    var html = '<blockquote class="nb-quote">' + renderRichText(rt) + '</blockquote>';
    if (block.children && block.children.length) {
      html += '<div class="nb-children">' + renderBlockList(block.children) + '</div>';
    }
    return html;
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
    var bodyHtml = '<p class="nb-p">' + renderRichText(rt) + '</p>';
    if (block.children && block.children.length) {
      bodyHtml += renderBlockList(block.children);
    }
    return '<div class="nb-callout"><div class="nb-callout-body">' + bodyHtml + '</div></div>';
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
    var lang = (data.language || '').trim();
    var isPlainText = lang.toLowerCase() === 'plain text';
    var code = rt.map(function (s) { return s.plain_text || ''; }).join('');
    var escaped = code
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
    var langClass = lang && !isPlainText ? ' class="language-' + lang + '"' : '';
    var langLabel = lang ? '<span class="nb-code-lang">' + lang + '</span>' : '';
    var wrapClass = 'nb-code-wrap' + (isPlainText ? ' nb-code-wrap--plain' : '');
    var copyBtn = '<button class="nb-code-copy" type="button" onclick="(function(btn){var pre=btn.closest(\'.nb-code-wrap\').querySelector(\'code\');navigator.clipboard&&navigator.clipboard.writeText(pre.textContent).then(function(){btn.textContent=\'✓\';setTimeout(function(){btn.textContent=\'복사\'},1500)})})(this)">복사</button>';
    return '<div class="' + wrapClass + '">' + langLabel + copyBtn +
      '<pre class="nb-code"><code' + langClass + '>' + escaped + '</code></pre></div>';
  }

  function escapeAttr(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/</g, '&lt;');
  }

  function escapePlainText(value) {
    return String(value || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function resolvePayloadUrl(payload) {
    if (!payload) return '';
    if (payload.type === 'external' && payload.external) return payload.external.url || '';
    if (payload.type === 'file' && payload.file) return payload.file.url || '';
    return '';
  }

  function resolveBlockMediaSrc(block, payloadKey) {
    if (block.local_url) return block.local_url;
    return resolvePayloadUrl(block[payloadKey]);
  }

  function normalizeEmbedUrl(url) {
    if (!url) return '';
    var showmeMatch = url.match(/\/RPD\/(assets\/showme\/[^?#]+)/i);
    if (showmeMatch) return showmeMatch[1];
    return url;
  }

  function fileLabelFromBlock(block) {
    var data = block.file || {};
    if (data.name) return data.name;
    var src = resolveBlockMediaSrc(block, 'file');
    if (!src) return '파일 다운로드';
    var parts = src.split('?')[0].split('/');
    return parts[parts.length - 1] || '파일 다운로드';
  }

  function renderImage(block) {
    var data = block.image || {};
    var src = resolveBlockMediaSrc(block, 'image');
    if (!src) return '<!-- notion-block: image (no src) -->';
    var caption = (data.caption || []).map(function (s) { return s.plain_text || ''; }).join('');
    return '<figure class="nb-image"><img src="' + escapeAttr(src) + '" alt="' + escapeAttr(caption || 'image') + '" loading="lazy">' +
      (caption ? '<figcaption>' + escapePlainText(caption) + '</figcaption>' : '') + '</figure>';
  }

  function renderVideo(block) {
    var src = resolveBlockMediaSrc(block, 'video');
    if (!src) return '<!-- notion-block: video (no src) -->';
    var ytMatch = src.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([A-Za-z0-9_-]{11})/);
    if (ytMatch) {
      return '<div class="nb-video-wrap"><iframe src="https://www.youtube.com/embed/' + ytMatch[1] + '" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen title="video"></iframe></div>';
    }
    return '<div class="nb-video-wrap"><video controls preload="metadata"><source src="' + escapeAttr(src) + '"></video></div>';
  }

  function renderFile(block) {
    var data = block.file || {};
    var src = resolveBlockMediaSrc(block, 'file');
    if (!src) return '<!-- notion-block: file (no src) -->';
    var label = fileLabelFromBlock(block);
    var caption = (data.caption || []).map(function (s) { return s.plain_text || ''; }).join('');
    return '<p class="nb-file">' +
      '<a class="nb-file-link" href="' + escapeAttr(src) + '" download rel="noopener">' + escapePlainText(label) + ' ↓</a>' +
      (caption ? '<span class="nb-file-caption">' + escapePlainText(caption) + '</span>' : '') +
      '</p>';
  }

  function renderEmbed(block) {
    var data = block.embed || {};
    var url = normalizeEmbedUrl(data.url || '');
    if (!url) return '<!-- notion-block: embed (no url) -->';
    var isShowMe = /assets\/showme\/.+\.html$/i.test(url);
    var wrapClass = isShowMe ? 'nb-embed nb-embed-showme' : 'nb-embed';
    var title = isShowMe ? 'Show Me card' : 'embedded content';
    return '<div class="' + wrapClass + '"><iframe src="' + escapeAttr(url) + '" title="' + escapeAttr(title) + '" loading="lazy"></iframe></div>';
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

  function _escapeHtml(str) {
    return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function _subpageHref(pageId) {
    var id = (pageId || '').replace(/-/g, '');
    return 'subpage.html?id=' + id;
  }

  function renderLinkToPage(block) {
    var data = block.link_to_page || {};
    if (data.type === 'page_id' && data.page_id) {
      var subpageTitle = (block.linked_page_title || block._resolved_title || '').trim() || '관련 자료';
      return '<p class="nb-p"><a class="nb-link-page nb-link-subpage" href="'
        + _subpageHref(data.page_id) + '">' + escapePlainText(subpageTitle) + '</a></p>';
    }
    var pageId = data.page_id || '';
    var title = block.linked_page_title || '';
    var url = block.linked_page_url || (pageId ? 'https://www.notion.so/' + String(pageId).replace(/-/g, '') : '');
    var label = title || (pageId ? 'Notion 페이지에서 열기' : 'Notion 데이터베이스');
    if (!url) {
      return '<p class="nb-p nb-link-page-wrap"><span class="nb-link-page nb-link-page--missing">' + escapePlainText(label) + '</span></p>';
    }
    return '<p class="nb-p nb-link-page-wrap"><a class="nb-link-page" href="' + escapeAttr(url) + '" target="_blank" rel="noopener">' + escapePlainText(title || label) + ' ↗</a></p>';
  }

  function renderChildPage(block) {
    var childTitle = ((block.child_page || {}).title || '').trim() || '하위 페이지';
    return '<p class="nb-p"><a class="nb-link-page nb-link-subpage" href="'
      + _subpageHref(block.id) + '">' + escapePlainText(childTitle) + '</a></p>';
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
      case 'heading_4':  return renderHeading(block, 4);
      case 'paragraph':  return renderParagraph(block);
      case 'bulleted_list_item': return renderBulletedListItem(block);
      case 'numbered_list_item': return renderNumberedListItem(block);
      case 'toggle':     return renderToggle(block);
      case 'callout':    return renderCallout(block);
      case 'to_do':      return renderTodo(block);
      case 'code':       return renderCode(block);
      case 'image':      return renderImage(block);
      case 'video':      return renderVideo(block);
      case 'file':       return renderFile(block);
      case 'embed':      return renderEmbed(block);
      case 'table':      return renderTable(block);
      case 'table_row':  return '';
      case 'quote':      return renderQuote(block);
      case 'divider':    return renderDivider();
      case 'link_to_page': return renderLinkToPage(block);
      case 'child_page':   return renderChildPage(block);
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
    var localized = (window.RPDI18n && typeof window.RPDI18n.localizeWeekData === 'function')
      ? window.RPDI18n.localizeWeekData(w)
      : w;
    var preset = (window.RPDWeekUI && typeof window.RPDWeekUI.getPreset === 'function')
      ? window.RPDWeekUI.getPreset()
      : {};
    var lang = (window.RPDI18n && typeof window.RPDI18n.getLanguage === 'function')
      ? window.RPDI18n.getLanguage()
      : 'ko';
    var heroEyebrow = (preset.labels && preset.labels.heroEyebrow)
      ? (window.RPDWeekUI
        ? window.RPDWeekUI.localize(preset.labels.heroEyebrow, lang, '')
        : (preset.labels.heroEyebrow.ko || preset.labels.heroEyebrow.en || ''))
      : '';
    var weekNum = String(w.week).padStart(2, '0');
    var pageTitle = localized.title || w.title || '';

    document.title = 'Week ' + w.week + ' — ' + pageTitle + ' | Blender Archive';
    var brandBadge = document.getElementById('brandBadge');
    var brandTitle = document.getElementById('brandTitle');
    if (brandBadge) brandBadge.textContent = weekNum;
    if (brandTitle) brandTitle.textContent = pageTitle;

    var heroHtml = '<section class="hero" id="hero-section">' +
      '<div class="hero-card rpd-panel rpd-panel--soft">' +
      '<div class="hero-header">' +
      '<span class="hero-week-well rpd-icon-well" aria-hidden="true">' + weekNum + '</span>' +
      '<div class="hero-copy">' +
      (heroEyebrow ? '<span class="hero-kicker">' + heroEyebrow + '</span>' : '') +
      '<h1>' + pageTitle + '</h1>' +
      (localized.subtitle ? '<p>' + localized.subtitle + '</p>' : '') +
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
      : '<a href="inha.html?panel=weeks">홈으로</a>';
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
