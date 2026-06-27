


let selectedIndex = -1;

function getRows() {
  return [...document.querySelectorAll("[data-keyboard-row]")];
}

function renderSelection(rows) {
  rows.forEach((row, index) => {
    row.classList.toggle("is-selected", index === selectedIndex);
  });
}

function moveSelection(direction) {
  const rows = getRows();

  if (!rows.length) {
    return;
  }

  if (selectedIndex === -1) {
    selectedIndex = direction === "down" ? 0 : rows.length - 1;
  } else if (direction === "down") {
    selectedIndex = Math.min(selectedIndex + 1, rows.length - 1);
  } else {
    selectedIndex = Math.max(selectedIndex - 1, 0);
  }

  renderSelection(rows);
}

function openSelectedRow() {
  const rows = getRows();
  const row = rows[selectedIndex];

  if (!row) {
    return;
  }

  window.location.href = row.href;
}

document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowDown") {
    event.preventDefault();
    moveSelection("down");
  }

  if (event.key === "ArrowUp") {
    event.preventDefault();
    moveSelection("up");
  }

  if (event.key === "Enter") {
    openSelectedRow();
  }
});
