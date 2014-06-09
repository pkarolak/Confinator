response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

response.menu = []

if auth.user:
    if auth.has_membership("admin"):
        response.menu = [
            #(<NAME>, False, URL(<Controller>, <Action>)),
        ]
    elif auth.has_membership("user"):
        response.menu = [
            ('Conferences', False, URL('conference', 'conference', args=[auth.user.id])),
            ('Lectures', False, URL('lecture', 'lecture', args=[auth.user.id])),
        ]
