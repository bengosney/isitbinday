import Alpine from 'alpinejs';

import focus from '@alpinejs/focus'

import taskList from '../modules/dragdrop';

Alpine.plugin(focus);

declare global {
    interface Window {
        Alpine: typeof Alpine;
    }
}

window.Alpine = Alpine;


Alpine.data("taskList", () => taskList);

Alpine.start();
