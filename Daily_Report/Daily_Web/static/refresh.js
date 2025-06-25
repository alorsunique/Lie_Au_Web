function scheduleRefreshOnNextMinute() {
    const now = new Date();
    const delay = (60 - now.getSeconds()) * 1000 - now.getMilliseconds();

    console.log(`Next refresh in ${Math.round(delay / 1000)}s`);

    setTimeout(() => {
        if (document.visibilityState === 'visible') {
            console.log("Refreshing at:", new Date().toLocaleTimeString());
            location.reload();
        } else {
            console.log("Tab not visible at refresh time, skipping...");
        }
    }, delay);
}

// When tab becomes visible, force immediate reload
document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === 'visible') {
        console.log("Tab became visible, refreshing immediately...");
        location.reload();  // Immediately reload to catch up
    }
});

// Start minute-syncing if tab is visible on initial load
if (document.visibilityState === 'visible') {
    scheduleRefreshOnNextMinute();
}
