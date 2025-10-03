PREV_PAGE_KEY = 'posts/prev_page'

def set_prev_page(session, value):
    prev_page = session.get(PREV_PAGE_KEY, "")

    session[PREV_PAGE_KEY] = value

def get_prev_page(session):
    prev_page = session.get(PREV_PAGE_KEY, "")

    if prev_page:
        return prev_page
    else:
        return "/"