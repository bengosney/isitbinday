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

const dragStart = (event: DragEvent) => {
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

const dragEnd = (event: DragEvent) => {
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

const dragOver = (event: DragEvent): DataTransferObject | undefined => {
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

export default {
  dragging: false,
  state: "",
  droppable: [],
  lastDraggedOver: null,
  lastOverPosition: null,
  container: {
    [":class"]() {
      return { dragging: this.dragging };
    },
  },
  taskGroup: {
    ["x-data"]() {
      return { dragover: false };
    },
    [":class"]() {
      return {
        "drag-over": this.dragover,
        droppable: this.droppable.includes(this.$el.dataset.state),
        orderable: this.droppable.includes(this.$el.dataset.state) || this.state == this.$el.dataset.state,
      };
    },
    ["x-on:dragleave"](event: DragEvent) {
      this.dragover = false;
    },
    ["x-on:dragover.prevent"](event: DragEvent) {
      if (event.dataTransfer && this.dragging && this.droppable.includes(this.$el.dataset.state)) {
        event.dataTransfer.dropEffect = "move";
        this.dragover = true;
      }
    },
    ["x-on:drop.prevent"](event: DragEvent) {
      if (
        event.dataTransfer &&
        this.dragging &&
        (this.droppable.includes(this.$el.dataset.state) || this.$el.dataset.state === this.state)
      ) {
        const taskId = event.dataTransfer.getData("text/plain");
        const task = document.getElementById(taskId);
        if (task) {
          task.parentNode?.removeChild(task);
          const target = document.querySelector(`#${this.lastDraggedOver}`);
          switch (this.lastOverPosition) {
            case "before":
              target?.before(task);
              break;
            case "after":
              target?.after(task);
              break;
          }
        }
      }
    },
  },
  task: {
    ["x-data"]() {
      return { draggingItem: false };
    },
    ["x-on:dragend"](event: DragEvent) {
      dragEnd(event);
      this.dragging = false;
      this.droppable = [];
      this.state = "";
    },
    ["x-on:dragstart"](event: DragEvent) {
      dragStart(event);
      this.dragging = true;
      this.state = this.$el.dataset.state;
      this.droppable = this.$el.dataset.availableStates.split(",");
    },
    ["x-on:dragover"](event: DragEvent) {
      const draggedOver = dragOver(event);
      if (draggedOver) {
        this.lastDraggedOver = draggedOver.id;
        this.lastOverPosition = draggedOver.position || "";
      }
    },
    ["x-on:dragleave.self"]() {
      clearDragOver();
    },
  },
};
