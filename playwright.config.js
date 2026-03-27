// @ts-check
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 15000,
  retries: 0,
  use: {
    baseURL: 'http://localhost:8771',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npx serve course-site -l 8771 --no-clipboard',
    port: 8771,
    reuseExistingServer: true,
  },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1280, height: 800 } } },
    { name: 'mobile', use: { viewport: { width: 375, height: 812 } } },
  ],
});
