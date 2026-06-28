// @ts-check
import { defineConfig } from 'astro/config';

// GitHub Pages project pages 로 배포: https://ssongji1122.github.io/RPD/
// 커스텀 도메인(rpd.soluta.studio) 전환 시 site 를 도메인으로, base 를 '/' 로 바꾸고
// public/CNAME 을 추가한다. 내부 링크는 src/lib/url.ts 의 url() 헬퍼가 base 를 따른다.
export default defineConfig({
  site: 'https://ssongji1122.github.io',
  base: '/RPD/',
  output: 'static',
});
