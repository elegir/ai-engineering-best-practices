import { test, expect } from "@playwright/test";

// Smoke = the 3–4 flows that must never break. Keep it under a minute.
// Selectors: accessibility tree (role/name/label), never brittle CSS. Assertions on text/state, not pixels.
const USER = { email: process.env.E2E_USER ?? "<<seed-user@example.com>>", password: process.env.E2E_PASS ?? "<<seed-password>>" };

test.describe("smoke", () => {
  test("home page renders and has no console errors", async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (e) => errors.push(e.message));
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    expect(errors, `console errors: ${errors.join("; ")}`).toHaveLength(0);
  });

  test("login works with the seed user", async ({ page }) => {
    await page.goto("/<<login>>");
    await page.getByLabel(/email/i).fill(USER.email);
    await page.getByLabel(/password/i).fill(USER.password);
    await page.getByRole("button", { name: /log in|sign in/i }).click();
    await expect(page.getByRole("navigation")).toContainText(/<<dashboard|logout>>/i);
  });

  test("core flow: <<create the main thing>>", async ({ page }) => {
    // Seed state through the API/fixtures when possible instead of clicking through.
    await page.goto("/<<core-path>>");
    await page.getByRole("button", { name: /<<new>>/i }).click();
    await page.getByLabel(/<<name>>/i).fill("Smoke item");
    await page.getByRole("button", { name: /save/i }).click();
    await expect(page.getByText("Smoke item")).toBeVisible();
  });

  test("API health endpoint responds", async ({ request }) => {
    const res = await request.get("/<<health>>");
    expect(res.ok()).toBeTruthy();
  });
});
