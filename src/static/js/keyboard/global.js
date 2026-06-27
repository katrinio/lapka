function getTerminalInput() {
  return document.getElementById("terminal-command");
}

function getSuggestionsContainer() {
  return document.getElementById("terminal-suggestions");
}

function isEditableElement(target) {
  // Обычные поля формы не должны перехватывать глобальные хоткеи.
  return (
    target instanceof HTMLInputElement ||
    target instanceof HTMLTextAreaElement ||
    target instanceof HTMLSelectElement ||
    target?.isContentEditable
  );
}

function isTerminalInput(target) {
  const terminalInput = getTerminalInput();
  return terminalInput ? target === terminalInput : false;
}

function closeTerminalSuggestions() {
  const container = getSuggestionsContainer();

  if (!container) {
    return;
  }

  container.hidden = true;
  container.innerHTML = "";
}

function focusTerminal() {
  const terminalInput = getTerminalInput();

  if (!terminalInput) {
    return;
  }

  terminalInput.focus();
  terminalInput.select();
}

document.addEventListener("keydown", (event) => {
  const target = event.target;

  // "/" открывает терминал только вне форм и contenteditable.
  if (event.key === "/") {
    if (isEditableElement(target)) {
      return;
    }

    event.preventDefault();
    focusTerminal();
    return;
  }

  if (event.key === "Escape") {
    // Escape закрывает терминальные подсказки и убирает фокус с терминала.
    closeTerminalSuggestions();

    if (isTerminalInput(target)) {
      event.preventDefault();
      target.blur();
    }
  }
});
