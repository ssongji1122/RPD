export interface Week {
  week: string;
  title: string;
  description: string;
  module?: string;
  type: 'lecture' | 'workshop' | 'review' | 'project';
}

export const syllabus: Week[] = [
  { week: 'W01', title: 'SOLV 복습 — Claude 기초', description: 'Claude 기본 사용법과 프롬프팅 원칙 재정리', module: 'r0', type: 'lecture' },
  { week: 'W02', title: 'SOLV 복습 — Artifacts 실습', description: 'Artifacts로 시각 자료 생성 실습', module: 'r0', type: 'workshop' },
  { week: 'W03', title: 'Blender MCP 설치 및 기초', description: 'Blender와 Claude 연동 환경 세팅', module: 'r1', type: 'lecture' },
  { week: 'W04', title: 'AI로 3D 씬 제어', description: '프롬프트로 오브젝트 생성·배치·수정', module: 'r1', type: 'workshop' },
  { week: 'W05', title: '제품 디자인 기술 언어', description: '형태·기구·마감 묘사 프롬프팅 기법', module: 'r2', type: 'lecture' },
  { week: 'W06', title: '형태 탐색 워크샵', description: '프롬프트 반복으로 형태 아이디에이션', module: 'r2', type: 'workshop' },
  { week: 'W07', title: '중간 리뷰', description: 'R0~R2 결과물 발표 및 피드백', type: 'review' },
  { week: 'W08', title: '제품 스펙 문서 생성', description: 'Artifacts로 스펙 시트·비교표 작성', module: 'r3', type: 'lecture' },
  { week: 'W09', title: '스펙 문서 실습', description: '실제 프로젝트에 스펙 문서 적용', module: 'r3', type: 'workshop' },
  { week: 'W10', title: '설계 레퍼런스 DB 구축', description: 'Projects에 레퍼런스 업로드·활용', module: 'r4', type: 'lecture' },
  { week: 'W11', title: '지식베이스 심화', description: '컨텍스트 유지 전략 및 팀 공유', module: 'r4', type: 'workshop' },
  { week: 'W12', title: '포트폴리오 기획', description: '캡스톤 프로젝트 구조 기획', module: 'r5', type: 'lecture' },
  { week: 'W13', title: 'AI 서술문 + 렌더 자동화', description: 'AI로 결과물 서술 및 Blender 렌더 자동화', module: 'r5', type: 'workshop' },
  { week: 'W14', title: '포트폴리오 완성', description: '포트폴리오 페이지 퍼블리시', module: 'r5', type: 'project' },
  { week: 'W15', title: '최종 발표', description: '전체 결과물 발표 및 마무리', type: 'review' },
];
