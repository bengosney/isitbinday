export const dragStart = (event: DragEvent) => {
    if (event.dataTransfer === null || event.target === null || event.target instanceof HTMLElement === false) {
        return;
    }

    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/plain', event.target.id);

    const { width, height, left, top } = event.target.getBoundingClientRect();
    const { clientX, clientY } = event;

    const x = clientX - left;
    const y = clientY - top;

    const clone = event.target.cloneNode(true) as HTMLElement;

    clone.classList.add('drag-ghost');
    clone.style.position = 'absolute';
    clone.style.top = `-${height * 10}px`;
    clone.style.width = `${width}px`;
    clone.style.height = `${height}px`;
    document.body.appendChild(clone);
    event.dataTransfer.setDragImage(clone, x, y);
}

export const dragEnd = (element: HTMLElement) => {
    document.querySelectorAll('.drag-ghost').forEach((ghost) => {
        ghost.remove();
    });
}
