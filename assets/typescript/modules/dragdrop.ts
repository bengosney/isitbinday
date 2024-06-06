const dragClass = 'dragging';

export const dragStart = (event: DragEvent) => {
    if (event.dataTransfer !== null && event.target !== null && event.target instanceof HTMLElement !== false) {
        const { target, dataTransfer } = event;

        setTimeout(() => target.classList.add(dragClass), 10);

        dataTransfer.effectAllowed = 'move';
        dataTransfer.setData('text/plain', event.target.id);

        const { width, height, left, top } = event.target.getBoundingClientRect();
        target.style.height = `${height}px`;
        const { clientX, clientY } = event;

        const x = clientX - left;
        const y = clientY - top;

        const clone = target.cloneNode(true) as HTMLElement;

        clone.classList.add('drag-ghost');
        clone.style.position = 'absolute';
        clone.style.top = `-${height * 10}px`;
        clone.style.width = `${width}px`;
        clone.style.height = `${height}px`;
        document.body.appendChild(clone);
        dataTransfer.setDragImage(clone, x, y);
    }
}

export const dragEnd = (event: DragEvent) => {
    document.querySelectorAll('.drag-ghost').forEach((ghost) => {
        ghost.remove();
    });

    if (event.target !== null && event.target instanceof HTMLElement !== false) {
        console.log('dragEnd', event.target.classList);
        const { target } = event;

        target.classList.remove(dragClass);
        target.addEventListener('transitionend', () => {
            target.style.height = '';
        }, { once: true });
    }
}
