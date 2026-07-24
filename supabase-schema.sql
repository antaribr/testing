-- Scout Manager Supabase schema

create table if not exists public.members (
  id uuid primary key default gen_random_uuid(),
  first_name text not null,
  last_name text not null,
  middle_name text,
  unit text,
  phone text,
  parent_phone text,
  blood_type text,
  nationality text,
  dob date,
  email text,
  created_at timestamptz default now()
);

create table if not exists public.leaders (
  id uuid primary key default gen_random_uuid(),
  full_name text not null,
  dob date,
  role text,
  phone text,
  email text,
  join_date date,
  created_at timestamptz default now()
);

create table if not exists public.payments (
  id uuid primary key default gen_random_uuid(),
  member_id uuid references public.members(id) on delete cascade,
  year integer not null,
  amount numeric(10,2) not null default 0,
  status text not null default 'Pending',
  payment_date date,
  notes text,
  created_at timestamptz default now()
);

create table if not exists public.badges (
  id uuid primary key default gen_random_uuid(),
  member_id uuid references public.members(id) on delete cascade,
  badge_name text not null,
  awarded_date date,
  awarded_by text,
  created_at timestamptz default now()
);

create table if not exists public.ranks (
  id uuid primary key default gen_random_uuid(),
  member_id uuid references public.members(id) on delete cascade,
  rank_name text not null,
  effective_date date,
  notes text,
  created_at timestamptz default now()
);

create table if not exists public.member_attendance (
  id uuid primary key default gen_random_uuid(),
  member_id uuid references public.members(id) on delete cascade,
  date date not null,
  status text not null,
  activity text,
  notes text,
  created_at timestamptz default now()
);

create table if not exists public.leader_attendance (
  id uuid primary key default gen_random_uuid(),
  leader_id uuid references public.leaders(id) on delete cascade,
  date date not null,
  status text not null,
  meeting text,
  notes text,
  created_at timestamptz default now()
);

create table if not exists public.meetings (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  meeting_date date not null,
  location text,
  created_by text,
  description text,
  minutes text,
  created_at timestamptz default now()
);

create table if not exists public.meeting_points (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid references public.meetings(id) on delete cascade,
  text text not null,
  sort_order integer default 0,
  created_at timestamptz default now()
);

create table if not exists public.meeting_members (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid references public.meetings(id) on delete cascade,
  member_id uuid references public.members(id) on delete cascade,
  created_at timestamptz default now(),
  unique(meeting_id, member_id)
);

create table if not exists public.meeting_leaders (
  id uuid primary key default gen_random_uuid(),
  meeting_id uuid references public.meetings(id) on delete cascade,
  leader_id uuid references public.leaders(id) on delete cascade,
  point text,
  created_at timestamptz default now(),
  unique(meeting_id, leader_id)
);

alter table public.members enable row level security;
alter table public.leaders enable row level security;
alter table public.payments enable row level security;
alter table public.badges enable row level security;
alter table public.ranks enable row level security;
alter table public.member_attendance enable row level security;
alter table public.leader_attendance enable row level security;
alter table public.meetings enable row level security;
alter table public.meeting_points enable row level security;
alter table public.meeting_members enable row level security;
alter table public.meeting_leaders enable row level security;

create policy "authenticated users can read members" on public.members for select to authenticated using (true);
create policy "authenticated users can insert members" on public.members for insert to authenticated with check (true);
create policy "authenticated users can update members" on public.members for update to authenticated using (true);
create policy "authenticated users can delete members" on public.members for delete to authenticated using (true);

create policy "authenticated users can read leaders" on public.leaders for select to authenticated using (true);
create policy "authenticated users can insert leaders" on public.leaders for insert to authenticated with check (true);
create policy "authenticated users can update leaders" on public.leaders for update to authenticated using (true);
create policy "authenticated users can delete leaders" on public.leaders for delete to authenticated using (true);

create policy "authenticated users can read payments" on public.payments for select to authenticated using (true);
create policy "authenticated users can insert payments" on public.payments for insert to authenticated with check (true);
create policy "authenticated users can update payments" on public.payments for update to authenticated using (true);
create policy "authenticated users can delete payments" on public.payments for delete to authenticated using (true);

create policy "authenticated users can read badges" on public.badges for select to authenticated using (true);
create policy "authenticated users can insert badges" on public.badges for insert to authenticated with check (true);
create policy "authenticated users can update badges" on public.badges for update to authenticated using (true);
create policy "authenticated users can delete badges" on public.badges for delete to authenticated using (true);

create policy "authenticated users can read ranks" on public.ranks for select to authenticated using (true);
create policy "authenticated users can insert ranks" on public.ranks for insert to authenticated with check (true);
create policy "authenticated users can update ranks" on public.ranks for update to authenticated using (true);
create policy "authenticated users can delete ranks" on public.ranks for delete to authenticated using (true);

create policy "authenticated users can read member attendance" on public.member_attendance for select to authenticated using (true);
create policy "authenticated users can insert member attendance" on public.member_attendance for insert to authenticated with check (true);
create policy "authenticated users can update member attendance" on public.member_attendance for update to authenticated using (true);
create policy "authenticated users can delete member attendance" on public.member_attendance for delete to authenticated using (true);

create policy "authenticated users can read leader attendance" on public.leader_attendance for select to authenticated using (true);
create policy "authenticated users can insert leader attendance" on public.leader_attendance for insert to authenticated with check (true);
create policy "authenticated users can update leader attendance" on public.leader_attendance for update to authenticated using (true);
create policy "authenticated users can delete leader attendance" on public.leader_attendance for delete to authenticated using (true);

create policy "authenticated users can read meetings" on public.meetings for select to authenticated using (true);
create policy "authenticated users can insert meetings" on public.meetings for insert to authenticated with check (true);
create policy "authenticated users can update meetings" on public.meetings for update to authenticated using (true);
create policy "authenticated users can delete meetings" on public.meetings for delete to authenticated using (true);

create policy "authenticated users can read meeting points" on public.meeting_points for select to authenticated using (true);
create policy "authenticated users can insert meeting points" on public.meeting_points for insert to authenticated with check (true);
create policy "authenticated users can update meeting points" on public.meeting_points for update to authenticated using (true);
create policy "authenticated users can delete meeting points" on public.meeting_points for delete to authenticated using (true);

create policy "authenticated users can read meeting members" on public.meeting_members for select to authenticated using (true);
create policy "authenticated users can insert meeting members" on public.meeting_members for insert to authenticated with check (true);
create policy "authenticated users can delete meeting members" on public.meeting_members for delete to authenticated using (true);

create policy "authenticated users can read meeting leaders" on public.meeting_leaders for select to authenticated using (true);
create policy "authenticated users can insert meeting leaders" on public.meeting_leaders for insert to authenticated with check (true);
create policy "authenticated users can update meeting leaders" on public.meeting_leaders for update to authenticated using (true);
create policy "authenticated users can delete meeting leaders" on public.meeting_leaders for delete to authenticated using (true);

-- Weekly Submissions table for Mobile submit section
create table if not exists public.weekly_submissions (
  id uuid primary key default gen_random_uuid(),
  commissariat text default 'الجنوب',
  group_name text default 'صيدا الأول',
  unit text not null,
  unit_canonical text,
  leader_email text,
  outgoing_number text,
  place text,
  date_dmy text,
  skills jsonb,
  schedule jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  created_by text
);

alter table public.weekly_submissions enable row level security;

create policy "authenticated users can read weekly submissions" on public.weekly_submissions for select to authenticated using (true);
create policy "authenticated users can insert weekly submissions" on public.weekly_submissions for insert to authenticated with check (true);
create policy "authenticated users can update weekly submissions" on public.weekly_submissions for update to authenticated using (true);
create policy "authenticated users can delete weekly submissions" on public.weekly_submissions for delete to authenticated using (true);

create policy "anon users can read weekly submissions" on public.weekly_submissions for select to anon using (true);
create policy "anon users can insert weekly submissions" on public.weekly_submissions for insert to anon with check (true);
create policy "anon users can update weekly submissions" on public.weekly_submissions for update to anon using (true);

