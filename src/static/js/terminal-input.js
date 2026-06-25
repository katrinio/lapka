const terminalInput = document.getElementById("terminal-command");

// Сопоставляет введённую команду с URL.
const COMMAND_ROUTES = {
  help: "/help",
  tags: "/tags",
};

if (terminalInput) {
  // Срабатывает по Enter в терминальной строке.
  terminalInput.addEventListener("keydown", (event) => {
    if (event.key !== "Enter") {
      return;
    }

    const command = terminalInput.value.trim().toLowerCase();
    const route = COMMAND_ROUTES[command];

    if (route) {
      window.location.href = route;
    }
  });
}
