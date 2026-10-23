(() => {
    const dialog = document.querySelector(".journal-dialog");
    const dialogBody = dialog && dialog.querySelector(".journal-dialog-body");
    const closeButton = dialog && dialog.querySelector(".journal-dialog-close");

    if (!dialog || !dialogBody || !closeButton || typeof dialog.showModal !== "function") {
        return;
    }

    let lastTrigger = null;

    document.addEventListener("click", (event) => {
        const trigger = event.target.closest("a[data-blog-template]");
        if (
            !trigger ||
            event.defaultPrevented ||
            event.button !== 0 ||
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey
        ) {
            return;
        }

        const template = document.getElementById(trigger.dataset.blogTemplate);
        if (!template) return;

        event.preventDefault();
        lastTrigger = trigger;
        dialogBody.replaceChildren(template.content.cloneNode(true));
        dialog.showModal();
        closeButton.focus();
    });

    closeButton.addEventListener("click", () => dialog.close());

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && dialog.open) {
            event.preventDefault();
            dialog.close();
        }
    });

    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) dialog.close();
    });

    dialog.addEventListener("close", () => {
        dialogBody.replaceChildren();
        if (lastTrigger && lastTrigger.isConnected) lastTrigger.focus();
        lastTrigger = null;
    });
})();
