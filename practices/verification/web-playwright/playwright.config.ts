import { defineConfig, devices } from "@playwright/test";

// Install: npm i -D @playwright/test && npx playwright install chromium
// Run:     npx playwright test            (full)   |  npx playwright test e2e/smoke (smoke only)
export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  retries: process.env.CI ? 1 : 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: process.env.BASE_URL ?? "http://localhost:<<3000>>",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  // Start the app for the tests unless BASE_URL points to a running one.
  webServer: process.env.BASE_URL
    ? undefined
    : {
        command: "<<npm run dev>>",
        url: "http://localhost:<<3000>>/<<health>>",
        reuseExistingServer: true,
        timeout: 120_000,
      },
});
