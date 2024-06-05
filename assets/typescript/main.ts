import './external/alpine';
import './external/htmx';
import { dragStart, dragEnd} from './modules/dragdrop';

declare global {
    interface Window {
        dragStart: typeof dragStart;
        dragEnd: typeof dragEnd;
    }
}

const Window = window;

window.dragStart = dragStart;
window.dragEnd = dragEnd;
