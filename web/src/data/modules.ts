export interface Module {
  id: string;
  label: string;
  title: string;
  description: string;
  topics: string[];
  week?: string;
}

export const modules: Module[] = [
  {
    id: 'r0',
    label: 'R0',
    title: 'SOLV 복습 — Claude · 프롬프팅 · Artifacts',
    description: 'studio.soluta M1~M3 핵심 개념을 RPD 맥락으로 재정리합니다.',
    topics: ['Claude 기본 사용법', '효과적인 프롬프팅', 'Artifacts 활용', 'Context Window 이해'],
    week: 'W01',
  },
  {
    id: 'r1',
    label: 'R1',
    title: 'Blender + Claude 연동',
    description: 'Blender MCP를 설정하고, Claude로 3D 씬을 프롬프트로 제어합니다.',
    topics: ['Blender MCP 설치', 'Python API 기초', 'AI 프롬프트로 씬 제어', '오브젝트 생성 자동화'],
    week: 'W03',
  },
  {
    id: 'r2',
    label: 'R2',
    title: '로봇 제품 디자인 맥락 프롬프팅',
    description: '형태, 기구, 마감 기술 언어를 사용해 제품 디자인에 특화된 프롬프트를 작성합니다.',
    topics: ['제품 기술 언어', '형태 묘사 프롬프트', '재질·마감 표현', '반복 개선 프로세스'],
    week: 'W05',
  },
  {
    id: 'r3',
    label: 'R3',
    title: 'Artifacts로 제품 스펙 문서 생성',
    description: 'Claude Artifacts를 활용해 제품 스펙 시트, 비교표, 제안서를 만듭니다.',
    topics: ['스펙 문서 구조', '비교표 자동 생성', '제안서 템플릿', '반복 활용 패턴'],
    week: 'W08',
  },
  {
    id: 'r4',
    label: 'R4',
    title: 'Projects로 설계 레퍼런스 DB 구축',
    description: 'Claude Projects에 디자인 레퍼런스를 업로드하고 지식베이스로 활용합니다.',
    topics: ['Projects 설정', '레퍼런스 문서화', '컨텍스트 유지 전략', '팀 공유 방법'],
    week: 'W10',
  },
  {
    id: 'r5',
    label: 'R5',
    title: 'AI + Blender로 포트폴리오 자동화',
    description: '수업 결과물을 AI로 정리해 포트폴리오 페이지를 자동 생성하는 캡스톤 프로젝트입니다.',
    topics: ['결과물 구조화', 'AI 서술문 생성', 'Blender 렌더 자동화', '포트폴리오 퍼블리시'],
    week: 'W13',
  },
];

export function getModule(id: string) {
  return modules.find((m) => m.id === id);
}
