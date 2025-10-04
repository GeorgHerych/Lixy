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
    const activeProfile = document.querySelector('[data-active-profile]');
    const activeAvatar = document.querySelector('[data-active-avatar]');
    const activeName = document.querySelector('[data-active-name]');
    const activeMeta = document.querySelector('[data-active-meta]');
    const lookingForSelect = document.querySelector('[data-looking-for]');
    const minAgeInput = document.querySelector('[data-min-age]');
    const maxAgeInput = document.querySelector('[data-max-age]');
    const countrySelect = document.querySelector('[data-country]');
    const citySelect = document.querySelector('[data-city]');
    const resultsCounter = document.querySelector('[data-results-count]');

    let filteredMembers = members.slice();
    let deck = filteredMembers.slice();
    const history = [];
    let activeCard = null;
    let pointerStart = null;
    const defaultAvatar = 'https://placehold.co/96x96?text=L';

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

    function formatActiveMeta(member) {
        const parts = [];

        if (member.age) {
            parts.push(`${member.age} років`);
        }

        const location = [member.city, member.country].filter(Boolean).join(', ');
        if (location) {
            parts.push(location);
        }

        if (member.gender_display) {
            parts.push(member.gender_display);
        }

        return parts.join(' • ');
    }

    function updateActiveProfile(member) {
        if (!activeProfile) {
            return;
        }

        if (!member) {
            activeProfile.classList.add('d-none');
            return;
        }

        if (activeAvatar) {
            activeAvatar.src = member.avatar || defaultAvatar;
            activeAvatar.alt = `${member.name} — аватар`;
        }

        if (activeName) {
            activeName.textContent = member.name;
        }

        if (activeMeta) {
            const metaText = formatActiveMeta(member);
            activeMeta.textContent = metaText;
            activeMeta.classList.toggle('d-none', metaText === '');
        }

        activeProfile.classList.remove('d-none');
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

        const media = document.createElement('div');
        media.className = 'profile-card__media';

        const img = document.createElement('img');
        img.src = member.banner || member.avatar || 'https://placehold.co/600x800?text=Lixy';
        img.alt = `${member.name} — фото профілю`;
        media.appendChild(img);

        if (member.gender_display) {
            const badge = document.createElement('span');
            badge.className = 'profile-card__badge';
            badge.textContent = member.gender_display;
            media.appendChild(badge);
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

        const footer = document.createElement('div');
        footer.className = 'profile-card__footer';
        const profileLink = document.createElement('a');
        profileLink.className = 'btn btn-outline-primary';
        profileLink.href = `/members/profile/${member.username}`;
        profileLink.textContent = 'Дивитися профіль';
        footer.appendChild(profileLink);
        body.appendChild(footer);

        card.appendChild(media);
        card.appendChild(body);

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
        });

        const nextCard = cards[cards.length - 1];

        if (activeCard && activeCard !== nextCard) {
            activeCard.removeEventListener('pointerdown', onPointerDown);
        }

        activeCard = nextCard || null;

        const activeMember = deck[deck.length - 1] || null;

        if (activeCard) {
            activeCard.classList.add('active');
            activeCard.addEventListener('pointerdown', onPointerDown);
        } else {
            clearFeedback();
        }

        updateActiveProfile(activeMember);
    }

    function onPointerDown(event) {
        if (!activeCard) {
            return;
        }

        pointerStart = { x: event.clientX, y: event.clientY };
        activeCard.setPointerCapture(event.pointerId);
        activeCard.style.transition = 'none';

        const onPointerMove = (moveEvent) => {
            if (!activeCard || !pointerStart) {
                return;
            }

            const deltaX = moveEvent.clientX - pointerStart.x;
            const deltaY = moveEvent.clientY - pointerStart.y;
            const rotation = deltaX * 0.05;

            activeCard.style.transform = `translate(${deltaX}px, ${deltaY}px) rotate(${rotation}deg)`;

            if (Math.abs(deltaX) > 40) {
                showFeedback(deltaX > 0 ? 'Супер! Свайп вправо' : 'Не моє. Свайп вліво', deltaX > 0 ? 'like' : 'nope');
            } else {
                clearFeedback();
            }
        };

        const onPointerUp = (upEvent) => {
            if (!activeCard || !pointerStart) {
                return;
            }

            activeCard.releasePointerCapture(upEvent.pointerId);
            activeCard.removeEventListener('pointermove', onPointerMove);
            activeCard.removeEventListener('pointerup', onPointerUp);
            activeCard.removeEventListener('pointercancel', onPointerUp);

            const deltaX = upEvent.clientX - pointerStart.x;
            const deltaY = upEvent.clientY - pointerStart.y;
            const threshold = activeCard.offsetWidth * 0.35;

            pointerStart = null;

            if (Math.abs(deltaX) > threshold) {
                finalizeSwipe(deltaX > 0);
            } else {
                activeCard.style.transition = 'transform 0.3s ease';
                activeCard.style.transform = 'translate(0px, 0px) rotate(0deg)';
                activeCard.addEventListener('transitionend', () => {
                    if (activeCard) {
                        activeCard.style.transition = '';
                    }
                }, { once: true });
                clearFeedback();
            }
        };

        activeCard.addEventListener('pointermove', onPointerMove);
        activeCard.addEventListener('pointerup', onPointerUp);
        activeCard.addEventListener('pointercancel', onPointerUp);
    }

    function finalizeSwipe(isLike) {
        if (!activeCard || deck.length === 0) {
            return;
        }

        const card = activeCard;
        const removedMember = deck.pop();
        history.push({ member: removedMember, choice: isLike ? 'like' : 'nope' });

        updateActiveProfile(deck[deck.length - 1] || null);

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
            if (!Number.isNaN(minAge) && member.age !== null && member.age < minAge) {
                return false;
            }
            if (!Number.isNaN(maxAge) && member.age !== null && member.age > maxAge) {
                return false;
            }
            return true;
        });

        deck = filteredMembers.slice();
        history.length = 0;
        renderDeck();
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

    renderDeck();
})();
