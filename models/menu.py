response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

response.menu = []

if auth.user:
    if auth.has_membership("admin"):
        response.menu = [
            ('Conferences', False, URL('conference', 'conference')),
            ('Lectures', False, URL('lecture', 'lecture')),
        ]
    elif auth.has_membership("user"):
        response.menu = [
            ('Conferences', False, URL('conference', 'conference')),
            ('Lectures', False, URL('lecture', 'lecture')),
        ]
