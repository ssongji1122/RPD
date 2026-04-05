(function(win) {
  "use strict";

  var STORAGE_KEY = "rpd-lang";
  var SUPPORTED_LANGS = ["ko", "en"];

  var COPY = {
    common: {
      ko: {
        languageSwitcherAria: "언어 전환",
        langKo: "KO",
        langEn: "EN",
      },
      en: {
        languageSwitcherAria: "Switch language",
        langKo: "KO",
        langEn: "EN",
      },
    },
    index: {
      ko: {
        pageTitle: "Edu Home — RPD",
        metaDescription: "RPD 학습 허브 — 인하대학교 RPD 수업의 통합 진입점",
        topbarTitle: "Edu Home",
        topbarMeta: "Edu Home · Inha University",
        libraryLink: "◫ 카드 라이브러리",
        shortcutsLink: "\u2328 단축키 DB",
        themeToggleAria: "테마 전환",
        heroEyebrow: "Edu Home",
        heroTitle: "학습 허브",
        heroDescription: "이번 주 실습, Show Me 카드, 참고자료를 한곳에서. 인하대 RPD 수업의 통합 진입점이에요.",
        heroMetaLabel: "학습 구조",
        heroMetaArchive: "Show Me 카드 · 단축키 · 실습",
        heroMetaProgram: "인하대학교 RPD 컬렉션",
        heroMetaActivePrefix: "현재 주차",
        heroMetaActiveFallback: "활성 주차 준비 중",
        heroPrimaryCta: "이번 주 시작하기",
        heroSecondaryCta: "카드 라이브러리",
        heroTertiaryCta: "단축키 DB 보기",
        archiveSectionEyebrow: "학습 자료",
        archiveSectionTitle: "수업 자료가 이렇게 나뉘어 있어요",
        archiveSectionDescription: "도구 설명과 단축키는 따로 정리해두고, 각 주차 수업에서 필요한 것만 가져다 써요.",
        archiveCardLibraryKicker: "Card Library",
        archiveCardLibraryTitle: "Show Me 카드 라이브러리",
        archiveCardLibraryCopy: "도구와 개념 카드를 이름으로 찾고, 어떤 수업에서도 재사용할 수 있게 모아둡니다.",
        archiveCardLibraryMeta: "개의 카드",
        archiveCardShortcutKicker: "Shortcut Base",
        archiveCardShortcutTitle: "단축키 DB",
        archiveCardShortcutCopy: "주차마다 흩어진 단축키를 공통 DB로 분리해서 필요한 수업에만 다시 조합합니다.",
        archiveCardShortcutMeta: "개의 단축키",
        archiveCardAssemblyKicker: "Course Assembly",
        archiveCardAssemblyTitle: "주차별 학습 구성",
        archiveCardAssemblyCopy: "실습 카드와 Show Me 카드, 참고 자료를 묶어 주차별 학습 경로로 보여줍니다.",
        archiveCardAssemblyMeta: "주차",
        programEyebrow: "커리큘럼",
        programTitle: "인하대학교 · Robot Product Design",
        programDescription: "15주 RPD 수업 커리큘럼이에요. 각 주차를 클릭하면 실습 카드, 참고자료, 과제를 확인할 수 있어요.",
        programStatWeeks: "주차",
        programStatCards: "연결된 카드",
        programStatActive: "현재 진행 주차",
        weekSectionEyebrow: "커리큘럼 타임라인",
        weekSectionTitle: "주차별 학습 경로",
        weekSectionDescription: "매주 배울 실습, 참고자료, 과제를 한 페이지에 모아뒀어요.",
        footerLabel: "Edu Home · RPD 2026",
        activeLabel: "현재 주차",
        badgeExam: "시험 주차",
        badgeDone: "완료",
        badgeActive: "진행 중",
        badgeUpcoming: "예정",
        weekMetricCards: "카드",
        weekMetricTasks: "체크포인트",
        weekMetricRefs: "참고",
        phaseBasics: "기초",
        phaseModeling: "모델링",
        phaseShading: "셰이딩",
        phaseMidterm: "중간평가",
        phaseAnimation: "애니메이션",
        phaseFinal: "마무리",
        featuredEmpty: "진행 중인 주차가 없어요",
        eduRefsEyebrow: "이번 주 참고자료",
        eduRefsTitle: "Notion 튜토리얼",
        eduRefsMore: "이 주차 전체 참고자료 보기 →",
        eduRefsOpenLabel: "Notion에서 열기",
      },
      en: {
        pageTitle: "Edu Home — RPD",
        metaDescription: "RPD learning hub — the unified entry point for Inha University RPD",
        topbarTitle: "Edu Home",
        topbarMeta: "Edu Home · Inha University",
        libraryLink: "◫ Card Library",
        shortcutsLink: "\u2328 Shortcuts DB",
        themeToggleAria: "Toggle theme",
        heroEyebrow: "Edu Home",
        heroTitle: "Your learning hub",
        heroDescription: "This week's practice, Show Me cards, and references — all in one place. The unified entry point for RPD.",
        heroMetaLabel: "Learning structure",
        heroMetaArchive: "Show Me cards · Shortcuts · Practice",
        heroMetaProgram: "Inha University RPD collection",
        heroMetaActivePrefix: "Current week",
        heroMetaActiveFallback: "No active week yet",
        heroPrimaryCta: "Start this week",
        heroSecondaryCta: "Card library",
        heroTertiaryCta: "View shortcuts DB",
        archiveSectionEyebrow: "Learning materials",
        archiveSectionTitle: "The course materials are organized like this",
        archiveSectionDescription: "Keep the reusable cards and shortcuts in one place, then assemble only the lesson pages you need.",
        archiveCardLibraryKicker: "Card Library",
        archiveCardLibraryTitle: "Show Me card library",
        archiveCardLibraryCopy: "Find tool and concept cards by name and reuse them across any course page.",
        archiveCardLibraryMeta: "cards",
        archiveCardShortcutKicker: "Shortcut Base",
        archiveCardShortcutTitle: "Shortcut DB",
        archiveCardShortcutCopy: "Pull shortcuts out of each week and keep them in one shared database you can recombine later.",
        archiveCardShortcutMeta: "shortcuts",
        archiveCardAssemblyKicker: "Course Assembly",
        archiveCardAssemblyTitle: "Weekly lesson path",
        archiveCardAssemblyCopy: "Bundle practice cards, Show Me cards, and references into a weekly learning path.",
        archiveCardAssemblyMeta: "weeks",
        programEyebrow: "Curriculum",
        programTitle: "Inha University · Robot Product Design",
        programDescription: "The 15-week RPD curriculum. Click any week to see its practice cards, references, and assignments.",
        programStatWeeks: "weeks",
        programStatCards: "linked cards",
        programStatActive: "current week",
        weekSectionEyebrow: "Curriculum timeline",
        weekSectionTitle: "Weekly learning path",
        weekSectionDescription: "Each week bundles the practice cards, Show Me cards, and references needed for that lesson.",
        footerLabel: "Edu Home · RPD 2026",
        activeLabel: "Current week",
        badgeExam: "Exam Week",
        badgeDone: "Done",
        badgeActive: "In Progress",
        badgeUpcoming: "Upcoming",
        weekMetricCards: "cards",
        weekMetricTasks: "checkpoints",
        weekMetricRefs: "refs",
        phaseBasics: "Basics",
        phaseModeling: "Modeling",
        phaseShading: "Shading",
        phaseMidterm: "Midterm",
        phaseAnimation: "Animation",
        phaseFinal: "Final",
        featuredEmpty: "No active week right now",
        eduRefsEyebrow: "This week's references",
        eduRefsTitle: "Notion tutorials",
        eduRefsMore: "View all references for this week →",
        eduRefsOpenLabel: "Open in Notion",
      },
    },
    week: {
      ko: {
        pageTitlePrefix: "Week",
        metaDescription: "Blender Archive 기반 RPD 주차 페이지",
        sidebarToggleAria: "목차 열기",
        brandLoading: "불러오는 중...",
        brandMeta: "Blender Archive · Inha University",
        shortcutsLink: "\u2328 단축키 DB",
        aiRefsLink: "\ud83e\udd16 AI 참고자료",
        blenderRefsLink: "\ud83d\udd27 블렌더 참고자료",
        themeToggleAria: "테마 전환",
        progressLabel: "진도",
        resetButton: "초기화",
        footerHome: "\u2190 Blender Archive",
        footerLibrary: "카드 라이브러리",
        modalResizeAria: "크기 전환",
        modalBrowseToggleAria: "Show Me 탐색 전환",
        modalCloseAria: "닫기",
        showmeFrameTitle: "Show Me 카드",
        modalBrowseSearchAria: "Show Me 카드 검색",
        modalBrowseSearchPlaceholder: "이번 주 카드나 연관 키워드 검색",
        modalBrowseContextHint: "이 브라우저는 이번 주 카드와 연관 카드만 빠르게 보여줍니다.",
        modalBrowseCurrent: "이번 주 카드",
        modalBrowseRelated: "연관 카드",
        modalBrowseResults: "검색 결과",
        modalBrowseEmpty: "조건에 맞는 카드가 없습니다.",
        modalBrowseResetCta: "이번 주 카드 보기",
        modalBrowseLibraryLink: "문서형 전체 라이브러리 열기",
        showMeRelatedPrompt: "연관 카드를 더 볼까요?",
        showMeRelatedMore: "더 보기",
        modalCurrentCardKicker: "현재 카드",
        modalCurrentCardFallbackMeta: "이 카드를 기준으로 같은 주차와 연관 카드를 탐색할 수 있어요.",
        modalBrowserViewing: "보고 있는 카드",
        loginTitle: "\ud83d\udc4b 바로 시작하세요",
        loginSubtitle: "퀴즈 기록은 이 브라우저에만 저장됩니다",
        loginPlaceholder: "이름 없이 사용 가능",
        guestBrowse: "바로 둘러보기",
        notFound: "해당 주차 데이터를 찾을 수 없습니다.",
        notFoundBack: "\u2190 Blender Archive",
        homeLabel: "\u2190 Blender Archive",
        listLabel: "아카이브",
        lastWeek: "마지막 주차",
        heroEyebrow: "Blender Archive · Inha University",
        learningEyebrow: "Student Flow",
        learningStartTitle: "지금 바로 이번 주 학습을 시작하세요.",
        learningContinueTitle: "여기서부터 이어서 학습하세요.",
        learningCompleteTitle: "이번 주 핵심 흐름을 모두 마쳤어요.",
        learningPanelCopy: "체크한 학습 항목과 Show Me 퀴즈 결과는 이 브라우저에 저장됩니다.",
        learningPrimaryStart: "학습 시작",
        learningPrimaryContinue: "이어서 학습",
        learningPrimaryReview: "다시 훑어보기",
        learningSecondaryShowme: "관련 Show Me 열기",
        learningAssignmentCta: "과제 보기",
        learningProgressSteps: "학습 단계",
        learningProgressShowme: "Show Me 퀴즈",
        learningProgressStorage: "저장 위치",
        learningProgressStorageValue: "이 브라우저",
        bundleChip: "조합 구조",
        bundleTitle: "이 페이지는 인하대학교 RPD에 맞춰 조합된 수업 페이지예요.",
        bundleDescription: "공통 Blender Archive에서 필요한 실습 카드와 Show Me 카드, 참고 자료만 묶어 이번 주 수업 흐름으로 재배치했어요.",
        bundleHomeLink: "Blender Archive 홈",
        bundleLibraryLink: "문서형 Show Me 라이브러리",
        bundleShortcutsLink: "단축키 DB",
        bundleStatPractice: "실습 카드",
        bundleStatShowme: "Show Me 카드",
        bundleStatTasks: "체크포인트",
        bundleStatReferences: "참고 자료",
        sectionPractice: "실습",
        taskGroupLabel: "체크리스트",
        sectionPracticeDesc: "",
        sectionMistakes: "막히는 지점",
        sectionMistakesSummary: "막혔을 때",
        sectionVideos: "공식 영상 튜토리얼",
        sectionDocs: "공식 문서",
        sectionAssignment: "과제",
        assignmentChip: "과제",
        assignmentStatusReady: "제출 준비됨",
        assignmentStatusDraft: "진행 중",
        assignmentProgressMeta: "학습 단계",
        assignmentChecklistMeta: "제출 체크",
        assignmentReadyAction: "제출 준비 완료 표시",
        assignmentUndoAction: "제출 준비 표시 해제",
        assignmentReviewCta: "실습 다시 보기",
        assignmentShowMeCta: "관련 Show Me 열기",
        assignmentStorageNote: "과제 준비 상태는 이 브라우저에만 저장됩니다.",
        toastQuizSaved: "퀴즈 기록을 저장했어요.",
        toastAssignmentReady: "제출 준비 완료로 표시했어요.",
        toastAssignmentDraft: "제출 준비 표시를 해제했어요.",
        toastProgressReset: "이번 주 학습 체크를 초기화했어요.",
        sectionShortcuts: "단축키 치트시트",
        sectionShortcutsDesc: "이번 주에 쓰는 핵심 단축키입니다. 외우지 말고 반복하세요.",
        shortcutsHeaderKeys: "단축키",
        shortcutsHeaderAction: "기능",
        sectionExplore: "더 해보기",
        sectionExploreDesc: "필수는 아니지만, 도전하면 실력이 빠르게 늡니다.",
        stepStatusActive: "진행 중",
        stepStatusComplete: "완료",
        stepToggleExpand: "실습 내용 열기",
        stepToggleCollapse: "실습 내용 접기",
        stepMetaTasks: "체크",
        stepMetaClips: "클립",
        stepMetaShowMe: "Show Me",
        stepMetaReferences: "레퍼런스",
        stepMetaDownloads: "다운로드",
        clipHint: "클릭하면 일시정지 · 다시 클릭하면 재생",
        clipTitle: "클릭하면 일시정지/재생",
        sidebarOverview: "개요",
        sidebarBundle: "수업 구조",
        sidebarPracticeGroup: "실습",
        sidebarReferenceGroup: "참고",
        sidebarShortcuts: "단축키",
        sidebarExplore: "더 해보기",
        sidebarMistakes: "막히는 지점",
        sidebarAssignment: "과제",
        sidebarShowMe: "Show Me",
        conceptVizTitle: "개념 이해 시각화",
        conceptWithout: "WITHOUT",
        conceptWith: "WITH",
        interactionTab: "직접 해보기",
      },
      en: {
        pageTitlePrefix: "Week",
        metaDescription: "RPD weekly page assembled from Blender Archive cards",
        sidebarToggleAria: "Open outline",
        brandLoading: "Loading...",
        brandMeta: "Blender Archive · Inha University",
        shortcutsLink: "\u2328 Shortcuts DB",
        aiRefsLink: "\ud83e\udd16 AI Reference",
        blenderRefsLink: "\ud83d\udd27 Blender Reference",
        themeToggleAria: "Toggle theme",
        progressLabel: "Progress",
        resetButton: "Reset",
        footerHome: "\u2190 Blender Archive",
        footerLibrary: "Card Library",
        modalResizeAria: "Toggle size",
        modalBrowseToggleAria: "Toggle Show Me browser",
        modalCloseAria: "Close",
        showmeFrameTitle: "Show Me card",
        modalBrowseSearchAria: "Search Show Me cards",
        modalBrowseSearchPlaceholder: "Search this week's cards or related keywords",
        modalBrowseContextHint: "This browser stays focused on this week's cards and closely related cards.",
        modalBrowseCurrent: "This week",
        modalBrowseRelated: "Related cards",
        modalBrowseResults: "Search results",
        modalBrowseEmpty: "No cards match this view.",
        modalBrowseResetCta: "Back to this week",
        modalBrowseLibraryLink: "Open document-style full library",
        showMeRelatedPrompt: "Want to view related cards?",
        showMeRelatedMore: "More",
        modalCurrentCardKicker: "Current card",
        modalCurrentCardFallbackMeta: "Use this card as the current reference while exploring this week's and related cards.",
        modalBrowserViewing: "Viewing",
        loginTitle: "\ud83d\udc4b Start right away",
        loginSubtitle: "Quiz progress is stored only in this browser",
        loginPlaceholder: "No sign-in required",
        guestBrowse: "Start browsing",
        notFound: "We couldn't find data for this week.",
        notFoundBack: "\u2190 Blender Archive",
        homeLabel: "\u2190 Blender Archive",
        listLabel: "Archive",
        lastWeek: "Last week",
        heroEyebrow: "Blender Archive · Inha University",
        learningEyebrow: "Student Flow",
        learningStartTitle: "Start this week's lesson now.",
        learningContinueTitle: "Pick up the lesson from here.",
        learningCompleteTitle: "You've finished the core flow for this week.",
        learningPanelCopy: "Checked learning items and Show Me quiz results are stored in this browser.",
        learningPrimaryStart: "Start lesson",
        learningPrimaryContinue: "Continue lesson",
        learningPrimaryReview: "Review flow",
        learningSecondaryShowme: "Open related Show Me",
        learningAssignmentCta: "View assignment",
        learningProgressSteps: "Lesson steps",
        learningProgressShowme: "Show Me quizzes",
        learningProgressStorage: "Storage",
        learningProgressStorageValue: "This browser",
        bundleChip: "Assembly",
        bundleTitle: "This page is an Inha University lesson assembled for RPD.",
        bundleDescription: "It pulls only the practice cards, Show Me cards, and references needed this week out of the shared Blender Archive.",
        bundleHomeLink: "Blender Archive home",
        bundleLibraryLink: "Document-style Show Me library",
        bundleShortcutsLink: "Shortcuts DB",
        bundleStatPractice: "practice cards",
        bundleStatShowme: "Show Me cards",
        bundleStatTasks: "checkpoints",
        bundleStatReferences: "references",
        sectionPractice: "Practice",
        taskGroupLabel: "Checklist",
        sectionPracticeDesc: "",
        sectionMistakes: "Troubleshooting",
        sectionMistakesSummary: "If you're stuck",
        sectionVideos: "Official Video Tutorials",
        sectionDocs: "Official Documentation",
        sectionAssignment: "Assignment",
        assignmentChip: "Assignment",
        assignmentStatusReady: "Ready to submit",
        assignmentStatusDraft: "In progress",
        assignmentProgressMeta: "Lesson steps",
        assignmentChecklistMeta: "Submission checks",
        assignmentReadyAction: "Mark ready to submit",
        assignmentUndoAction: "Remove ready mark",
        assignmentReviewCta: "Review lesson",
        assignmentShowMeCta: "Open related Show Me",
        assignmentStorageNote: "Assignment readiness is stored only in this browser.",
        toastQuizSaved: "Saved your quiz progress.",
        toastAssignmentReady: "Marked this assignment as ready to submit.",
        toastAssignmentDraft: "Removed the ready-to-submit mark.",
        toastProgressReset: "Reset this week's learning checks.",
        sectionShortcuts: "Shortcut Cheat Sheet",
        sectionShortcutsDesc: "These are the key shortcuts for this week. Don't memorize them all at once. Repeat them in practice.",
        shortcutsHeaderKeys: "Shortcut",
        shortcutsHeaderAction: "Action",
        sectionExplore: "Go Further",
        sectionExploreDesc: "Optional, but tackling these challenges will level you up quickly.",
        stepStatusActive: "In Progress",
        stepStatusComplete: "Done",
        stepToggleExpand: "Expand lesson details",
        stepToggleCollapse: "Collapse lesson details",
        stepMetaTaskSingular: "task",
        stepMetaTaskPlural: "tasks",
        stepMetaClipSingular: "clip",
        stepMetaClipPlural: "clips",
        stepMetaShowMeSingular: "Show Me card",
        stepMetaShowMePlural: "Show Me cards",
        stepMetaReferenceSingular: "reference",
        stepMetaReferencePlural: "references",
        stepMetaDownloadSingular: "download",
        stepMetaDownloadPlural: "downloads",
        clipHint: "Click to pause. Click again to play.",
        clipTitle: "Click to pause or play",
        sidebarOverview: "Overview",
        sidebarBundle: "Assembly",
        sidebarPracticeGroup: "Practice",
        sidebarReferenceGroup: "Reference",
        sidebarShortcuts: "Shortcuts",
        sidebarExplore: "Go Further",
        sidebarMistakes: "Troubleshooting",
        sidebarAssignment: "Assignment",
        sidebarShowMe: "Show Me",
        conceptVizTitle: "Concept Visualization",
        conceptWithout: "WITHOUT",
        conceptWith: "WITH",
        interactionTab: "Try It",
      },
    },
    library: {
      ko: {
        pageTitle: "Show Me 카드 라이브러리 - Blender Archive",
        metaDescription: "Blender Archive 안의 Show Me 카드를 Blender 공식 문서 흐름에 맞춰 찾는 라이브러리",
        backHome: "\u2190 Blender Archive",
        title: "Show Me 카드 라이브러리",
        subtitle: "큰 흐름으로 먼저 보고, 필요하면 검색과 ABC로 바로 좁혀보세요",
        searchAria: "도구 검색",
        searchPlaceholder: "예: Array, Mirror, UV...",
        categoryFilterAria: "카테고리 필터",
        tocAria: "라이브러리 목차",
        alphabetFilterAria: "ABC 필터",
        contentsLabel: "목차",
        alphabetLabel: "ABC",
        allLetters: "전체",
        sectionGettingStartedTitle: "시작 준비",
        sectionGettingStartedCopy: "환경 설정과 레퍼런스 준비처럼 Blender에 들어가기 전에 먼저 잡아야 하는 시작 단계를 모았습니다.",
        sectionUserInterfaceTitle: "기초 조작과 작업 흐름",
        sectionUserInterfaceCopy: "화면 조작, 축 기준, Pivot, 스냅처럼 Blender 인터페이스를 읽는 법과 기본 조작 감각을 먼저 정리합니다.",
        sectionModelingTitle: "모델링",
        sectionModelingCopy: "형태를 만들고 다듬는 핵심 구간입니다. Edit Mode 도구, Modifier, 정리용 개념을 한 흐름으로 묶었습니다.",
        sectionSculptingPaintingTitle: "스컬프팅 · 페인팅",
        sectionSculptingPaintingCopy: "브러시 기반으로 형태를 밀고 다듬는 흐름을 따로 모았습니다.",
        sectionMaterialsUvTitle: "셰이딩 · 재질 · UV",
        sectionMaterialsUvCopy: "재질 표현과 UV 준비를 함께 보게 해 Shader와 Texture 흐름을 한 번에 찾도록 구성했습니다.",
        sectionRenderingTitle: "렌더링",
        sectionRenderingCopy: "조명 세팅부터 렌더 엔진, 컴포지팅까지 최종 출력 단계에서 필요한 카드를 모았습니다.",
        sectionAnimationRiggingTitle: "애니메이션 · 리깅",
        sectionAnimationRiggingCopy: "키프레임, 그래프 편집, Armature, Weight Paint처럼 움직임과 캐릭터 제어에 필요한 주제를 묶었습니다.",
        modalCloseAria: "닫기",
        showmeFrameTitle: "Show Me Widget",
        emptyResults: "검색 결과가 없습니다",
      },
      en: {
        pageTitle: "Show Me Card Library - Blender Archive",
        metaDescription: "A Show Me card library organized around the Blender Manual flow",
        backHome: "\u2190 Blender Archive",
        title: "Show Me Card Library",
        subtitle: "Start from the main flow, then narrow down with search and ABC when needed",
        searchAria: "Search tools",
        searchPlaceholder: "e.g. Array, Mirror, UV...",
        categoryFilterAria: "Category filter",
        tocAria: "Library table of contents",
        alphabetFilterAria: "ABC filter",
        contentsLabel: "Contents",
        alphabetLabel: "ABC",
        allLetters: "All",
        sectionGettingStartedTitle: "Getting Started",
        sectionGettingStartedCopy: "This gathers the first setup steps you usually need before real work begins, including preferences and reference prep.",
        sectionUserInterfaceTitle: "User Interface",
        sectionUserInterfaceCopy: "Viewport movement, axis logic, pivot rules, snapping, and basic interaction concepts live here.",
        sectionModelingTitle: "Modeling",
        sectionModelingCopy: "The main shape-making area. Core modeling tools, modifier workflows, and cleanup concepts are grouped into one flow.",
        sectionSculptingPaintingTitle: "Sculpting & Painting",
        sectionSculptingPaintingCopy: "Brush-based form building and surface refinement live here.",
        sectionMaterialsUvTitle: "Shading, Materials & UV",
        sectionMaterialsUvCopy: "Material setup and UV preparation are grouped together so shader and texture concepts are easier to scan in one pass.",
        sectionRenderingTitle: "Rendering",
        sectionRenderingCopy: "Lighting, render engines, and compositing are grouped as the final output stage.",
        sectionAnimationRiggingTitle: "Animation & Rigging",
        sectionAnimationRiggingCopy: "Cards about time, keyframes, bones, and character control live together here.",
        modalCloseAria: "Close",
        showmeFrameTitle: "Show Me widget",
        emptyResults: "No results found",
      },
    },
    shortcuts: {
      ko: {
        pageTitle: "단축키 DB - RPD",
        metaDescription: "Blender 단축키 전체 검색 - Robot Product Design",
        brandTitle: "Blender Shortcuts DB",
        brandMeta: "Robot Product Design · 2026",
        backToList: "\u2190 전체 목록",
        heroEyebrow: "Blender Shortcuts",
        heroTitle: "단축키 DB",
        heroDescription: "수업용 단축키를 빠르게 찾고 바로 확인합니다.",
        heroPrimaryCta: "\u2328 키보드 맵 보기",
        heroSecondaryCta: "현재 주차 보기",
        heroTertiaryCta: "카드 라이브러리",
        searchPlaceholder: "단축키 또는 기능 검색... (예: Ctrl+R, Extrude, 이동)",
        searchAria: "단축키 검색",
        categoryFilterAria: "카테고리 필터",
        viewModeAria: "보기 방식",
        viewList: "목록",
        viewKeyboard: "\u2328 키보드",
        footerBack: "\u2190 전체 목록",
        allFilter: "전체",
        emptyResults: "검색 결과가 없습니다. 다른 키워드로 시도해보세요.",
        keyboardMapAria: "Blender 키보드 단축키 맵",
        numpadLabel: "NUMPAD",
        mouseLabel: "마우스",
      },
      en: {
        pageTitle: "Shortcuts DB - RPD",
        metaDescription: "Search every Blender shortcut used in Robot Product Design",
        brandTitle: "Blender Shortcuts DB",
        brandMeta: "Robot Product Design · 2026",
        backToList: "\u2190 All Weeks",
        heroEyebrow: "Blender Shortcuts",
        heroTitle: "Shortcuts DB",
        heroDescription: "Quickly find the class shortcuts you need and check them right away.",
        heroPrimaryCta: "\u2328 View keyboard map",
        heroSecondaryCta: "Go to current week",
        heroTertiaryCta: "Card library",
        searchPlaceholder: "Search shortcuts or actions... (e.g. Ctrl+R, Extrude, Move)",
        searchAria: "Search shortcuts",
        categoryFilterAria: "Category filter",
        viewModeAria: "View mode",
        viewList: "List",
        viewKeyboard: "\u2328 Keyboard",
        footerBack: "\u2190 All Weeks",
        allFilter: "All",
        emptyResults: "No results found. Try a different keyword.",
        keyboardMapAria: "Blender keyboard shortcut map",
        numpadLabel: "NUMPAD",
        mouseLabel: "Mouse",
      },
    },
  };

  var SHOWME_LABELS = {
    "image-reference": { ko: "이미지 레퍼런스 설정", en: "Image Reference Setup" },
    "blender-preferences": { ko: "Preferences 설정", en: "Preferences Setup" },
    "viewport-navigation": { ko: "화면 조작 원리", en: "Viewport Navigation" },
    "transform-grs": { ko: "G/R/S 변형 이해", en: "Understanding G/R/S" },
    "transform-orientation": { ko: "Transform Orientation 이해", en: "Transform Orientation" },
    "pivot-point": { ko: "Pivot Point 이해", en: "Pivot Point" },
    "snap": { ko: "Snapping 이해", en: "Snapping" },
    "viewport-shading": { ko: "Viewport Shading 이해", en: "Viewport Shading" },
    "xray-opacity": { ko: "X-Ray 투명도 조절", en: "X-Ray Opacity" },
    "edit-mode": { ko: "Edit Mode 이해", en: "Edit Mode" },
    "edit-mode-tools": { ko: "Edit Mode 도구 전체", en: "Edit Mode Toolset" },
    "extrude": { ko: "Extrude 작동 원리", en: "Extrude" },
    "loop-cut": { ko: "Loop Cut 이해", en: "Loop Cut" },
    "inset": { ko: "Inset 작동 원리", en: "Inset" },
    "bevel-tool": { ko: "Bevel Tool 이해", en: "Bevel Tool" },
    "array-modifier": { ko: "Array Modifier 이해", en: "Array Modifier" },
    "bevel-modifier": { ko: "Bevel Modifier 이해", en: "Bevel Modifier" },
    "boolean-modifier": { ko: "Boolean 작동 원리", en: "Boolean" },
    "build-modifier": { ko: "Build Modifier 이해", en: "Build Modifier" },
    "curve-to-tube": { ko: "Curve to Tube 이해", en: "Curve to Tube" },
    "decimate-modifier": { ko: "Decimate 이해", en: "Decimate" },
    "edge-split-modifier": { ko: "Edge Split 이해", en: "Edge Split" },
    "mask-modifier": { ko: "Mask Modifier 이해", en: "Mask Modifier" },
    "mirror-modifier": { ko: "Mirror Modifier 이해", en: "Mirror Modifier" },
    "mirror-workflow": { ko: "Mirror 작업 흐름", en: "Mirror Workflow" },
    "mirror-origin-mode": { ko: "Mirror·Origin·모드 이해", en: "Mirror, Origin, and Modes" },
    "multiresolution-modifier": { ko: "Multiresolution 이해", en: "Multiresolution" },
    "remesh-modifier": { ko: "Remesh 이해", en: "Remesh" },
    "scatter-on-surface": { ko: "Scatter on Surface 이해", en: "Scatter on Surface" },
    "screw-modifier": { ko: "Screw Modifier 이해", en: "Screw Modifier" },
    "skin-modifier": { ko: "Skin Modifier 이해", en: "Skin Modifier" },
    "solidify-modifier": { ko: "Solidify 이해", en: "Solidify" },
    "subdivision-surface": { ko: "Subdivision Surface 이해", en: "Subdivision Surface" },
    "triangulate-modifier": { ko: "Triangulate 이해", en: "Triangulate" },
    "volume-to-mesh": { ko: "Volume to Mesh 이해", en: "Volume to Mesh" },
    "weld-modifier": { ko: "Weld Modifier 이해", en: "Weld Modifier" },
    "wireframe-modifier": { ko: "Wireframe 이해", en: "Wireframe" },
    "weighted-normal": { ko: "Weighted Normal 이해", en: "Weighted Normal" },
    "proportional-editing": { ko: "Proportional Editing 이해", en: "Proportional Editing" },
    "transform-apply": { ko: "Apply Transform 이해", en: "Apply Transform" },
    "simple-deform": { ko: "Simple Deform 이해", en: "Simple Deform" },
    "bevel-tool-vs-modifier": { ko: "Bevel 비교", en: "Bevel Comparison" },
    "join-separate": { ko: "Join/Separate 이해", en: "Join / Separate" },
    "sculpt-basics": { ko: "Sculpt Mode 기초", en: "Sculpt Mode Basics" },
    "material-basics": { ko: "Material 시스템 기초", en: "Material Basics" },
    "principled-bsdf": { ko: "Principled BSDF 이해", en: "Principled BSDF" },
    "shader-editor": { ko: "Shader Editor 이해", en: "Shader Editor" },
    "uv-unwrapping": { ko: "UV Unwrapping 이해", en: "UV Unwrapping" },
    "uv-editor": { ko: "UV Editor 조작", en: "UV Editor" },
    "light-types": { ko: "4가지 Light 종류", en: "The Four Light Types" },
    "hdri-lighting": { ko: "HDRI 환경 조명", en: "HDRI Lighting" },
    "three-point-light": { ko: "3점 조명법", en: "Three-Point Lighting" },
    "keyframe-basics": { ko: "키프레임 기초", en: "Keyframe Basics" },
    "graph-editor": { ko: "Graph Editor 이해", en: "Graph Editor" },
    "armature-basics": { ko: "Armature 이해", en: "Armature Basics" },
    "weight-paint": { ko: "Weight Paint 이해", en: "Weight Paint" },
    "render-settings": { ko: "Cycles vs EEVEE", en: "Cycles vs EEVEE" },
    "compositing-basics": { ko: "컴포지팅 기초", en: "Compositing Basics" },
    "origin-vs-3dcursor": { ko: "Origin vs 3D Cursor", en: "Origin vs 3D Cursor" },
    "poly-circle": { ko: "다각형으로 원 만들기", en: "Making a Circle with Polygons" },
    "box-rounding": { ko: "박스 모서리 라운딩", en: "Rounding Box Corners" },
  };

  var LIBRARY_CATEGORY_LABELS = {
    "전체": { ko: "전체", en: "All" },
    "Edit Mode": { ko: "Edit Mode", en: "Edit Mode" },
    "Generate Modifiers": { ko: "Generate Modifiers", en: "Generate Modifiers" },
    "Normals": { ko: "Normals", en: "Normals" },
    "Sculpting": { ko: "Sculpting", en: "Sculpting" },
    "Material": { ko: "Material", en: "Material" },
    "UV": { ko: "UV", en: "UV" },
    "Lighting": { ko: "Lighting", en: "Lighting" },
    "Animation": { ko: "Animation", en: "Animation" },
    "Rigging": { ko: "Rigging", en: "Rigging" },
    "Rendering": { ko: "Rendering", en: "Rendering" },
    "기타": { ko: "기타", en: "Misc" },
  };

  var SHORTCUT_CATEGORY_LABELS = {
    general: { ko: "일반", en: "General" },
    navigation: { ko: "화면 조작", en: "Navigation" },
    transform: { ko: "기본 변형", en: "Transforms" },
    modeling: { ko: "모델링", en: "Modeling" },
    modifier: { ko: "Modifier", en: "Modifier" },
    object: { ko: "오브젝트", en: "Object" },
    sculpt: { ko: "Sculpt", en: "Sculpt" },
    material: { ko: "재질", en: "Material" },
    uv: { ko: "UV", en: "UV" },
    rigging: { ko: "리깅", en: "Rigging" },
    render: { ko: "렌더링", en: "Rendering" },
  };

  var WEEK_TRANSLATIONS = {
    1: {
      title: { ko: "수업 시작 준비", en: "Course Setup" },
      subtitle: { ko: "오리엔테이션 · Blender 설치 · 컨셉 설정", en: "Orientation · Install Blender · Set a Concept" },
      topics: {
        ko: ["수업 소개 및 방향", "Blender 설치 및 실행 확인", "Mixboard 디자인 컨셉 설정"],
        en: ["Course overview and direction", "Install and launch Blender", "Set a design concept with Mixboard"],
      },
      assignmentTitle: { ko: "Blender 설치 확인 스크린샷", en: "Blender Launch Screenshot" },
      steps: [
        { title: { ko: "Blender 설치", en: "Install Blender" } },
        { title: { ko: "컨셉 설정 (Mixboard)", en: "Set a Concept (Mixboard)" } },
      ],
    },
    2: {
      title: { ko: "Blender 인터페이스 · 기초", en: "Blender Interface and Basics" },
      subtitle: { ko: "화면 조작 · 오브젝트 변형 · 첫 모델링", en: "Viewport Navigation · Object Transforms · First Modeling" },
      topics: {
        ko: ["Blender 인터페이스 구조", "화면 조작 (Orbit/Pan/Zoom)", "오브젝트 기본 변형 (G/R/S)", "Extrude / Inset / Loop Cut / Bevel"],
        en: ["Blender interface layout", "Viewport navigation (Orbit/Pan/Zoom)", "Basic object transforms (G/R/S)", "Extrude / Inset / Loop Cut / Bevel"],
      },
      assignmentTitle: { ko: "간단한 로우폴리 소품 만들기", en: "Create a Simple Low-Poly Prop" },
      steps: [
        { title: { ko: "프리퍼런스 세팅", en: "Preferences Setup" } },
        { title: { ko: "화면 조작", en: "Viewport Navigation" } },
        { title: { ko: "기본 변형 (G/R/S)", en: "Basic Transforms (G/R/S)" } },
        { title: { ko: "Edit Mode 모델링", en: "Edit Mode Modeling" } },
        { title: { ko: "Bevel 마무리", en: "Finishing with Bevel" } },
        { title: { ko: "뷰포트 셰이딩", en: "Viewport Shading" } },
      ],
    },
    3: {
      title: { ko: "기초 모델링 1 — Edit + Modifier", en: "Basic Modeling 1 - Edit + Modifier" },
      subtitle: { ko: "기본형 · 대칭 · 곡면 · 반복", en: "Base Forms · Symmetry · Surfaces · Repetition" },
      topics: {
        ko: ["Reference Image로 작업 준비", "Edit Mode: Extrude / Loop Cut / Inset / Bevel", "Mirror", "Subdivision Surface", "Solidify", "Array", "Boolean", "Bevel Modifier + Weighted Normal", "Modifier Stack 순서와 Apply"],
        en: ["Prepare with reference images", "Edit Mode: Extrude / Loop Cut / Inset / Bevel", "Mirror", "Subdivision Surface", "Solidify", "Array", "Boolean", "Bevel Modifier + Weighted Normal", "Modifier stack order and Apply"],
      },
      assignmentTitle: { ko: "Edit + Modifier 로봇", en: "Edit + Modifier Robot" },
      steps: [
        { title: { ko: "레퍼런스 이미지 설정", en: "Reference Image Setup" } },
        { title: { ko: "기본형 만들기", en: "Create the Base Form" } },
        { title: { ko: "Mirror", en: "Mirror" } },
        { title: { ko: "Subdivision Surface", en: "Subdivision Surface" } },
        { title: { ko: "Solidify", en: "Solidify" } },
        { title: { ko: "Array", en: "Array" } },
        { title: { ko: "Boolean", en: "Boolean" } },
        { title: { ko: "Bevel Modifier", en: "Bevel Modifier" } },
        { title: { ko: "Weighted Normal", en: "Weighted Normal" } },
        { title: { ko: "Modifier Stack 정리", en: "Organize the Modifier Stack" } },
        { title: { ko: "Collection", en: "Collection" } },
        { title: { ko: "Reference Image 실습", en: "Reference Image Practice" } },
      ],
    },
    4: {
      title: { ko: "기초 모델링 2 — 디테일 & 정리", en: "Basic Modeling 2 - Details and Cleanup" },
      subtitle: { ko: "Bevel · Weighted Normal · Apply", en: "Bevel · Weighted Normal · Apply" },
      topics: {
        ko: ["Inset / Boolean 디테일", "Bevel Tool vs Bevel Modifier", "Weighted Normal", "Join / Separate", "Apply Transform vs Modifier Apply"],
        en: ["Inset / Boolean details", "Bevel Tool vs Bevel Modifier", "Weighted Normal", "Join / Separate", "Apply Transform vs Modifier Apply"],
      },
      assignmentTitle: { ko: "로봇 디테일 정리", en: "Refine Robot Details" },
      steps: [
        { title: { ko: "Transform 정리와 파츠 관리", en: "Organize Transforms and Parts" } },
        { title: { ko: "얼굴과 패널 디테일", en: "Face and Panel Details" } },
        { title: { ko: "Bevel 두 가지 비교", en: "Two Ways to Use Bevel" } },
        { title: { ko: "Weighted Normal과 음영 정리", en: "Weighted Normal and Shading Cleanup" } },
        { title: { ko: "Apply 시점과 최종 점검", en: "When to Apply and Final Check" } },
      ],
    },
    5: {
      title: { ko: "AI 3D 생성 + Sculpting", en: "AI 3D Generation + Sculpting" },
      subtitle: { ko: "AI 툴 활용 · Sculpt Mode 기초 · 메쉬 정리", en: "AI Tools · Sculpt Mode Basics · Mesh Cleanup" },
      topics: {
        ko: ["AI 3D 생성 툴 (Meshy/Tripo)", "AI 메쉬 Import 및 정리", "Sculpt Mode 기초 브러시", "Sculpt 브러시 심화 (Clay/Crease/Inflate)", "Remesh와 Dyntopo", "AI + Sculpt 하이브리드 워크플로우"],
        en: ["AI 3D generation tools (Meshy/Tripo)", "Importing and cleaning AI meshes", "Core Sculpt Mode brushes", "Advanced sculpt brushes (Clay/Crease/Inflate)", "Remesh and Dyntopo", "AI + sculpt hybrid workflow"],
      },
      assignmentTitle: { ko: "AI + 수동 하이브리드 오브젝트", en: "AI + Manual Hybrid Object" },
      steps: [
        { title: { ko: "AI 3D 생성 체험", en: "Try AI 3D Generation" } },
        { title: { ko: "AI 메쉬 정리", en: "Clean Up an AI Mesh" } },
        { title: { ko: "Sculpt Mode 기초", en: "Sculpt Mode Basics" } },
        { title: { ko: "Sculpt 브러시 심화", en: "Advanced Sculpt Brushes" } },
        { title: { ko: "Remesh와 마무리", en: "Remesh and Final Cleanup" } },
      ],
    },
    6: {
      title: { ko: "Material & Shader Node", en: "Material and Shader Nodes" },
      subtitle: { ko: "재질 시스템 · Principled BSDF · 노드 편집", en: "Material System · Principled BSDF · Node Editing" },
      topics: {
        ko: ["Material 슬롯 구조", "Principled BSDF 핵심 파라미터", "Shader Node Editor 기초", "Color Ramp / Texture 노드", "파츠별 Material 분리", "Viewport Shading 모드"],
        en: ["Material slot structure", "Key Principled BSDF parameters", "Shader Node Editor basics", "Color Ramp / Texture nodes", "Separate materials by part", "Viewport shading modes"],
      },
      assignmentTitle: { ko: "재질 스타일 샘플러", en: "Material Style Sampler" },
      steps: [
        { title: { ko: "Material 할당", en: "Material Assignment" } },
        { title: { ko: "Principled BSDF 탐색", en: "Explore Principled BSDF" } },
        { title: { ko: "Shader Node Editor", en: "Shader Node Editor" } },
        { title: { ko: "Texture 노드로 질감 추가", en: "Add Texture with Texture Nodes" } },
        { title: { ko: "Viewport Shading 비교", en: "Compare Viewport Shading Modes" } },
      ],
    },
    7: {
      title: { ko: "UV Unwrapping + AI Texture", en: "UV Unwrapping + AI Textures" },
      subtitle: { ko: "UV 펼치기 · 텍스처 매핑 · AI 이미지 활용", en: "UV Layout · Texture Mapping · AI Images" },
      topics: {
        ko: ["UV 개념과 필요성", "Seam 설정 전략", "Unwrap + UV Editor", "UV 섬 정리와 배치", "AI Texture 생성 및 적용", "Texture Painting 맛보기"],
        en: ["Why UVs matter", "Seam placement strategies", "Unwrap + UV Editor", "Organize and pack UV islands", "Generate and apply AI textures", "Intro to texture painting"],
      },
      assignmentTitle: { ko: "텍스처 입힌 소품", en: "Textured Prop" },
      steps: [
        { title: { ko: "UV 개념 이해", en: "Understand UVs" } },
        { title: { ko: "Unwrap & UV Editor", en: "Unwrap and Use the UV Editor" } },
        { title: { ko: "Smart UV Project로 빠른 펼침", en: "Fast Unwrapping with Smart UV Project" } },
        { title: { ko: "AI Texture 생성 및 적용", en: "Generate and Apply an AI Texture" } },
        { title: { ko: "Texture Painting 맛보기", en: "Intro to Texture Painting" } },
      ],
    },
    8: {
      title: { ko: "⭐ 중간고사 — 중간 프로젝트 발표", en: "Midterm Project Presentation" },
      subtitle: { ko: "지금까지 배운 것을 담은 작품 발표", en: "Present a project that brings together what you've learned so far" },
      topics: {
        ko: ["3D 모델 완성", "Material/Texture 적용", "발표 준비"],
        en: ["Finalize the 3D model", "Apply materials and textures", "Prepare the presentation"],
      },
      assignmentTitle: { ko: "중간 프로젝트 발표", en: "Midterm Project Presentation" },
      steps: [
        { title: { ko: "프로젝트 마무리", en: "Finish the Project" } },
      ],
    },
    9: {
      title: { ko: "Lighting 기초 + 조명 연출", en: "Lighting Basics + Scene Lighting" },
      subtitle: { ko: "빛의 종류 · HDRI · 3점 조명 · 카메라", en: "Light Types · HDRI · Three-Point Lighting · Camera" },
      topics: {
        ko: ["Light 오브젝트 4종류", "HDRI 환경 조명", "3점 조명법", "카메라 세팅", "조명 색온도와 분위기", "배경 설정"],
        en: ["The four light object types", "HDRI environment lighting", "Three-point lighting", "Camera setup", "Color temperature and mood", "Background setup"],
      },
      assignmentTitle: { ko: "조명 포트폴리오", en: "Lighting Portfolio" },
      steps: [
        { title: { ko: "Light 종류 탐색", en: "Explore Light Types" } },
        { title: { ko: "HDRI 환경 조명", en: "HDRI Environment Lighting" } },
        { title: { ko: "3점 조명 세팅", en: "Three-Point Lighting Setup" } },
        { title: { ko: "카메라 세팅", en: "Camera Setup" } },
        { title: { ko: "분위기 연출 실험", en: "Mood Lighting Experiments" } },
      ],
    },
    10: {
      title: { ko: "Animation 기초", en: "Animation Basics" },
      subtitle: { ko: "키프레임 · Dope Sheet · Graph Editor · 루프", en: "Keyframes · Dope Sheet · Graph Editor · Loops" },
      topics: {
        ko: ["키프레임 삽입과 삭제", "Location / Rotation / Scale 애니메이션", "Dope Sheet 타이밍 편집", "Graph Editor 커브 조절", "자동 키프레임 모드", "루프 애니메이션"],
        en: ["Insert and delete keyframes", "Location / Rotation / Scale animation", "Timing edits in the Dope Sheet", "Curves in the Graph Editor", "Auto keying mode", "Loop animation"],
      },
      assignmentTitle: { ko: "간단한 움직임 애니메이션", en: "Simple Motion Animation" },
      steps: [
        { title: { ko: "키프레임 기초", en: "Keyframe Basics" } },
        { title: { ko: "회전·크기 애니메이션", en: "Rotation and Scale Animation" } },
        { title: { ko: "Dope Sheet 타이밍", en: "Timing in the Dope Sheet" } },
        { title: { ko: "Graph Editor 커브", en: "Curves in the Graph Editor" } },
        { title: { ko: "루프 애니메이션", en: "Loop Animation" } },
      ],
    },
    11: {
      title: { ko: "Rigging 기초", en: "Rigging Basics" },
      subtitle: { ko: "Armature · 본 구조 · 웨이트 페인팅 · 포즈", en: "Armature · Bone Structure · Weight Paint · Posing" },
      topics: {
        ko: ["Armature 추가와 구조", "Bone 편집 (Extrude/Subdivide)", "Mesh Parenting (Automatic Weights)", "Pose Mode로 포즈 잡기", "Weight Paint 기초 수정", "Bone Constraint 맛보기"],
        en: ["Armatures and bone structure", "Bone editing (Extrude/Subdivide)", "Mesh parenting (Automatic Weights)", "Posing in Pose Mode", "Basic weight painting fixes", "Intro to bone constraints"],
      },
      assignmentTitle: { ko: "기본 캐릭터 리깅", en: "Basic Character Rig" },
      steps: [
        { title: { ko: "Armature 추가와 본 만들기", en: "Add an Armature and Build Bones" } },
        { title: { ko: "메쉬와 연결 (Skinning)", en: "Connect the Mesh (Skinning)" } },
        { title: { ko: "Pose Mode로 포즈 잡기", en: "Pose in Pose Mode" } },
        { title: { ko: "Weight Paint 수정", en: "Refine Weights with Weight Paint" } },
      ],
    },
    12: {
      title: { ko: "AI 활용 리깅 (Mixamo)", en: "AI-Assisted Rigging (Mixamo)" },
      subtitle: { ko: "Mixamo 자동 리깅 · FBX 워크플로우 · NLA", en: "Mixamo Auto-Rigging · FBX Workflow · NLA" },
      topics: {
        ko: ["Blender → FBX 익스포트 준비", "Mixamo 업로드 및 자동 리깅", "애니메이션 선택 및 다운로드", "Blender FBX 임포트", "NLA Editor로 애니메이션 관리", "수동 리깅 vs AI 리깅 비교"],
        en: ["Prepare Blender for FBX export", "Upload to Mixamo and auto-rig", "Choose and download animations", "Import FBX back into Blender", "Manage animations in the NLA Editor", "Manual rigging vs AI rigging"],
      },
      assignmentTitle: { ko: "AI 리깅 캐릭터 애니메이션", en: "AI-Rigged Character Animation" },
      steps: [
        { title: { ko: "익스포트 준비", en: "Prepare for Export" } },
        { title: { ko: "Mixamo 자동 리깅", en: "Auto-Rig with Mixamo" } },
        { title: { ko: "애니메이션 선택 및 임포트", en: "Choose and Import an Animation" } },
        { title: { ko: "NLA Editor로 애니메이션 관리", en: "Manage Animations in the NLA Editor" } },
      ],
    },
    13: {
      title: { ko: "렌더링 + AI 후처리", en: "Rendering + AI Post-Processing" },
      subtitle: { ko: "Cycles vs EEVEE · 출력 설정 · Compositing · AI 후처리", en: "Cycles vs EEVEE · Output Settings · Compositing · AI Post-Processing" },
      topics: {
        ko: ["Cycles vs EEVEE 비교", "렌더 샘플링과 노이즈", "Output 해상도와 파일 형식", "Compositing 노드 기초", "애니메이션 렌더링", "AI 후처리 체험"],
        en: ["Cycles vs EEVEE", "Render sampling and noise", "Output resolution and file format", "Compositing node basics", "Animation rendering", "Try AI post-processing"],
      },
      assignmentTitle: { ko: "렌더링 포트폴리오", en: "Rendering Portfolio" },
      steps: [
        { title: { ko: "렌더 엔진 비교", en: "Compare Render Engines" } },
        { title: { ko: "렌더 출력 설정", en: "Render Output Settings" } },
        { title: { ko: "Compositing 기초", en: "Compositing Basics" } },
        { title: { ko: "애니메이션 렌더링", en: "Animation Rendering" } },
        { title: { ko: "AI 후처리 체험", en: "Try AI Post-Processing" } },
      ],
    },
    14: {
      title: { ko: "최종 프로젝트 제작", en: "Final Project Production" },
      subtitle: { ko: "개인 프로젝트 집중 작업", en: "Focused Work on Your Individual Project" },
      topics: {
        ko: ["자유 주제 3D 작품 완성", "교수 피드백 반영", "렌더링 마무리"],
        en: ["Complete a self-directed 3D project", "Apply instructor feedback", "Finalize rendering"],
      },
      assignmentTitle: { ko: "최종 프로젝트 사전 제출", en: "Final Project Pre-Submission" },
      steps: [
        { title: { ko: "프로젝트 마무리", en: "Finalize the Project" } },
      ],
    },
    15: {
      title: { ko: "⭐ 기말고사 — 최종 프로젝트 발표", en: "Final Project Presentation" },
      subtitle: { ko: "학기 전체 결과물 발표", en: "Present the work you've built across the semester" },
      topics: {
        ko: ["최종 발표 (5분)", "작품 설명", "배운 점 공유"],
        en: ["Final presentation (5 minutes)", "Explain your work", "Share what you learned"],
      },
      assignmentTitle: { ko: "기말 발표", en: "Final Presentation" },
      steps: [
        { title: { ko: "발표 준비", en: "Prepare the Presentation" } },
      ],
    },
  };

  function normalizeLang(lang) {
    if (!lang) return null;
    var value = String(lang).toLowerCase();
    return SUPPORTED_LANGS.indexOf(value) !== -1 ? value : null;
  }

  function getStoredLang() {
    try {
      return normalizeLang(win.localStorage.getItem(STORAGE_KEY));
    } catch (e) {
      return null;
    }
  }

  function detectLang() {
    var stored = getStoredLang();
    if (stored) return stored;
    return "ko";
  }

  var currentLang = detectLang();

  function applyDocumentLang(lang) {
    if (!win.document || !win.document.documentElement) return;
    win.document.documentElement.lang = lang;
    win.document.documentElement.setAttribute("data-lang", lang);
  }

  function localizeValue(value, lang) {
    if (value == null) return value;
    if (value && typeof value === "object" && !Array.isArray(value)) {
      if (Object.prototype.hasOwnProperty.call(value, "ko") || Object.prototype.hasOwnProperty.call(value, "en")) {
        return value[lang] || value.ko || value.en || "";
      }
    }
    return value;
  }

  function getStrings(page) {
    var lang = currentLang;
    var common = COPY.common[lang] || {};
    var pageCopy = COPY[page] ? (COPY[page][lang] || {}) : {};
    return Object.assign({}, common, pageCopy);
  }

  function getShowMeLabel(id, fallbackMeta) {
    var localized = SHOWME_LABELS[id];
    if (localized) return localizeValue(localized, currentLang);
    return fallbackMeta && fallbackMeta.label ? fallbackMeta.label : id;
  }

  function getLibraryCategoryLabel(name) {
    return LIBRARY_CATEGORY_LABELS[name] ? localizeValue(LIBRARY_CATEGORY_LABELS[name], currentLang) : name;
  }

  function getShortcutCategoryLabel(key, fallback) {
    return SHORTCUT_CATEGORY_LABELS[key] ? localizeValue(SHORTCUT_CATEGORY_LABELS[key], currentLang) : (fallback || key);
  }

  var HANGUL_RE = /[가-힣]/;
  var SHOWME_ATTRS = ["aria-label", "title", "placeholder", "alt"];
  var COURSE_FRAGMENT_MAP = {
    "Blender 공식 사이트": "the official Blender site",
    "화면 조작": "viewport navigation",
    "기본 모델링 도구": "basic modeling tools",
    "기본 모델링": "basic modeling",
    "기본형": "base form",
    "과제": "assignment",
    "공식 사이트": "official site",
    "공식 문서": "official documentation",
    "설치 파일": "installer",
    "버전 번호": "version number",
    "실행": "launch",
    "정상 실행": "successful launch",
    "스크린샷": "screenshot",
    "레퍼런스 이미지": "reference images",
    "레퍼런스": "reference",
    "이미지": "image",
    "정면": "front",
    "측면": "side",
    "후면": "back",
    "보드": "board",
    "캡처": "capture",
    "저장": "save",
    "비율": "proportions",
    "구조": "structure",
    "작업": "work",
    "실습": "practice",
    "연습": "practice",
    "확인": "check",
    "정리": "cleanup",
    "추가": "add",
    "적용": "apply",
    "세팅": "setup",
    "설정": "setup",
    "탐색": "explore",
    "비교": "compare",
    "만들기": "create",
    "제출": "submit",
    "열기": "open",
    "열어보기": "open it",
    "켜기": "turn on",
    "끄기": "turn off",
    "불러오기": "import",
    "임포트": "import",
    "익스포트": "export",
    "연결": "connect",
    "전환": "switch",
    "수정": "adjust",
    "배치": "place",
    "탑색": "explore",
    "진입": "enter",
    "복귀": "return",
    "마무리": "finish",
    "준비": "prepare",
    "발표": "presentation",
    "비교 이미지": "comparison renders",
    "결과물": "result",
    "포즈": "pose",
    "조명": "lighting",
    "렌더": "render",
    "재질": "material",
    "질감": "texture",
    "오브젝트": "object",
    "메쉬": "mesh",
    "버텍스": "vertex",
    "정점": "vertex",
    "다듬기": "refinement"
  };
  var COURSE_PATTERNS = [
    {
      pattern: /^(.+)에서 (.+) 다운로드$/,
      format: function(match, source, subject) {
        return "Download " + translateCourseFragment(subject) + " from " + translateCourseFragment(source);
      }
    },
    {
      pattern: /^(.+) 후 (.+) 확인$/,
      format: function(match, action, subject) {
        return "After " + translateCourseFragment(action) + ", check " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s(\d+)개 이상 수집$/,
      format: function(match, subject, count) {
        return "Collect at least " + count + " " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s직접 열어보기$/,
      format: function(match, subject) {
        return "Open " + translateCourseFragment(subject) + " yourself";
      }
    },
    {
      pattern: /^(.+)\s켜기$/,
      format: function(match, subject) {
        return "Turn on " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s끄기$/,
      format: function(match, subject) {
        return "Turn off " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s확인$/,
      format: function(match, subject) {
        return "Check " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s연습$/,
      format: function(match, subject) {
        return "Practice " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+?)\s*포함된 스크린샷 제출$/,
      format: function(match, subject) {
        return "Submit a screenshot that includes " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s비교$/,
      format: function(match, subject) {
        return "Compare " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s제출$/,
      format: function(match, subject) {
        return "Submit " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s가이드$/,
      format: function(match, subject) {
        return translateCourseFragment(subject) + " Guide";
      }
    },
    {
      pattern: /^(.+)\s정리$/,
      format: function(match, subject) {
        return "Clean up " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s탐색$/,
      format: function(match, subject) {
        return "Explore " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s세팅$/,
      format: function(match, subject) {
        return "Set up " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s설정$/,
      format: function(match, subject) {
        return "Set up " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s추가$/,
      format: function(match, subject) {
        return "Add " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s적용$/,
      format: function(match, subject) {
        return "Apply " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s만들기$/,
      format: function(match, subject) {
        return "Create " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s전환$/,
      format: function(match, subject) {
        return "Switch " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s사용$/,
      format: function(match, subject) {
        return "Use " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s파악$/,
      format: function(match, subject) {
        return "Identify " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s수정$/,
      format: function(match, subject) {
        return "Adjust " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s배치$/,
      format: function(match, subject) {
        return "Place " + translateCourseFragment(subject);
      }
    },
    {
      pattern: /^(.+)\s보이는지 확인$/,
      format: function(match, subject) {
        return "Check whether " + translateCourseFragment(subject) + " is visible";
      }
    },
    {
      pattern: /^(.+)\s완료$/,
      format: function(match, subject) {
        return "Complete " + translateCourseFragment(subject);
      }
    }
  ];

  function getContentStore() {
    return win.RPD_I18N_CONTENT || {};
  }

  function getCurriculumExactMap() {
    var content = getContentStore();
    return content.curriculum && content.curriculum.exact ? content.curriculum.exact : {};
  }

  function getBlenderGlossary() {
    var content = getContentStore();
    return content.blenderGlossary || {};
  }

  function getShowMeStore() {
    var content = getContentStore();
    return content.showme || {};
  }

  function containsHangul(value) {
    return typeof value === "string" && HANGUL_RE.test(value);
  }

  function normalizeTranslatableText(value) {
    return typeof value === "string"
      ? value.replace(/\s+/g, " ").trim()
      : value;
  }

  function preserveEdgeWhitespace(source, translated) {
    var leading = (source.match(/^\s*/) || [""])[0];
    var trailing = (source.match(/\s*$/) || [""])[0];
    return leading + translated + trailing;
  }

  var reverseExactCache = typeof WeakMap === "function" ? new WeakMap() : null;

  function getReverseExactMap(map) {
    if (!map || typeof map !== "object") return {};
    if (reverseExactCache && reverseExactCache.has(map)) {
      return reverseExactCache.get(map);
    }

    var reverse = {};
    Object.keys(map).forEach(function(key) {
      var translated = map[key];
      if (typeof translated !== "string" || !translated || reverse[translated]) return;
      reverse[translated] = key;
    });

    if (reverseExactCache) reverseExactCache.set(map, reverse);
    return reverse;
  }

  function getExactTranslation(map, value) {
    if (!map || typeof map !== "object" || typeof value !== "string" || !value) return "";
    if (Object.prototype.hasOwnProperty.call(map, value)) return map[value];
    var normalized = normalizeTranslatableText(value);
    if (normalized && normalized !== value && Object.prototype.hasOwnProperty.call(map, normalized)) {
      return map[normalized];
    }
    return "";
  }

  function getReverseExactTranslation(map, value) {
    if (typeof value !== "string" || !value) return "";
    var reverse = getReverseExactMap(map);
    if (Object.prototype.hasOwnProperty.call(reverse, value)) return reverse[value];
    var normalized = normalizeTranslatableText(value);
    if (normalized && normalized !== value && Object.prototype.hasOwnProperty.call(reverse, normalized)) {
      return reverse[normalized];
    }
    return "";
  }

  function getShowMeExactMaps(widgetId) {
    var showme = getShowMeStore();
    return {
      common: showme.common && showme.common.exact ? showme.common.exact : {},
      widget: showme.widgets && showme.widgets[widgetId] && showme.widgets[widgetId].exact
        ? showme.widgets[widgetId].exact
        : {}
    };
  }

  function getShowMeExactTranslation(widgetId, value) {
    var maps = getShowMeExactMaps(widgetId);
    return getExactTranslation(maps.widget, value) || getExactTranslation(maps.common, value);
  }

  function getShowMeReverseExactTranslation(widgetId, value) {
    var maps = getShowMeExactMaps(widgetId);
    return getReverseExactTranslation(maps.widget, value) || getReverseExactTranslation(maps.common, value);
  }

  function translateShowMeStaticSnippet(value, widgetId) {
    return getShowMeExactTranslation(widgetId, value) || translateCourseText(value) || value;
  }

  function translateShowMeStaticSnippetToKo(value, widgetId) {
    return getShowMeReverseExactTranslation(widgetId, value)
      || getReverseExactTranslation(getCurriculumExactMap(), value)
      || value;
  }

  function translateShowMeSentenceGroup(value, widgetId) {
    var parts = typeof value === "string" ? value.match(/[^.?!]+[.?!]?/g) : null;
    if (!parts || !parts.length) return translateShowMeStaticSnippet(value, widgetId);
    return parts.map(function(part) {
      var trimmed = normalizeTranslatableText(part);
      if (!trimmed) return "";
      return translateShowMeStaticSnippet(trimmed, widgetId);
    }).filter(Boolean).join(" ");
  }

  function translateShowMeSentenceGroupToKo(value, widgetId) {
    var parts = typeof value === "string" ? value.match(/[^.?!]+[.?!]?/g) : null;
    if (!parts || !parts.length) return translateShowMeStaticSnippetToKo(value, widgetId);
    return parts.map(function(part) {
      var trimmed = normalizeTranslatableText(part);
      if (!trimmed) return "";
      return translateShowMeStaticSnippetToKo(trimmed, widgetId);
    }).filter(Boolean).join(" ");
  }

  function applyOrderedMap(value, map) {
    var result = value;
    Object.keys(map || {})
      .sort(function(a, b) { return b.length - a.length; })
      .forEach(function(key) {
        if (!key) return;
        result = result.split(key).join(map[key]);
      });
    return result;
  }

  function cleanupTranslatedText(value) {
    return String(value || "")
      .replace(/\s+([,.!?;:])/g, "$1")
      .replace(/\(\s+/g, "(")
      .replace(/\s+\)/g, ")")
      .replace(/\s{2,}/g, " ")
      .replace(/\s*→\s*/g, " -> ")
      .trim();
  }

  function translateCourseFragment(value) {
    if (typeof value !== "string" || !value) return value;
    if (!containsHangul(value)) return value;

    var exact = getExactTranslation(getCurriculumExactMap(), value);
    if (exact) return exact;

    var result = value;
    result = applyOrderedMap(result, getBlenderGlossary());
    result = applyOrderedMap(result, COURSE_FRAGMENT_MAP);
    return cleanupTranslatedText(result);
  }

  function translateCourseText(value) {
    if (currentLang !== "en" || typeof value !== "string" || !value) return value;
    if (!containsHangul(value)) return value;

    var exact = getExactTranslation(getCurriculumExactMap(), value);
    if (exact) return exact;

    value = normalizeTranslatableText(value);

    for (var i = 0; i < COURSE_PATTERNS.length; i += 1) {
      var rule = COURSE_PATTERNS[i];
      if (rule.pattern.test(value)) {
        return cleanupTranslatedText(value.replace(rule.pattern, rule.format));
      }
    }

    return cleanupTranslatedText(translateCourseFragment(value));
  }

  function localizeCourseList(list) {
    return Array.isArray(list) ? list.map(translateCourseText) : list;
  }

  function localizeCourseTask(task) {
    if (!task || currentLang !== "en") return task;
    return Object.assign({}, task, {
      label: translateCourseText(task.label),
      detail: translateCourseText(task.detail)
    });
  }

  function localizeWeekData(week) {
    if (!week || currentLang === "ko") return week;
    var tr = WEEK_TRANSLATIONS[week.week] || {};
    var localized = Object.assign({}, week);

    localized.title = localizeValue(tr.title, currentLang) || translateCourseText(week.title);
    localized.subtitle = localizeValue(tr.subtitle, currentLang) || translateCourseText(week.subtitle);
    localized.summary = translateCourseText(week.summary);
    localized.topics = tr.topics ? localizeValue(tr.topics, currentLang) : localizeCourseList(week.topics);
    localized.mistakes = localizeCourseList(week.mistakes);

    if (week.assignment) {
      localized.assignment = Object.assign({}, week.assignment, {
        title: localizeValue(tr.assignmentTitle, currentLang) || translateCourseText(week.assignment.title),
        description: translateCourseText(week.assignment.description),
        checklist: localizeCourseList(week.assignment.checklist)
      });
    }

    localized.shortcuts = Array.isArray(week.shortcuts) ? week.shortcuts.map(function(item) {
      return Object.assign({}, item, {
        action: translateCourseText(item.action)
      });
    }) : week.shortcuts;

    localized.docs = Array.isArray(week.docs) ? week.docs.map(function(item) {
      return Object.assign({}, item, {
        title: translateCourseText(item.title)
      });
    }) : week.docs;

    localized.videos = Array.isArray(week.videos) ? week.videos.map(function(item) {
      return Object.assign({}, item, {
        title: translateCourseText(item.title)
      });
    }) : week.videos;

    localized.steps = Array.isArray(week.steps) ? week.steps.map(function(step, index) {
      var stepTr = tr.steps && tr.steps[index];
      var localizedStep = Object.assign({}, step);
      localizedStep.title = stepTr ? (localizeValue(stepTr.title, currentLang) || translateCourseText(step.title)) : translateCourseText(step.title);
      localizedStep.copy = translateCourseText(step.copy);
      localizedStep.goal = localizeCourseList(step.goal);
      localizedStep.done = localizeCourseList(step.done);
      localizedStep.tasks = Array.isArray(step.tasks) ? step.tasks.map(localizeCourseTask) : step.tasks;
      localizedStep.clips = Array.isArray(step.clips) ? step.clips.map(function(clip) {
        return Object.assign({}, clip, { label: translateCourseText(clip.label) });
      }) : step.clips;
      return localizedStep;
    }) : week.steps;

    return localized;
  }

  function translateShowMeDynamicText(value, widgetId) {
    var match;

    if (value === "완벽합니다!") return "Perfect!";
    if (value === "조금 더 연습하면 완벽해질 거예요!") return "A little more practice and you'll nail it.";
    if (value === "interaction — 버텍스를 직접 드래그해보세요" || value === "직접 해보기 — 버텍스를 직접 드래그해보세요") {
      return "Try It - drag the vertex handles yourself";
    }
    if (value === "파란 점을 드래그하면 초록색 미러가 실시간으로 반영됩니다.") return "Drag the blue points to update the green mirrored side in real time.";
    if (value === "파란 점 드래그 → 초록 미러 실시간 반영 | Clipping 끄면 중심선을 넘길 수 있어요") return "Drag the blue points -> the green mirror updates in real time | Turn Clipping off to cross the center line.";

    match = value.match(/^문제\s+(\d+)\s*\/\s*(\d+)\s*·\s*점수\s*(\d+)점$/);
    if (match) return "Question " + match[1] + " / " + match[2] + " · Score " + match[3];

    match = value.match(/^(\d+)\s*\/\s*(\d+)\s*정답$/);
    if (match) return match[1] + " / " + match[2] + " correct";

    match = value.match(/^Q(\d+)\.\s+(.+)$/);
    if (match) return "Q" + match[1] + ". " + translateCourseText(match[2]);

    match = value.match(/^📖\s*Blender 공식 문서\s*[—-]\s*(.+)$/);
    if (match) return "📖 Blender Official Manual - " + translateCourseText(match[1]);

    match = value.match(/^interaction\s*[—-]\s*(.+)$/i);
    if (match) return "Interactive Demo - " + translateShowMeSentenceGroup(match[1], widgetId);

    match = value.match(/^직접 체험[:：]\s*(.+)$/);
    if (match) return "Try it: " + translateShowMeSentenceGroup(match[1], widgetId);

    match = value.match(/^분할 수:\s*(\d+)$/);
    if (match) return "Segments: " + match[1];

    match = value.match(/^(\d+)각형$/);
    if (match) return match[1] + "-gon";

    match = value.match(/^(\d+)각형\s+\((\d+)개 꼭짓점\)$/);
    if (match) return match[1] + "-gon (" + match[2] + " vertices)";

    match = value.match(/^(\d+)각형\s+[—-]\s+([0-9.]+%)$/);
    if (match) return match[1] + "-gon - " + match[2];

    match = value.match(/^단면:\s*(\d+)각형$/);
    if (match) return "Cross-section: " + match[1] + "-gon";

    match = value.match(/^현재 Radius\s+([0-9.]+),\s*Resolution\s+(\d+)\s+설정입니다\.\s+(.+)$/);
    if (match) {
      return "Current settings: Radius " + match[1] + ", Resolution " + match[2] + ". "
        + translateShowMeSentenceGroup(match[3], widgetId);
    }

    match = value.match(/^(\d+)각형은 원 면적의\s+([0-9.]+%)를 커버합니다\.\s+(.+)$/);
    if (match) {
      return "A " + match[1] + "-gon covers " + match[2] + " of the true circle area. "
        + translateShowMeSentenceGroup(match[3], widgetId);
    }

    match = value.match(/^(.+?)(란|이란)\?$/);
    if (match) return "What is " + translateCourseText(match[1]) + "?";

    match = value.match(/^(.+?)가 필요할 때$/);
    if (match) return "When to Use " + translateCourseText(match[1]);

    match = value.match(/^(.+?)를 안 쓰는 경우$/);
    if (match) return "When Not to Use " + translateCourseText(match[1]);

    match = value.match(/^(.+?) 전후$/);
    if (match) return "Before and After " + translateCourseText(match[1]);

    match = value.match(/^(.+?) 핵심이에요$/);
    if (match) return translateCourseText(match[1]) + " matters";

    return value;
  }

  function translateShowMeDynamicTextToKo(value, widgetId) {
    var match;

    if (value === "Perfect!") return "완벽합니다!";
    if (value === "A little more practice and you'll nail it.") return "조금 더 연습하면 완벽해질 거예요!";
    if (value === "Try It - drag the vertex handles yourself") return "직접 해보기 — 버텍스를 직접 드래그해보세요";
    if (value.indexOf("Interactive Demo - ") === 0) {
      return "interaction — " + translateShowMeSentenceGroupToKo(value.slice("Interactive Demo - ".length), widgetId);
    }
    if (value === "Drag the blue points to update the green mirrored side in real time.") {
      return "파란 점을 드래그하면 초록색 미러가 실시간으로 반영됩니다.";
    }
    if (value === "Drag the blue points -> the green mirror updates in real time | Turn Clipping off to cross the center line.") {
      return "파란 점 드래그 → 초록 미러 실시간 반영 | Clipping 끄면 중심선을 넘길 수 있어요";
    }

    match = value.match(/^Question\s+(\d+)\s*\/\s*(\d+)\s*·\s*Score\s+(\d+)$/);
    if (match) return "문제 " + match[1] + " / " + match[2] + " · 점수 " + match[3] + "점";

    match = value.match(/^(\d+)\s*\/\s*(\d+)\s*correct$/);
    if (match) return match[1] + " / " + match[2] + " 정답";

    match = value.match(/^Try it:\s*(.+)$/i);
    if (match) return "직접 체험: " + translateShowMeSentenceGroupToKo(match[1], widgetId);

    match = value.match(/^Segments:\s*(\d+)$/);
    if (match) return "분할 수: " + match[1];

    match = value.match(/^(\d+)-gon$/);
    if (match) return match[1] + "각형";

    match = value.match(/^(\d+)-gon\s+\((\d+) vertices\)$/);
    if (match) return match[1] + "각형 (" + match[2] + "개 꼭짓점)";

    match = value.match(/^(\d+)-gon\s+-\s+([0-9.]+%)$/);
    if (match) return match[1] + "각형 — " + match[2];

    match = value.match(/^Cross-section:\s*(\d+)-gon$/);
    if (match) return "단면: " + match[1] + "각형";

    match = value.match(/^Current settings:\s+Radius\s+([0-9.]+),\s*Resolution\s+(\d+)\.\s+(.+)$/);
    if (match) {
      return "현재 Radius " + match[1] + ", Resolution " + match[2] + " 설정입니다. "
        + translateShowMeSentenceGroupToKo(match[3], widgetId);
    }

    match = value.match(/^A\s+(\d+)-gon covers\s+([0-9.]+%)\s+of the true circle area\.\s+(.+)$/);
    if (match) {
      return match[1] + "각형은 원 면적의 " + match[2] + "를 커버합니다. "
        + translateShowMeSentenceGroupToKo(match[3], widgetId);
    }

    return value;
  }

  function translateShowMeString(value, widgetId) {
    if (typeof value !== "string" || !value) return value;

    var trimmed = normalizeTranslatableText(value);
    if (!trimmed) return value;

    var translated = "";

    if (currentLang === "en") {
      translated = getShowMeExactTranslation(widgetId, trimmed);

      if (!translated) {
        translated = translateShowMeDynamicText(trimmed, widgetId);
      }

      if (translated === trimmed) {
        translated = translateCourseText(trimmed);
      }
    } else {
      translated = getShowMeReverseExactTranslation(widgetId, trimmed)
        || getReverseExactTranslation(getCurriculumExactMap(), trimmed);

      if (!translated) {
        translated = translateShowMeDynamicTextToKo(trimmed, widgetId);
      }
    }

    return preserveEdgeWhitespace(value, translated || trimmed);
  }

  var SHOWME_STRUCTURED_TAGS = {
    A: true,
    DIV: true,
    H1: true,
    H2: true,
    H3: true,
    H4: true,
    H5: true,
    H6: true,
    LABEL: true,
    LI: true,
    P: true,
    SUMMARY: true,
    TD: true,
    TH: true
  };

  var SHOWME_INLINE_ONLY_TAGS = {
    A: true,
    ABBR: true,
    B: true,
    BDI: true,
    BDO: true,
    BR: true,
    CITE: true,
    CODE: true,
    DATA: true,
    DFN: true,
    EM: true,
    I: true,
    KBD: true,
    MARK: true,
    Q: true,
    S: true,
    SAMP: true,
    SMALL: true,
    SPAN: true,
    STRONG: true,
    SUB: true,
    SUP: true,
    TIME: true,
    U: true,
    VAR: true,
    WBR: true
  };

  function canTranslateStructuredShowMeElement(el) {
    if (!el || el.nodeType !== 1 || !SHOWME_STRUCTURED_TAGS[el.nodeName]) return false;
    if (!el.textContent || !normalizeTranslatableText(el.textContent)) return false;

    var descendants = el.querySelectorAll("*");
    if (!descendants.length) return false;

    for (var i = 0; i < descendants.length; i += 1) {
      var name = descendants[i].nodeName.toUpperCase();
      if (!SHOWME_INLINE_ONLY_TAGS[name]) return false;
    }

    return true;
  }

  function localizeShowMeStructuredBlocks(root, widgetId) {
    var scope = root && root.nodeType === 9 ? root.body : root;
    if (!scope || !scope.querySelectorAll) return;

    scope.querySelectorAll("*").forEach(function(el) {
      if (!canTranslateStructuredShowMeElement(el)) return;
      var original = el.textContent;
      var translated = translateShowMeString(original, widgetId);
      if (translated !== original) el.textContent = translated;
    });
  }

  function localizeShowMeTextNodes(doc, widgetId) {
    if (!doc || !doc.body) return;
    var nodeFilter = doc.defaultView && doc.defaultView.NodeFilter ? doc.defaultView.NodeFilter : win.NodeFilter;
    var walker = doc.createTreeWalker(doc.body, nodeFilter.SHOW_TEXT, {
      acceptNode: function(node) {
        if (!node || !node.nodeValue || !node.nodeValue.trim()) return nodeFilter.FILTER_REJECT;
        var parent = node.parentNode;
        if (!parent || /^(SCRIPT|STYLE|NOSCRIPT)$/i.test(parent.nodeName)) return nodeFilter.FILTER_REJECT;
        return nodeFilter.FILTER_ACCEPT;
      }
    });

    var current;
    while ((current = walker.nextNode())) {
      var nextValue = translateShowMeString(current.nodeValue, widgetId);
      if (nextValue !== current.nodeValue) current.nodeValue = nextValue;
    }
  }

  function localizeShowMeAttributes(root, widgetId) {
    if (!root || root.nodeType !== 1) return;
    SHOWME_ATTRS.forEach(function(attr) {
      if (!root.hasAttribute(attr)) return;
      var original = root.getAttribute(attr);
      var localized = translateShowMeString(original, widgetId);
      if (localized !== original) root.setAttribute(attr, localized);
    });
    root.querySelectorAll(SHOWME_ATTRS.map(function(attr) { return "[" + attr + "]"; }).join(","))
      .forEach(function(el) {
        SHOWME_ATTRS.forEach(function(attr) {
          if (!el.hasAttribute(attr)) return;
          var original = el.getAttribute(attr);
          var localized = translateShowMeString(original, widgetId);
          if (localized !== original) el.setAttribute(attr, localized);
        });
      });
  }

  function applyShowMeLocalization(doc, widgetId) {
    if (!doc || !doc.body) return;
    if (typeof doc.title === "string") doc.title = translateShowMeString(doc.title, widgetId);
    localizeShowMeAttributes(doc.body, widgetId);
    localizeShowMeStructuredBlocks(doc, widgetId);
    localizeShowMeTextNodes(doc, widgetId);
  }

  function queueShowMeLocalization(doc, widgetId) {
    if (!doc || !doc.defaultView || typeof doc.defaultView.setTimeout !== "function") return;
    if (doc.__rpdShowMeQueuedTimer) {
      doc.defaultView.clearTimeout(doc.__rpdShowMeQueuedTimer);
    }
    doc.__rpdShowMeQueuedTimer = doc.defaultView.setTimeout(function() {
      doc.__rpdShowMeQueuedTimer = null;
      applyShowMeLocalization(doc, widgetId);
    }, 72);
  }

  function scheduleShowMeLocalization(doc, widgetId) {
    if (!doc || !doc.defaultView || typeof doc.defaultView.setTimeout !== "function") return;
    if (doc.__rpdShowMeTimers && doc.__rpdShowMeTimers.length) {
      doc.__rpdShowMeTimers.forEach(function(timerId) {
        doc.defaultView.clearTimeout(timerId);
      });
    }
    doc.__rpdShowMeTimers = [0, 48, 180, 480, 1200, 2400, 4200, 6400].map(function(delay) {
      return doc.defaultView.setTimeout(function() {
        applyShowMeLocalization(doc, widgetId);
      }, delay);
    });
  }

  function patchShowMeCanvasText(frameWin) {
    if (!frameWin || !frameWin.CanvasRenderingContext2D) return;
    var proto = frameWin.CanvasRenderingContext2D.prototype;
    if (proto.__rpdI18nPatched) return;
    ["fillText", "strokeText"].forEach(function(method) {
      var original = proto[method];
      if (typeof original !== "function") return;
      proto[method] = function(text) {
        var args = Array.prototype.slice.call(arguments);
        if (typeof args[0] === "string") {
          args[0] = translateShowMeString(args[0], frameWin.__rpdShowMeWidgetId);
        }
        return original.apply(this, args);
      };
    });
    proto.__rpdI18nPatched = true;
  }

  function observeShowMeDocument(doc, widgetId) {
    if (!doc || !doc.body || !doc.defaultView || typeof doc.defaultView.MutationObserver !== "function") return;
    if (doc.__rpdShowMeObserver) doc.__rpdShowMeObserver.disconnect();

    doc.__rpdShowMeObserver = new doc.defaultView.MutationObserver(function(mutations) {
      var shouldQueue = false;
      mutations.forEach(function(mutation) {
        if (mutation.type === "characterData" && mutation.target) {
          var nextValue = translateShowMeString(mutation.target.nodeValue, widgetId);
          if (nextValue !== mutation.target.nodeValue) mutation.target.nodeValue = nextValue;
          return;
        }

        if (mutation.type === "attributes" && mutation.target && mutation.attributeName) {
          var attrValue = mutation.target.getAttribute(mutation.attributeName);
          var translated = translateShowMeString(attrValue, widgetId);
          if (translated !== attrValue) mutation.target.setAttribute(mutation.attributeName, translated);
          return;
        }

        Array.prototype.forEach.call(mutation.addedNodes || [], function(node) {
          if (!node) return;
          if (node.nodeType === 3) {
            var textValue = translateShowMeString(node.nodeValue, widgetId);
            if (textValue !== node.nodeValue) node.nodeValue = textValue;
            shouldQueue = true;
            return;
          }
          if (node.nodeType === 1) {
            localizeShowMeAttributes(node, widgetId);
            localizeShowMeStructuredBlocks(node, widgetId);
            localizeShowMeTextNodes(doc, widgetId);
            shouldQueue = true;
          }
        });
      });

      if (shouldQueue) queueShowMeLocalization(doc, widgetId);
    });

    doc.__rpdShowMeObserver.observe(doc.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: SHOWME_ATTRS
    });
  }

  function localizeShowMeIframe(iframe, widgetId) {
    if (!iframe || !iframe.contentWindow || !iframe.contentDocument) return;
    var frameWin = iframe.contentWindow;
    var doc = iframe.contentDocument;
    frameWin.__rpdShowMeWidgetId = widgetId;
    doc.documentElement.lang = currentLang;
    doc.documentElement.setAttribute("data-lang", currentLang);
    patchShowMeCanvasText(frameWin);
    applyShowMeLocalization(doc, widgetId);
    observeShowMeDocument(doc, widgetId);
    scheduleShowMeLocalization(doc, widgetId);
  }

  function updateSwitcherState(root) {
    if (!root) return;
    var strings = getStrings();
    root.setAttribute("aria-label", strings.languageSwitcherAria || "Switch language");
    root.querySelectorAll("[data-lang-value]").forEach(function(btn) {
      var value = btn.getAttribute("data-lang-value");
      var active = value === currentLang;
      btn.classList.toggle("is-active", active);
      btn.setAttribute("aria-pressed", active ? "true" : "false");
      btn.title = value === "ko" ? "Korean" : "English";
    });
  }

  function mountLanguageSwitcher(target) {
    var el = typeof target === "string" ? win.document.querySelector(target) : target;
    if (!el) return null;

    el.textContent = "";
    var strings = getStrings();
    var wrap = win.document.createElement("div");
    wrap.className = "lang-switcher";
    wrap.setAttribute("role", "group");
    wrap.setAttribute("aria-label", strings.languageSwitcherAria || "Switch language");

    ["ko", "en"].forEach(function(code) {
      var button = win.document.createElement("button");
      button.type = "button";
      button.className = "lang-switcher-btn";
      button.setAttribute("data-lang-value", code);
      button.textContent = code === "ko" ? strings.langKo : strings.langEn;
      button.addEventListener("click", function() {
        setLanguage(code);
      });
      wrap.appendChild(button);
    });

    el.appendChild(wrap);
    updateSwitcherState(wrap);
    return wrap;
  }

  function setLanguage(nextLang) {
    var normalized = normalizeLang(nextLang);
    if (!normalized || normalized === currentLang) return currentLang;
    currentLang = normalized;
    try {
      win.localStorage.setItem(STORAGE_KEY, normalized);
    } catch (e) {}
    applyDocumentLang(normalized);
    win.dispatchEvent(new win.CustomEvent("rpd:langchange", { detail: { lang: normalized } }));
    win.document.querySelectorAll(".lang-switcher").forEach(updateSwitcherState);
    return currentLang;
  }

  function onLanguageChange(callback, immediate) {
    if (immediate !== false) callback(currentLang);
    var handler = function(event) {
      callback(event.detail.lang);
    };
    win.addEventListener("rpd:langchange", handler);
    return function() {
      win.removeEventListener("rpd:langchange", handler);
    };
  }

  applyDocumentLang(currentLang);

  win.RPDI18n = {
    getLanguage: function() { return currentLang; },
    setLanguage: setLanguage,
    onLanguageChange: onLanguageChange,
    getStrings: getStrings,
    localizeValue: localizeValue,
    translateCourseText: translateCourseText,
    translateShowMeUiText: translateShowMeString,
    localizeWeekData: localizeWeekData,
    getShowMeLabel: getShowMeLabel,
    getLibraryCategoryLabel: getLibraryCategoryLabel,
    getShortcutCategoryLabel: getShortcutCategoryLabel,
    localizeShowMeIframe: localizeShowMeIframe,
    mountLanguageSwitcher: mountLanguageSwitcher,
  };
}(window));
