(function () {
    const datasetEl = document.getElementById('discover-data');

    if (!datasetEl) {
        return;
    }

    const members = JSON.parse(datasetEl.textContent || '[]');
    const cardStack = document.querySelector('[data-card-stack]');
    const emptyState = document.querySelector('[data-empty-state]');
    const feedback = document.querySelector('[data-action-feedback]');
    const likeButton = document.querySelector('[data-action="like"]');
    const dislikeButton = document.querySelector('[data-action="dislike"]');
    const rewindButton = document.querySelector('[data-action="rewind"]');
    const lookingForSelect = document.querySelector('[data-looking-for]');
    const minAgeInput = document.querySelector('[data-min-age]');
    const maxAgeInput = document.querySelector('[data-max-age]');
    const countrySelect = document.querySelector('[data-country]');
    const citySelect = document.querySelector('[data-city]');
    const resultsCounter = document.querySelector('[data-results-count]');
    const filterToggle = document.querySelector('[data-filter-toggle]');
    const filterPanel = document.querySelector('[data-filter-panel]');
    const filterOverlay = document.querySelector('[data-filter-overlay]');
    const filterCloseButtons = document.querySelectorAll('[data-filter-close]');
    const filterForm = document.querySelector('[data-filter-form]');
    const resetFiltersButton = document.querySelector('[data-reset-filters]');
    const distanceInput = document.querySelector('[data-distance]');
    const distanceValue = document.querySelector('[data-distance-value]');
    const interestCheckboxes = filterForm ? filterForm.querySelectorAll('[data-interest-filter]') : [];

    let filteredMembers = members.slice();
    let deck = filteredMembers.slice();
    const history = [];
    let activeCard = null;
    let pointerStart = null;
    let lastFocusedElement = null;
    const defaultCardPhoto = 'https://placehold.co/600x600?text=Lixy';
    const dragThreshold = 6;
    const supportsPointerEvents = 'PointerEvent' in window;

    function updateResultsCounter() {
        if (resultsCounter) {
            resultsCounter.textContent = deck.length;
        }
    }

    function updateEmptyState() {
        if (!emptyState) {
            return;
        }

        if (deck.length === 0) {
            emptyState.classList.remove('d-none');
        } else {
            emptyState.classList.add('d-none');
        }
    }

    function clearFeedback() {
        if (!feedback) {
            return;
        }

        feedback.textContent = '';
        feedback.classList.remove('swipe-feedback--like', 'swipe-feedback--nope');
    }

    function showFeedback(message, type) {
        if (!feedback) {
            return;
        }

        feedback.textContent = message;
        feedback.classList.remove('swipe-feedback--like', 'swipe-feedback--nope');

        if (type === 'like') {
            feedback.classList.add('swipe-feedback--like');
        } else if (type === 'nope') {
            feedback.classList.add('swipe-feedback--nope');
        }
    }

    function createCard(member, index) {
        const card = document.createElement('article');
        card.className = 'profile-card';
        card.dataset.username = member.username;
        card.style.setProperty('--offset', (deck.length - 1) - index);
        card.tabIndex = -1;
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Відкрити профіль користувача ${member.name}`);
        card.dataset.dragging = 'false';

        const photoWrapper = document.createElement('div');
        photoWrapper.className = 'profile-card__photo';

        const photo = document.createElement('img');
        photo.src = member.avatar || defaultCardPhoto;
        photo.alt = `${member.name} — аватар`;
        photoWrapper.appendChild(photo);

        if (member.gender_display) {
            const badge = document.createElement('span');
            badge.className = 'profile-card__badge';
            badge.textContent = member.gender_display;
            photoWrapper.appendChild(badge);
        }

        const body = document.createElement('div');
        body.className = 'profile-card__body';

        const title = document.createElement('h2');
        title.className = 'profile-card__title';
        title.textContent = member.age ? `${member.name}, ${member.age}` : member.name;
        body.appendChild(title);

        const meta = document.createElement('div');
        meta.className = 'profile-card__meta';
        if (member.city || member.country) {
            const location = document.createElement('span');
            location.innerHTML = `<i class="bi bi-geo-alt"></i> ${[member.city, member.country].filter(Boolean).join(', ')}`;
            meta.appendChild(location);
        }
        if (member.gender_display) {
            const genderEl = document.createElement('span');
            genderEl.innerHTML = `<i class="bi bi-gender-ambiguous"></i> ${member.gender_display}`;
            meta.appendChild(genderEl);
        }
        body.appendChild(meta);

        const bio = document.createElement('p');
        bio.className = 'profile-card__bio';
        bio.textContent = member.bio || 'Користувач поки не поділився інформацією про себе.';
        body.appendChild(bio);

        const cta = document.createElement('div');
        cta.className = 'profile-card__cta';
        cta.innerHTML = '<span class="text-primary fw-semibold">Натисніть, щоб переглянути профіль</span>';
        body.appendChild(cta);

        card.appendChild(photoWrapper);
        card.appendChild(body);

        card.addEventListener('click', (event) => {
            if (card.dataset.dragging === 'true') {
                event.preventDefault();
                return;
            }

            window.location.href = `/members/profile/${member.username}`;
        });

        card.addEventListener('keydown', (event) => {
            if ((event.key === 'Enter' || event.key === ' ') && card.classList.contains('active')) {
                event.preventDefault();
                window.location.href = `/members/profile/${member.username}`;
            }
        });

        return card;
    }

    function renderDeck() {
        if (!cardStack) {
            return;
        }

        clearFeedback();
        cardStack.querySelectorAll('.profile-card').forEach((card) => card.remove());

        deck.forEach((member, index) => {
            const card = createCard(member, index);
            cardStack.appendChild(card);
        });

        requestAnimationFrame(() => {
            const cards = cardStack.querySelectorAll('.profile-card');
            cards.forEach((card, index) => {
                card.style.zIndex = index + 1;
            });
            setActiveCard();
            updateEmptyState();
            updateResultsCounter();
            updateControlsState();
        });
    }

    function updateControlsState() {
        const hasCards = deck.length > 0;
        if (likeButton) {
            likeButton.disabled = !hasCards;
        }
        if (dislikeButton) {
            dislikeButton.disabled = !hasCards;
        }
        if (rewindButton) {
            rewindButton.disabled = history.length === 0;
        }
    }

    function setActiveCard() {
        if (!cardStack) {
            return;
        }

        const cards = cardStack.querySelectorAll('.profile-card');
        cards.forEach((card) => {
            card.classList.remove('active', 'liked', 'dismissed');
            card.removeEventListener('pointerdown', onPointerDown);
            card.removeEventListener('mousedown', onMouseDown);
            card.removeEventListener('touchstart', onTouchStart);
            card.tabIndex = -1;
        });

        const nextCard = cards[cards.length - 1];

        if (activeCard && activeCard !== nextCard) {
            activeCard.removeEventListener('pointerdown', onPointerDown);
            activeCard.removeEventListener('mousedown', onMouseDown);
            activeCard.removeEventListener('touchstart', onTouchStart);
        }

        activeCard = nextCard || null;

        if (activeCard) {
            activeCard.classList.add('active');
            if (supportsPointerEvents) {
                activeCard.addEventListener('pointerdown', onPointerDown);
            } else {
                activeCard.addEventListener('mousedown', onMouseDown);
                activeCard.addEventListener('touchstart', onTouchStart, { passive: false });
            }
            activeCard.tabIndex = 0;
        } else {
            clearFeedback();
        }
    }

    function startDrag(startX, startY) {
        if (!activeCard) {
            return;
        }

        pointerStart = { x: startX, y: startY };
        activeCard.dataset.dragging = 'false';
        activeCard.style.transition = 'none';
    }

    function handleDragMove(currentX, currentY) {
        if (!activeCard || !pointerStart) {
            return;
        }

        const deltaX = currentX - pointerStart.x;
        const deltaY = currentY - pointerStart.y;
        const rotation = deltaX * 0.05;

        if (Math.abs(deltaX) > dragThreshold || Math.abs(deltaY) > dragThreshold) {
            activeCard.dataset.dragging = 'true';
        }

        activeCard.style.transform = `translate(${deltaX}px, ${deltaY}px) rotate(${rotation}deg)`;

        if (Math.abs(deltaX) > 40) {
            showFeedback(deltaX > 0 ? 'Супер! Свайп вправо' : 'Не моє. Свайп вліво', deltaX > 0 ? 'like' : 'nope');
        } else {
            clearFeedback();
        }
    }

    function resetActiveCardPosition() {
        if (!activeCard) {
            return;
        }

        activeCard.dataset.dragging = 'false';
        activeCard.style.transition = 'transform 0.3s ease';
        activeCard.style.transform = 'translate(0px, 0px) rotate(0deg)';
        activeCard.addEventListener('transitionend', () => {
            if (activeCard) {
                activeCard.style.transition = '';
            }
        }, { once: true });
        clearFeedback();
    }

    function handleDragEnd(endX) {
        if (!activeCard || !pointerStart) {
            return;
        }

        const deltaX = endX - pointerStart.x;
        const threshold = activeCard.offsetWidth * 0.35;

        pointerStart = null;

        if (Math.abs(deltaX) > threshold) {
            finalizeSwipe(deltaX > 0);
            return;
        }

        resetActiveCardPosition();
    }

    function onPointerDown(event) {
        if (!activeCard) {
            return;
        }

        if (event.pointerType === 'mouse' && event.button !== 0) {
            return;
        }

        startDrag(event.clientX, event.clientY);
        activeCard.setPointerCapture(event.pointerId);

        const onPointerMove = (moveEvent) => {
            handleDragMove(moveEvent.clientX, moveEvent.clientY);
        };

        const onPointerUp = (upEvent) => {
            if (activeCard) {
                activeCard.releasePointerCapture(upEvent.pointerId);
                activeCard.removeEventListener('pointermove', onPointerMove);
                activeCard.removeEventListener('pointerup', onPointerUp);
                activeCard.removeEventListener('pointercancel', onPointerUp);
            }

            handleDragEnd(upEvent.clientX);
        };

        activeCard.addEventListener('pointermove', onPointerMove);
        activeCard.addEventListener('pointerup', onPointerUp);
        activeCard.addEventListener('pointercancel', onPointerUp);
    }

    function onMouseDown(event) {
        if (!activeCard || event.button !== 0) {
            return;
        }

        startDrag(event.clientX, event.clientY);

        const onMouseMove = (moveEvent) => {
            handleDragMove(moveEvent.clientX, moveEvent.clientY);
        };

        const onMouseUp = (upEvent) => {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
            handleDragEnd(upEvent.clientX);
        };

        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
        event.preventDefault();
    }

    function onTouchStart(event) {
        if (!activeCard || event.touches.length === 0) {
            return;
        }

        const touch = event.touches[0];
        startDrag(touch.clientX, touch.clientY);

        const onTouchMove = (moveEvent) => {
            const moveTouch = moveEvent.touches[0];
            if (moveTouch) {
                handleDragMove(moveTouch.clientX, moveTouch.clientY);
            }
            moveEvent.preventDefault();
        };

        const onTouchEnd = (endEvent) => {
            document.removeEventListener('touchmove', onTouchMove, { passive: false });
            document.removeEventListener('touchend', onTouchEnd);
            document.removeEventListener('touchcancel', onTouchEnd);

            const changedTouch = endEvent.changedTouches[0];
            const endX = changedTouch ? changedTouch.clientX : touch.clientX;
            handleDragEnd(endX);
        };

        document.addEventListener('touchmove', onTouchMove, { passive: false });
        document.addEventListener('touchend', onTouchEnd);
        document.addEventListener('touchcancel', onTouchEnd);
        event.preventDefault();
    }

    function finalizeSwipe(isLike) {
        if (!activeCard || deck.length === 0) {
            return;
        }

        const card = activeCard;
        const removedMember = deck.pop();
        history.push({ member: removedMember, choice: isLike ? 'like' : 'nope' });

        pointerStart = null;

        const direction = isLike ? 1 : -1;
        card.classList.add(isLike ? 'liked' : 'dismissed');
        card.style.transition = 'transform 0.4s ease, opacity 0.4s ease';
        card.style.transform = `translate(${direction * (card.offsetWidth * 1.4)}px, -80px) rotate(${direction * 25}deg)`;
        card.style.opacity = '0';

        showFeedback(isLike ? 'Вподобали користувача' : 'Пропущено', isLike ? 'like' : 'nope');

        card.addEventListener('transitionend', () => {
            card.remove();
            activeCard = null;
            updateEmptyState();
            updateResultsCounter();
            updateControlsState();
            setActiveCard();
        }, { once: true });
    }

    function handleAction(isLike) {
        if (!cardStack) {
            return;
        }

        const card = cardStack.querySelector('.profile-card:last-child');
        if (!card) {
            return;
        }

        activeCard = card;
        finalizeSwipe(isLike);
    }

    function rewindLast() {
        if (history.length === 0) {
            return;
        }

        const last = history.pop();
        deck.push(last.member);
        showFeedback('Повернули картку', null);
        renderDeck();
    }

    function applyFilters() {
        const lookingFor = lookingForSelect ? lookingForSelect.value : 'any';
        const minAge = parseInt(minAgeInput ? minAgeInput.value : '', 10);
        const maxAge = parseInt(maxAgeInput ? maxAgeInput.value : '', 10);
        const countryId = countrySelect ? countrySelect.value : '';
        const cityId = citySelect ? citySelect.value : '';
        const maxDistance = parseInt(distanceInput ? distanceInput.value : '', 10);
        const unlimitedDistance = distanceInput ? parseInt(distanceInput.dataset.unlimitedValue || '', 10) : Number.NaN;
        const limitByDistance = distanceInput && !Number.isNaN(maxDistance) && (Number.isNaN(unlimitedDistance) || maxDistance < unlimitedDistance);
        const selectedInterests = Array.from(interestCheckboxes || [])
            .filter((checkbox) => checkbox.checked)
            .map((checkbox) => checkbox.value);

        filteredMembers = members.filter((member) => {
            if (lookingFor === 'female' && member.gender !== 'F') {
                return false;
            }
            if (lookingFor === 'male' && member.gender !== 'M') {
                return false;
            }
            if (countryId && String(member.country_id || '') !== countryId) {
                return false;
            }
            if (cityId && String(member.city_id || '') !== cityId) {
                return false;
            }
            if (limitByDistance && member.distance_km !== null && member.distance_km > maxDistance) {
                return false;
            }
            if (!Number.isNaN(minAge) && member.age !== null && member.age < minAge) {
                return false;
            }
            if (!Number.isNaN(maxAge) && member.age !== null && member.age > maxAge) {
                return false;
            }
            if (selectedInterests.length > 0) {
                const hasMatchingInterest = Array.isArray(member.interests)
                    && member.interests.some((interest) => selectedInterests.includes(interest));

                if (!hasMatchingInterest) {
                    return false;
                }
            }
            return true;
        });

        deck = filteredMembers.slice();
        history.length = 0;
        renderDeck();
    }

    function updateDistanceLabel() {
        if (!distanceInput || !distanceValue) {
            return;
        }

        const rawValue = parseInt(distanceInput.value, 10);
        const unlimitedValue = parseInt(distanceInput.dataset.unlimitedValue || '', 10);

        if (!Number.isNaN(unlimitedValue) && rawValue >= unlimitedValue) {
            distanceValue.textContent = 'Будь-яка';
            return;
        }

        if (Number.isNaN(rawValue)) {
            distanceValue.textContent = 'Будь-яка';
            return;
        }

        distanceValue.textContent = `до ${rawValue} км`;
    }

    function updateInterestChipsState() {
        (interestCheckboxes || []).forEach((checkbox) => {
            const chip = checkbox.closest('.discover-filters__chip');
            if (!chip) {
                return;
            }

            chip.classList.toggle('discover-filters__chip--checked', checkbox.checked);
        });
    }

    function getFocusableElements(container) {
        if (!container) {
            return [];
        }

        return Array.from(container.querySelectorAll('a[href], button:not([disabled]), textarea, input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'));
    }

    function closeFilters(options = {}) {
        const { restoreFocus = true } = options;

        if (filterPanel) {
            filterPanel.classList.remove('is-open');
            filterPanel.setAttribute('aria-hidden', 'true');
        }

        if (filterToggle) {
            filterToggle.setAttribute('aria-expanded', 'false');
        }

        if (filterOverlay) {
            filterOverlay.classList.remove('is-visible');
        }

        document.body.classList.remove('discover-filters-open');

        document.removeEventListener('keydown', handleFilterKeydown);

        if (restoreFocus && lastFocusedElement) {
            lastFocusedElement.focus({ preventScroll: true });
        }
    }

    function openFilters() {
        if (!filterPanel) {
            return;
        }

        lastFocusedElement = document.activeElement instanceof HTMLElement ? document.activeElement : null;

        filterPanel.classList.add('is-open');
        filterPanel.setAttribute('aria-hidden', 'false');

        if (filterToggle) {
            filterToggle.setAttribute('aria-expanded', 'true');
        }

        if (filterOverlay) {
            filterOverlay.classList.add('is-visible');
        }

        document.body.classList.add('discover-filters-open');

        const focusable = getFocusableElements(filterPanel);
        if (focusable.length > 0) {
            focusable[0].focus();
        }

        document.addEventListener('keydown', handleFilterKeydown);
    }

    function handleFilterKeydown(event) {
        if (event.key === 'Escape') {
            event.preventDefault();
            closeFilters();
            return;
        }

        if (event.key !== 'Tab' || !filterPanel || !filterPanel.classList.contains('is-open')) {
            return;
        }

        const focusable = getFocusableElements(filterPanel);
        if (focusable.length === 0) {
            return;
        }

        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault();
            last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault();
            first.focus();
        }
    }

    function resetFilters() {
        if (lookingForSelect) {
            lookingForSelect.value = 'any';
        }

        if (minAgeInput) {
            minAgeInput.value = '';
        }

        if (maxAgeInput) {
            maxAgeInput.value = '';
        }

        if (countrySelect) {
            countrySelect.value = '';
        }

        if (citySelect) {
            citySelect.innerHTML = '<option value="">Усі міста</option>';
            citySelect.disabled = true;
        }

        if (distanceInput) {
            const defaultValue = parseInt(distanceInput.dataset.defaultValue || distanceInput.max || '', 10);
            if (!Number.isNaN(defaultValue)) {
                distanceInput.value = String(defaultValue);
            } else {
                distanceInput.value = distanceInput.max || '';
            }
            updateDistanceLabel();
        }

        (interestCheckboxes || []).forEach((checkbox) => {
            checkbox.checked = false;
        });
        updateInterestChipsState();

        applyFilters();
    }

    function loadCities(countryId) {
        if (!citySelect) {
            return;
        }

        citySelect.innerHTML = '<option value="">Усі міста</option>';
        citySelect.disabled = !countryId;

        if (!countryId) {
            citySelect.dispatchEvent(new Event('change'));
            applyFilters();
            return;
        }

        fetch(`/members/edit-profile/get-cities/?country_id=${countryId}`)
            .then((response) => response.json())
            .then((cities) => {
                cities.forEach((city) => {
                    const option = document.createElement('option');
                    option.value = city.id;
                    option.textContent = city.name;
                    citySelect.appendChild(option);
                });
                citySelect.dispatchEvent(new Event('change'));
            })
            .catch(() => {
                showFeedback('Не вдалося завантажити міста', 'nope');
            });
    }

    if (likeButton) {
        likeButton.addEventListener('click', () => handleAction(true));
    }

    if (dislikeButton) {
        dislikeButton.addEventListener('click', () => handleAction(false));
    }

    if (rewindButton) {
        rewindButton.addEventListener('click', rewindLast);
    }

    if (lookingForSelect) {
        lookingForSelect.addEventListener('change', applyFilters);
    }

    if (minAgeInput) {
        minAgeInput.addEventListener('input', applyFilters);
    }

    if (maxAgeInput) {
        maxAgeInput.addEventListener('input', applyFilters);
    }

    if (countrySelect) {
        countrySelect.addEventListener('change', (event) => {
            loadCities(event.target.value);
        });
    }

    if (citySelect) {
        citySelect.addEventListener('change', applyFilters);
    }

    if (distanceInput) {
        distanceInput.addEventListener('input', () => {
            updateDistanceLabel();
            applyFilters();
        });
        updateDistanceLabel();
    }

    if (filterToggle) {
        filterToggle.addEventListener('click', () => {
            if (filterPanel && filterPanel.classList.contains('is-open')) {
                closeFilters();
            } else {
                openFilters();
            }
        });
    }

    if (filterOverlay) {
        filterOverlay.addEventListener('click', () => closeFilters());
    }

    if (filterCloseButtons && filterCloseButtons.length > 0) {
        filterCloseButtons.forEach((button) => {
            button.addEventListener('click', () => closeFilters());
        });
    }

    if (resetFiltersButton) {
        resetFiltersButton.addEventListener('click', resetFilters);
    }

    if (interestCheckboxes && interestCheckboxes.length > 0) {
        interestCheckboxes.forEach((checkbox) => {
            checkbox.addEventListener('change', () => {
                updateInterestChipsState();
                applyFilters();
            });
        });
        updateInterestChipsState();
    }

    renderDeck();
})();
