const dragClass = "dragging";

const clearDragOver = () => {
  ["move-up", "move-down"].forEach((selector) => {
    document.querySelectorAll(`.${selector}`).forEach((element) => element.classList.remove(selector));
  });
};

interface DataTransferObject {
  id: string;
  position?: "before" | "after";
}

export const dragStart = (event: DragEvent) => {
  clearDragOver();
  if (event.dataTransfer !== null && event.target instanceof HTMLElement !== false) {
    const { target, dataTransfer } = event;

    setTimeout(() => target.classList.add(dragClass), 10);

    dataTransfer.effectAllowed = "move";
    dataTransfer.setData("text/plain", target.id);

    const { width, height, left, top } = target.getBoundingClientRect();
    target.style.height = `${height}px`;
    const taskList = target.closest(".task-list");
    if (taskList instanceof HTMLElement !== false) {
      taskList.style.setProperty("--move-height", `${height}px`);
    }
    const { clientX, clientY } = event;

    const x = clientX - left;
    const y = clientY - top;

    const clone = target.cloneNode(true) as HTMLElement;

    clone.removeAttribute("x-data");
    clone.removeAttribute("x-bind");
    clone.classList.add("drag-ghost");
    clone.style.position = "absolute";
    clone.style.top = `-${height * 10}px`;
    clone.style.width = `${width}px`;
    clone.style.height = `${height}px`;
    document.body.appendChild(clone);
    dataTransfer.setDragImage(clone, x, y);
  }
};

export const dragEnd = (event: DragEvent) => {
  document.querySelectorAll(".drag-ghost").forEach((ghost) => ghost.remove());
  const { target, dataTransfer } = event;

  if (dataTransfer && target !== null && target instanceof HTMLElement !== false) {
    target.classList.remove(dragClass);
    target.addEventListener(
      "transitionend",
      () => {
        target.style.height = "";
        clearDragOver();
      },
      { once: true },
    );
  }
};

export const dragOver = (event: DragEvent): DataTransferObject | undefined => {
  clearDragOver();
  if (event.dataTransfer && event.target !== null && event.target instanceof HTMLElement !== false) {
    const target = event.target.closest(".task") as HTMLElement;
    const { height, top } = target.getBoundingClientRect();
    const { clientY } = event;

    const data: DataTransferObject = { id: target.id };
    if (clientY < top + height / 2) {
      target.classList.add("move-down");
      data.position = "before";
    } else {
      target.classList.add("move-up");
      data.position = "after";
    }

    return data;
  }
};

export const dragLeave = (event: DragEvent) => {
  clearDragOver();
};
