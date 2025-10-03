const actions_menus = document.querySelectorAll(".actions-block");
const btn_actions = document.querySelectorAll("#more-actions");

btn_actions.forEach(button => {
    button.addEventListener("click", () => {
        btn_actions.forEach(btn => {
            const m = btn.nextElementSibling;

            if (!m.classList.contains("hidden")) {
                m.classList.add("hidden");
            }
        });

        const menu = button.nextElementSibling;

        menu.classList.toggle("hidden");
    });
});

document.addEventListener("click", (event) => {
    const btn_arr = Array.from(btn_actions)
    const isClickInsideMenu = event.target.closest(".actions-block");
    const isClickOnButton = btn_arr.some(button => button === event.target) || btn_arr.some(button => button === event.target.parentElement);

    if (!isClickInsideMenu && !isClickOnButton) {
        document.querySelectorAll(".actions-block").forEach(block => {
            block.classList.add("hidden");
        });
    }
});