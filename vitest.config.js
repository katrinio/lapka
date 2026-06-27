import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    include: ["tests/js/**/*.test.js"],
    coverage: {
      provider: "v8",
      include: ["src/static/js/**/*.js"],
      reporter: ["text", "html"],
    },
  },
});
