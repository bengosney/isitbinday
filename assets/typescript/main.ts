import "./external/alpine";
import "./external/htmx";
import { dragStart, dragEnd, dragOver, dragLeave } from "./modules/dragdrop";

declare global {
  interface Window {
    dragStart: typeof dragStart;
    dragEnd: typeof dragEnd;
    dragOver: typeof dragOver;
    dragLeave: typeof dragLeave;
  }
}

const Window = window;

window.dragStart = dragStart;
window.dragEnd = dragEnd;
window.dragOver = dragOver;
window.dragLeave = dragLeave;
