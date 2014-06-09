db = DAL("sqlite://storage.sqlite")

response.generic_patterns = ['*'] if request.is_local else []
response.optimize_css = 'concat,minify,inline'
response.optimize_js = 'concat,minify,inline'
response.static_version = '1.0.0'

from gluon.tools import Auth, Crud
auth = Auth(db)
auth.define_tables(username=True)
crud = Crud(db)

auth.settings.extra_fields['auth_user'] = (
    [Field('user_type', requires=IS_IN_SET(['admin', 'user']))]
)

auth.settings.login_next = URL('index')
auth.settings.register_next = URL('user', args='login')
auth.settings.register_onaccept.append(lambda form: auth.add_membership('user', db(db.auth_user.email == form.vars.email).select().first().id))



db.define_table(
    'conference_halls',
    Field('name'),
    Field('address', length=128, requires=[IS_NOT_EMPTY()]),
    Field('city', length=128, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(error_message='Alphanumeric only')]),
    Field('zip', length=8, requires=[IS_NOT_EMPTY(), IS_MATCH('^\d{2}-\d{3}?$', error_message='Wrong code format')]),
    format = '%(name)s, %(city)s',
)

db.define_table(
    'conferences',
    Field('name'),
    Field('location', db.conference_halls),
    Field('time'),
    Field('organiser', db.auth_user),
)


db.define_table(
    'lectures',
    Field('topic'),
    Field('conference', db.conferences),
    Field('lecturer', db.auth_user),
)
