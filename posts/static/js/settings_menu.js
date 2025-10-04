(function () {
    document.addEventListener('DOMContentLoaded', function () {
        var toggle = document.querySelector('[data-settings-toggle]');
        var submenu = document.querySelector('[data-settings-submenu]');

        if (!toggle || !submenu) {
            return;
        }

        var navItem = toggle.closest('.nav-item-settings');

        var openClass = 'settings-submenu--visible';

        submenu.setAttribute('aria-hidden', 'true');

        var closeSubmenu = function () {
            toggle.setAttribute('aria-expanded', 'false');
            submenu.classList.remove(openClass);
            submenu.setAttribute('aria-hidden', 'true');
            if (navItem) {
                navItem.classList.remove('settings-submenu-open');
            }
        };

        toggle.addEventListener('click', function (event) {
            var isExpanded = toggle.getAttribute('aria-expanded') === 'true';

            if (!isExpanded) {
                event.preventDefault();
                toggle.setAttribute('aria-expanded', 'true');
                submenu.classList.add(openClass);
                submenu.setAttribute('aria-hidden', 'false');
                if (navItem) {
                    navItem.classList.add('settings-submenu-open');
                }
                return;
            }

            closeSubmenu();
        });

        document.addEventListener('click', function (event) {
            if (!submenu.classList.contains(openClass)) {
                return;
            }

            if (submenu.contains(event.target)) {
                return;
            }

            if (event.target === toggle || toggle.contains(event.target)) {
                return;
            }

            closeSubmenu();
        });
    });
})();
