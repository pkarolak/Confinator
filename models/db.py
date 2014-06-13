db = DAL("sqlite://storage.sqlite")

response.generic_patterns = ['*'] if request.is_local else []
response.optimize_css = 'concat,minify,inline'
response.optimize_js = 'concat,minify,inline'
response.static_version = '1.0.0'

from gluon.tools import Auth, Crud, Mail
auth = Auth(db)
auth.define_tables(username=False)
crud = Crud(db)

auth.settings.extra_fields['auth_user'] = (
    [Field('user_type', requires=IS_IN_SET(['admin', 'user']))]
)

auth.settings.login_next = URL('index')
auth.settings.register_next = URL('user', args='login')
auth.settings.register_onaccept.append(lambda form: auth.add_membership('user', db(db.auth_user.email == form.vars.email).select().first().id))

auth.settings.create_user_groups = False
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = False

# db.define_table(
#     'conference_halls',
#     Field('name'),
#     Field('address', length=128, requires=[IS_NOT_EMPTY()]),
#     Field('city', length=128, requires=[IS_NOT_EMPTY(), IS_ALPHANUMERIC(error_message='Alphanumeric only')]),
#     Field('zip', length=8, requires=[IS_NOT_EMPTY(), IS_MATCH('^\d{2}-\d{3}?$', error_message='Wrong code format')]),
#     format = '%(name)s, %(city)s',
# )
db.auth_user._format = "%(first_name)s %(last_name)s"
db.define_table(
    'conferences',
    Field('name'),
    # Field('location', db.conference_halls),
    Field('time', 'datetime'),
    Field('organiser', 'reference auth_user'),
)

db.define_table(
    'talks',
    Field('topic', length=100, requires=[IS_NOT_EMPTY()]),
    Field('description', requires=[IS_NOT_EMPTY()]),
    Field('id_conference', 'reference conferences'),
    Field('id_speaker', 'reference auth_user'),
)


db.define_table(
    'schedule',
    Field('hour', requires=[IS_NOT_EMPTY()]),
    Field('duration', 'integer', requires=[IS_INT_IN_RANGE(15, 90)]),
    Field('talk', 'reference talks')
)

mail = Mail()
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login
auth.settings.mailer = mail