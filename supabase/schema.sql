-- =====================================================================
-- RPD Supabase Schema
-- Supabase 대시보드 → SQL Editor에서 이 파일 전체를 실행하세요.
-- =====================================================================

-- ── 1. profiles 테이블 ───────────────────────────────────────────────
-- auth.users와 1:1 연결. 이름, 역할(admin/student) 저장.
create table if not exists public.profiles (
  id          uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  role        text not null default 'student',   -- 'student' | 'admin'
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

-- 새 유저 가입 시 profiles 자동 생성 트리거
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer as $$
begin
  insert into public.profiles (id, display_name, role)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'full_name', new.email),
    'student'
  )
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- ── 2. decks 테이블 ──────────────────────────────────────────────────
-- 유저별 덱 저장. localStorage의 DeckStore 구조와 동일한 JSON 스키마.
create table if not exists public.decks (
  id          text primary key,           -- 'deck-xxx' 형태 클라이언트 생성 ID
  user_id     uuid not null references auth.users(id) on delete cascade,
  name        text not null,
  description text not null default '',
  items       jsonb not null default '[]', -- [{type:'card', id:'slug'}, ...]
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

create index if not exists decks_user_id_idx on public.decks(user_id);

-- updated_at 자동 갱신
create or replace function public.update_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists decks_updated_at on public.decks;
create trigger decks_updated_at
  before update on public.decks
  for each row execute procedure public.update_updated_at();

-- ── 3. Row Level Security (RLS) ──────────────────────────────────────

alter table public.profiles enable row level security;
alter table public.decks     enable row level security;

-- profiles: 본인만 읽기/수정
create policy "profiles: self read"
  on public.profiles for select
  using (auth.uid() = id);

create policy "profiles: self update"
  on public.profiles for update
  using (auth.uid() = id);

-- decks: 본인만 CRUD
create policy "decks: self select"
  on public.decks for select
  using (auth.uid() = user_id);

create policy "decks: self insert"
  on public.decks for insert
  with check (auth.uid() = user_id);

create policy "decks: self update"
  on public.decks for update
  using (auth.uid() = user_id);

create policy "decks: self delete"
  on public.decks for delete
  using (auth.uid() = user_id);

-- ── 4. admin role 부여 함수 ─────────────────────────────────────────
-- SQL Editor에서 직접 실행: select make_admin('user@email.com');
create or replace function public.make_admin(target_email text)
returns text language plpgsql security definer as $$
declare
  target_id uuid;
begin
  select id into target_id from auth.users where email = target_email;
  if target_id is null then
    return 'User not found: ' || target_email;
  end if;
  update public.profiles set role = 'admin' where id = target_id;
  return 'OK: ' || target_email || ' is now admin';
end;
$$;
