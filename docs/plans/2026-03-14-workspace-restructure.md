# Workspace Restructure: RPD 독립 Repo 분리

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** RPD 프로젝트를 Workspace-level git repo에서 분리하여 독립 git repo로 만든다.

**Architecture:** Workspace/ 루트에 흩어진 RPD 관련 파일들(weeks/, tools/, resources/, templates/, docs/plans/, syllabus.md)을 RPD/ 안으로 이동시키고, RPD/를 새 git repo로 초기화한다. Workspace-level .git은 제거한다.

**현재 상태:**
- Git repo: `Workspace/` (remote: `ssongji1122/Workspace.git`)
- 29 commits, 30+ branches (대부분 Claude worktree 브랜치)
- RPD 관련 파일이 Workspace 루트에 분산: `weeks/`, `tools/`, `resources/`, `templates/`, `docs/plans/`, `syllabus.md`
- Tutorial_making (117 files)이 같은 repo에 혼재
- 3개 활성 worktree (awesome-keller, heuristic-yonath, hungry-lovelace)

---

### Task 1: Worktree 및 브랜치 정리

**Step 1: 활성 worktree 제거**

```bash
cd /Users/ssongji/Developer/Workspace
git worktree remove .claude/worktrees/awesome-keller --force 2>/dev/null
git worktree remove .claude/worktrees/heuristic-yonath --force 2>/dev/null
git worktree remove .claude/worktrees/hungry-lovelace --force 2>/dev/null
git worktree remove RPD/.claude/worktrees/awesome-keller --force 2>/dev/null
git worktree remove RPD/.claude/worktrees/heuristic-yonath --force 2>/dev/null
git worktree remove RPD/.claude/worktrees/hungry-lovelace --force 2>/dev/null
git worktree prune
```

**Step 2: Claude 브랜치 일괄 삭제**

```bash
git branch | grep 'claude/' | xargs git branch -D
```

**Step 3: 확인**

```bash
git worktree list   # main만 남아야 함
git branch          # main만 남아야 함
```

---

### Task 2: RPD 관련 파일을 RPD/ 안으로 이동

**이동 대상:**
- `weeks/` → `RPD/weeks/`
- `tools/` → `RPD/tools/`
- `resources/` → `RPD/resources/`
- `templates/` → `RPD/templates/`
- `docs/plans/` → `RPD/docs/plans/` (RPD/docs/ 이미 존재, plans/ 서브디렉토리 병합)
- `syllabus.md` → `RPD/syllabus.md`

**Step 1: 파일 이동**

```bash
cd /Users/ssongji/Developer/Workspace
mv weeks RPD/
mv tools RPD/
mv resources RPD/
mv templates RPD/
mv docs/plans RPD/docs/  # RPD/docs/plans/ 로 이동
rmdir docs 2>/dev/null   # 비어있으면 삭제
mv syllabus.md RPD/
```

**Step 2: 이동 확인**

```bash
ls RPD/
# 예상: Blender_2026/ Blender_Class101/ docs/ resources/ syllabus.md templates/ tools/ weeks/ .claude/
```

---

### Task 3: RPD를 독립 git repo로 초기화

**Step 1: RPD에 새 git repo 생성**

```bash
cd /Users/ssongji/Developer/Workspace/RPD
git init
```

**Step 2: .gitignore 생성**

기존 Workspace .gitignore에서 RPD 관련 항목을 가져와 RPD용으로 정리.

**Step 3: 초기 커밋**

```bash
cd /Users/ssongji/Developer/Workspace/RPD
git add -A
git commit -m "chore: initialize RPD as independent repo (migrated from Workspace)"
```

---

### Task 4: Workspace-level git 정리

**Step 1: Workspace .git 제거**

```bash
cd /Users/ssongji/Developer/Workspace
rm -rf .git
```

**Step 2: Workspace-level .gitignore 정리 (선택)**

Workspace가 더 이상 git repo가 아니므로 .gitignore는 불필요. 다만 Obsidian workspace로 사용 중이므로 그대로 둬도 무방.

**Step 3: GitHub remote 정리 (선택)**

기존 `ssongji1122/Workspace.git` remote는 더 이상 유효하지 않음.
RPD에 새 remote를 만들거나 기존 repo를 RPD용으로 전환할 수 있음.

---

### Task 5: 최종 검증

```bash
cd /Users/ssongji/Developer/Workspace/RPD
git status
git log --oneline
ls -la weeks/ tools/ resources/ templates/ docs/plans/
```

### 주의사항

- `RPD/Blender_2026/client_secret.json`, `youtube_token.json` 등 시크릿 파일이 untracked 상태로 존재 → .gitignore에 반드시 포함
- `Tutorial_making/`은 Workspace에 그대로 두되 git 추적 안 함 (Workspace .git 삭제하므로 자동 해결)
- 기존 git history (29 commits)는 보존하지 않음 (fresh start)
