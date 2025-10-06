(function () {
    function selectMessagesList() {
        return document.querySelector('.dialog-messages');
    }

    function createElement(tag, className) {
        const element = document.createElement(tag);
        if (className) {
            element.className = className;
        }
        return element;
    }

    function selectDialogNavLink() {
        return document.querySelector('[data-dialog-link]');
    }

    function parseCounterValue(textContent) {
        const parsed = Number.parseInt(String(textContent || '').trim(), 10);
        return Number.isNaN(parsed) ? 0 : parsed;
    }

    function ensureNavCounter(link) {
        let counter = link.querySelector('[data-dialog-unread-counter]');
        if (!counter) {
            counter = document.createElement('span');
            counter.className = 'nav-counter';
            counter.setAttribute('aria-hidden', 'true');
            counter.dataset.dialogUnreadCounter = 'true';
            link.appendChild(counter);
        }
        return counter;
    }

    function ensureNavLabel(link) {
        let label = link.querySelector('[data-dialog-unread-label]');
        if (!label) {
            label = document.createElement('span');
            label.className = 'visually-hidden';
            label.dataset.dialogUnreadLabel = 'true';
            link.appendChild(label);
        }
        return label;
    }

    function setDialogNavUnreadCount(count) {
        const link = selectDialogNavLink();
        if (!link) {
            return;
        }

        const normalizedCount = Math.max(0, Number(count) || 0);
        if (normalizedCount === 0) {
            const counter = link.querySelector('[data-dialog-unread-counter]');
            const label = link.querySelector('[data-dialog-unread-label]');
            if (counter) {
                counter.remove();
            }
            if (label) {
                label.remove();
            }
            return;
        }

        const counter = ensureNavCounter(link);
        counter.textContent = String(normalizedCount);

        const label = ensureNavLabel(link);
        label.textContent = `Непрочитаних діалогів: ${normalizedCount}`;
    }

    function adjustDialogNavUnreadCount(delta) {
        const link = selectDialogNavLink();
        if (!link) {
            return;
        }

        const counter = link.querySelector('[data-dialog-unread-counter]');
        const current = counter ? parseCounterValue(counter.textContent) : 0;
        const next = Math.max(0, current + Number(delta || 0));
        setDialogNavUnreadCount(next);
    }

    function ensureDateSeparator(listElement, date, dateDisplay) {
        const selector = `.dialog-date-separator[data-date="${date}"]`;
        let separator = listElement.querySelector(selector);
        if (!separator) {
            separator = createElement('li', 'dialog-date-separator');
            separator.dataset.date = date;
            separator.setAttribute('aria-label', `Повідомлення за ${dateDisplay}`);
            const span = document.createElement('span');
            span.textContent = dateDisplay;
            separator.appendChild(span);
            listElement.appendChild(separator);
        }
        return separator;
    }

    function buildMessageElement(message, currentUserId) {
        const isCurrentUser = message.is_current_user ?? message.sender_id === currentUserId;
        const item = createElement('li', 'dialog-message-item');
        item.classList.add(isCurrentUser ? 'dialog-message-item-out' : 'dialog-message-item-in');
        item.dataset.messageId = String(message.id);
        item.dataset.senderId = String(message.sender_id);
        item.dataset.isCurrentUser = isCurrentUser ? 'true' : 'false';
        item.dataset.isRead = message.is_read ? 'true' : 'false';
        item.dataset.readDisplay = message.read_display || '';

        const main = createElement(
            'div',
            `dialog-message-main ${isCurrentUser ? 'dialog-message-main-out' : 'dialog-message-main-in'}`,
        );
        const bubble = createElement(
            'div',
            `dialog-message ${isCurrentUser ? 'dialog-message-out' : 'dialog-message-in'}`,
        );

        const author = createElement('span', 'dialog-message-author');
        author.textContent = message.author;
        const text = createElement('span', 'dialog-message-text');
        text.textContent = message.text;

        bubble.appendChild(author);
        bubble.appendChild(text);
        main.appendChild(bubble);
        item.appendChild(main);

        const meta = createElement(
            'div',
            `dialog-message-meta ${isCurrentUser ? 'dialog-message-meta-out' : 'dialog-message-meta-in'}`,
        );
        const time = createElement('span', 'dialog-message-time');
        time.textContent = message.time_display;
        meta.appendChild(time);

        if (isCurrentUser) {
            const icon = createElement('i', `bi ${message.is_read ? 'bi-check-all' : 'bi-check'}`);
            icon.setAttribute('aria-hidden', 'true');
            meta.appendChild(icon);

            const hidden = createElement('span', 'visually-hidden');
            hidden.textContent = message.is_read ? 'Повідомлення прочитано' : 'Повідомлення надіслано';
            meta.appendChild(hidden);
        }

        item.appendChild(meta);

        if (isCurrentUser && message.is_read) {
            const read = createElement('div', 'dialog-message-read');
            read.textContent = message.read_display ? `прочитано ${message.read_display}` : 'прочитано';
            item.appendChild(read);
        }

        return item;
    }

    function scrollToBottom(listElement) {
        listElement.scrollTop = listElement.scrollHeight;
    }

    function setupForm(form, { onMessage } = {}) {
        if (!form) {
            return;
        }

        const messageField = form.querySelector('[name="text"]');
        const submitButton = form.querySelector('button[type="submit"]');
        const errorContainer = form.querySelector('.dialog-form-errors');

        function setError(message) {
            if (!errorContainer) {
                return;
            }
            errorContainer.textContent = message || '';
        }

        form.addEventListener('submit', (event) => {
            event.preventDefault();
            if (!messageField) {
                return;
            }

            const text = messageField.value.trim();
            if (!text) {
                setError('Введіть повідомлення перед відправкою.');
                return;
            }

            setError('');

            if (submitButton) {
                submitButton.disabled = true;
            }

            const formData = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            })
                .then(async (response) => {
                    if (response.ok) {
                        return response.json();
                    }

                    let errorMessage = 'Не вдалося надіслати повідомлення.';
                    try {
                        const payload = await response.json();
                        const textErrors = payload?.errors?.text;
                        if (Array.isArray(textErrors) && textErrors.length) {
                            const firstError = textErrors[0];
                            if (firstError?.message) {
                                errorMessage = firstError.message;
                            }
                        }
                    } catch (error) {
                        // Ignore parsing errors and use the default message.
                    }

                    throw new Error(errorMessage);
                })
                .then((payload) => {
                    form.reset();
                    if (messageField instanceof HTMLTextAreaElement) {
                        messageField.value = '';
                    }
                    if (typeof onMessage === 'function' && payload && payload.message) {
                        onMessage(payload.message);
                    }
                })
                .catch((error) => {
                    setError(error.message);
                })
                .finally(() => {
                    if (submitButton) {
                        submitButton.disabled = false;
                    }
                });
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        const messagesList = selectMessagesList();
        if (!messagesList) {
            return;
        }

        const currentUserId = Number(messagesList.dataset.currentUserId || '0');
        const companionUsername = messagesList.dataset.companionUsername;
        const companionId = Number(messagesList.dataset.companionId || '0');

        if (!companionUsername || !currentUserId || !companionId) {
            return;
        }

        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const websocketUrl = `${protocol}://${window.location.host}/ws/dialogs/${companionUsername}/`;
        const websocket = new WebSocket(websocketUrl);

        const pendingReadIds = new Set();
        let socketOpen = false;

        function hasUnreadMessagesForDialog() {
            return Boolean(
                messagesList.querySelector(
                    '.dialog-message-item[data-is-current-user="false"][data-is-read="false"]',
                ),
            );
        }

        function sendPendingReadIds() {
            if (!socketOpen || pendingReadIds.size === 0) {
                return;
            }
            const ids = Array.from(pendingReadIds);
            pendingReadIds.clear();
            websocket.send(
                JSON.stringify({
                    action: 'mark_read',
                    message_ids: ids,
                }),
            );
        }

        function queueReadConfirmation(messageIds) {
            messageIds.forEach((id) => pendingReadIds.add(Number(id)));
            if (socketOpen) {
                sendPendingReadIds();
            }
        }

        function appendMessage(message) {
            ensureDateSeparator(messagesList, message.date, message.date_display);
            const element = buildMessageElement(message, currentUserId);
            messagesList.appendChild(element);
            scrollToBottom(messagesList);
            return element;
        }

        function handleNewMessage(message) {
            const enriched = {
                ...message,
                is_current_user: message.sender_id === currentUserId,
            };
            const element = appendMessage(enriched);
            if (!enriched.is_current_user) {
                queueReadConfirmation([enriched.id]);
            }
            return element;
        }

        function updateReadState(messageIds, readDisplay, readerId) {
            const hadUnreadBefore = hasUnreadMessagesForDialog();

            messageIds.forEach((id) => {
                const item = messagesList.querySelector(
                    `.dialog-message-item[data-message-id="${id}"]`,
                );
                if (!item) {
                    return;
                }

                item.dataset.isRead = 'true';
                item.dataset.readDisplay = readDisplay || '';

                if (item.dataset.isCurrentUser === 'true') {
                    const icon = item.querySelector('.dialog-message-meta i');
                    if (icon) {
                        icon.classList.remove('bi-check');
                        icon.classList.add('bi-check-all');
                    }

                    let readLabel = item.querySelector('.dialog-message-read');
                    if (!readLabel) {
                        readLabel = createElement('div', 'dialog-message-read');
                        item.appendChild(readLabel);
                    }
                    readLabel.textContent = readDisplay ? `прочитано ${readDisplay}` : 'прочитано';
                }
            });

            const hasUnreadAfter = hasUnreadMessagesForDialog();

            if (Number(readerId) === currentUserId && hadUnreadBefore && !hasUnreadAfter) {
                adjustDialogNavUnreadCount(-1);
            }
        }

        websocket.addEventListener('open', () => {
            socketOpen = true;
            sendPendingReadIds();
        });

        websocket.addEventListener('close', () => {
            socketOpen = false;
        });

        websocket.addEventListener('message', (event) => {
            let payload;
            try {
                payload = JSON.parse(event.data);
            } catch (error) {
                return;
            }

            if (payload.event === 'new' && payload.message) {
                handleNewMessage(payload.message);
            } else if (payload.event === 'read' && Array.isArray(payload.message_ids)) {
                updateReadState(
                    payload.message_ids.map(Number),
                    payload.read_display || '',
                    payload.reader_id,
                );
            }
        });

        const initialUnread = Array.from(
            messagesList.querySelectorAll(
                '.dialog-message-item[data-is-current-user="false"][data-is-read="false"]',
            ),
        ).map((element) => Number(element.dataset.messageId));

        if (initialUnread.length) {
            queueReadConfirmation(initialUnread);
        }

        const form = document.querySelector('.dialog-form');
        setupForm(form, { onMessage: handleNewMessage });

        scrollToBottom(messagesList);
    });
})();
