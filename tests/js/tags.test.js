// tags.js регистрирует слушатели в момент загрузки — DOM нужен до импорта.
// Используем динамические импорты в beforeAll.

beforeAll(async () => {
  document.body.innerHTML = `
    <input id="tags-input" data-tags="WORK,TRAVEL,TECH,INFRA,DEV,PERSONAL">
    <div id="tag-suggestions"></div>
  `;
  await import("../../src/static/js/autocomplete/core.js");
  await import("../../src/static/js/autocomplete/tags.js");
});

function getInput() {
  return document.getElementById("tags-input");
}

function getSuggestions() {
  return document.getElementById("tag-suggestions");
}

function type(value, cursor = value.length) {
  const input = getInput();
  input.value = value;
  Object.defineProperty(input, "selectionStart", { get: () => cursor, configurable: true });
  input.dispatchEvent(new Event("input", { bubbles: true }));
}

function clickSuggestion(index = 0) {
  const buttons = getSuggestions().querySelectorAll("button");
  buttons[index]?.click();
}

afterEach(() => {
  getInput().value = "";
  getSuggestions().innerHTML = "";
  getSuggestions().hidden = true;
});

describe("подсказки тегов", () => {
  it("показывает подходящие теги по префиксу", () => {
    type("W");
    const buttons = getSuggestions().querySelectorAll("button");
    expect(buttons.length).toBe(1);
    expect(buttons[0].textContent).toBe("WORK");
  });

  it("показывает несколько совпадений", () => {
    type("T");
    const buttons = getSuggestions().querySelectorAll("button");
    expect(buttons.length).toBe(2);
  });

  it("скрывает подсказки при пустом токене", () => {
    type("W");
    expect(getSuggestions().hidden).toBe(false);
    type("");
    expect(getSuggestions().hidden).toBe(true);
  });

  it("скрывает подсказки если нет совпадений", () => {
    type("XYZ");
    expect(getSuggestions().hidden).toBe(true);
  });

  it("совпадение нечувствительно к регистру", () => {
    type("w");
    const buttons = getSuggestions().querySelectorAll("button");
    expect(buttons[0].textContent).toBe("WORK");
  });
});

describe("вставка тега по клику", () => {
  it("вставляет тег в пустое поле", () => {
    type("W");
    clickSuggestion(0);
    expect(getInput().value).toBe("WORK");
  });

  it("заменяет текущий токен выбранным тегом", () => {
    type("WO");
    clickSuggestion(0);
    expect(getInput().value).toContain("WORK");
  });

  it("скрывает подсказки после выбора", () => {
    type("W");
    clickSuggestion(0);
    expect(getSuggestions().hidden).toBe(true);
  });

  it("вставляет тег в середину строки с разделителем", () => {
    type("INFRA W", 7);
    clickSuggestion(0);
    expect(getInput().value).toContain("WORK");
    expect(getInput().value).toContain("INFRA");
  });
});

describe("навигация по списку", () => {
  it("показывает не более 5 подсказок", () => {
    type("A");
    // нет тегов на A — должно быть скрыто
    expect(getSuggestions().hidden).toBe(true);
  });

  it("событие keyup тоже обновляет подсказки", () => {
    const input = getInput();
    input.value = "W";
    input.dispatchEvent(new Event("keyup", { bubbles: true }));
    expect(getSuggestions().querySelectorAll("button").length).toBe(1);
  });

  it("событие click на input обновляет подсказки", () => {
    const input = getInput();
    input.value = "T";
    input.dispatchEvent(new Event("click", { bubbles: true }));
    expect(getSuggestions().querySelectorAll("button").length).toBe(2);
  });
});
