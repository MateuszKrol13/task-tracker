function toggleTab(target) {
    const parent = target.parentElement;
    tabs = parent.querySelectorAll("div.tab-content");
    tabs.forEach((tab) => {tab.style.display = "none";});
    target.style.display = "unset";
}

