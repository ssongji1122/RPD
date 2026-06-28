// 내부 링크·자산 경로를 배포 base 에 맞춰 보정한다.
// GitHub Pages project pages 는 /RPD/ 하위 경로라 절대경로 링크에 base 가 필요하다.
// 커스텀 도메인(rpd.soluta.studio) 전환 시 astro.config 의 base 를 '/' 로 바꾸면
// 이 헬퍼가 자동으로 루트 경로를 낸다.
const BASE = import.meta.env.BASE_URL; // 예: '/RPD/' 또는 '/'

export function url(path: string): string {
  const b = BASE.endsWith('/') ? BASE.slice(0, -1) : BASE;
  return path.startsWith('/') ? `${b}${path}` : `${b}/${path}`;
}
