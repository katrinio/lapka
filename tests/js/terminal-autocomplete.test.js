// terminal.js инициализируется внутри DOMContentLoaded.
// Каждый тест получает свежий модуль через vi.resetModules() + динамический импорт,
// после которого вручную диспатчим DOMContentLoaded.

const COMMANDS = [
  { command: "help", description: "Show help" },
  { command: "new", description: "New milestone" },
  { command: "tags", description: "List tags" },
  { command: "random", description: "Random milestone" },
  { command: "search", description: "Search" },
];

async function setup(fetchOk = true) {
  vi.resetModules();

  document.body.innerHTML = `
    <input id="terminal-command">
    <div id="terminal-suggestions" hidden></div>
  `;

  global.fetch = vi.fn().mockResolvedValue({
    ok: fetchOk,
    json: () => Promise.resolve(COMMANDS),
  });

  await import("../../src/static/js/autocomplete/core.js");
  await import("../../src/static/js/terminal/history.js");
  await import("../../src/static/js/autocomplete/terminal.js");

  // Запускаем DOMContentLoaded вручную — в jsdom он уже мог отработать.
  document.dispatchEvent(new Event("DOMContentLoaded"));

  // Ждём пока отработает async-обработчик с fetch.
  await new Promise((resolve) => setTimeout(resolve, 10));
}

function getInput() {
  return document.getElementById("terminal-command");
}

function getContainer() {
  return document.getElementById("terminal-suggestions");
}

function type(value) {
  const input = getInput();
  input.value = value;
  input.dispatchEvent(new Event("input", { bubbles: true }));
}

function press(key) {
  getInput().dispatchEvent(
    new KeyboardEvent("keydown", { key, bubbles: true, cancelable: true }),
  );
}

describe("отображение подсказок", () => {
  beforeEach(() => setup());

  it("пустой ввод не показывает подсказки", () => {
    type("");
    expect(getContainer().hidden).toBe(true);
  });

  it("совпадающий префикс показывает подсказки", () => {
    type("h");
    expect(getContainer().hidden).toBe(false);
    expect(getContainer().innerHTML).toContain("help");
  });

  it("несовпадающий ввод скрывает подсказки", () => {
    type("zzz");
    expect(getContainer().hidden).toBe(true);
  });

  it("при открытии ни один элемент не выбран", () => {
    type("h");
    const active = getContainer().querySelectorAll(".is-active");
    expect(active.length).toBe(0);
  });
});

describe("навигация стрелками", () => {
  beforeEach(() => setup());

  it("ArrowDown выбирает первый элемент", () => {
    type("h");
    press("ArrowDown");
    expect(getContainer().querySelector(".is-active")).not.toBeNull();
  });

  it("Escape скрывает подсказки", () => {
    type("h");
    expect(getContainer().hidden).toBe(false);
    press("Escape");
    expect(getContainer().hidden).toBe(true);
  });

  it("Tab применяет выбранную подсказку", () => {
    type("h");
    press("ArrowDown");
    press("Tab");
    expect(getInput().value).toBe("help");
    expect(getContainer().hidden).toBe(true);
  });

  it("Tab без выбора не меняет ввод", () => {
    type("h");
    press("Tab");
    expect(getInput().value).toBe("h");
  });
});

describe("история команд при скрытых подсказках", () => {
  beforeEach(async () => {
    localStorage.clear();
    await setup();
  });

  it("ArrowUp при пустой истории не меняет ввод", () => {
    press("ArrowUp");
    expect(getInput().value).toBe("");
  });

  it("ввод сбрасывает курсор истории", () => {
    // просто убеждаемся что input-событие не бросает ошибок
    type("h");
    type("");
    expect(getContainer().hidden).toBe(true);
  });
});

describe("клик по подсказке", () => {
  beforeEach(() => setup());

  it("клик применяет команду", () => {
    type("h");
    const suggestion = getContainer().querySelector("[data-command]");
    suggestion?.dispatchEvent(new MouseEvent("pointerdown", { bubbles: true }));
    expect(getInput().value).toBe("help");
  });
});

describe("ошибка загрузки команд", () => {
  it("при неудачном fetch список остаётся пустым", async () => {
    await setup(false);
    type("h");
    expect(getContainer().hidden).toBe(true);
  });
});
