$ = (q) => {
    if (q.length > 0) {
        return document.querySelectorAll(q);
    } else {
        throw new Error("No query provided");
    }
}

