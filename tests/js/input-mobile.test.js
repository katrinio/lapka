// input-mobile.js регистрирует слушатель в момент загрузки — DOM нужен до импорта.

function makeMobileViewport(matches) {
  return vi.fn().mockReturnValue({ matches });
}

async function setup(isMobile = true) {
  vi.resetModules();

  document.body.innerHTML = '<input id="terminal-command">';

  vi.stubGlobal("matchMedia", makeMobileViewport(isMobile));

  await import("../../src/static/js/terminal/input-mobile.js");
}

function focus() {
  document.getElementById("terminal-command").dispatchEvent(
    new FocusEvent("focus", { bubbles: true }),
  );
}

describe("прокрутка на мобильных", () => {
  let scrollTo;
  let raf;

  beforeEach(() => {
    scrollTo = vi.fn();
    vi.stubGlobal("scrollTo", scrollTo);

    // requestAnimationFrame выполняем синхронно.
    raf = vi.spyOn(window, "requestAnimationFrame").mockImplementation((fn) => {
      fn();
      return 0;
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("прокручивает вниз при фокусе на мобильном", async () => {
    await setup(true);
    focus();
    expect(scrollTo).toHaveBeenCalledWith(
      expect.objectContaining({ behavior: "smooth" }),
    );
  });

  it("не прокручивает на десктопе", async () => {
    await setup(false);
    focus();
    expect(scrollTo).not.toHaveBeenCalled();
  });

  it("прокрутка идёт к низу страницы", async () => {
    await setup(true);
    focus();
    expect(scrollTo).toHaveBeenCalledWith(
      expect.objectContaining({ top: document.documentElement.scrollHeight }),
    );
  });
});

describe("элемент не найден", () => {
  it("не падает если нет #terminal-command", async () => {
    vi.resetModules();
    document.body.innerHTML = "";
    vi.stubGlobal("matchMedia", makeMobileViewport(true));
    await expect(
      import("../../src/static/js/terminal/input-mobile.js"),
    ).resolves.not.toThrow();
  });
});
