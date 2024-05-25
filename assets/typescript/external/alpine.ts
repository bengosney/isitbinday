import Alpine from 'alpinejs';

import focus from '@alpinejs/focus'

Alpine.plugin(focus);

declare global {
    interface Window {
        Alpine: typeof Alpine;
    }
}

window.Alpine = Alpine;

Alpine.start();
