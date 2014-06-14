@auth.requires(auth.has_membership('user'))
def view():
    message = "Welcome to your kingdom! Manage your existing conferences or add a new one if you want."
    grid = SQLFORM.grid(
        db.conferences.organiser == auth.user_id,
        fields=[db.conferences.name, db.conferences.time],
        user_signature=False,
        editable=False,
        deletable=False,
        details=False,
        create=False,
        searchable=False,
        links=[
            dict(
                header='', 
                body=lambda row: A('Edit details', _href=URL("conference", "details", vars={"conference":row.id})) 
            ),
            dict(
                header='', 
                body=lambda row: A('Manage schedule', _href=URL("conference", "schedule", vars={"conference":row.id})) 
            ),
        ],
        csv=False,
        maxtextlength=200,
        
    )
    return locals()

@auth.requires(auth.has_membership('user'))
def list():
    message = "Just look how many conferences are looking for a brilliant speaker!"
    grid = SQLFORM.grid(
        db.conferences,
        fields=[db.conferences.name, db.conferences.time, db.conferences.organiser],
        user_signature=False,
        editable=False,
        deletable=False,
        details=False,
        create=False,
        links=[
                dict(header='', body=lambda row: A('Give a speech', _href=URL("lecture", "new", vars={"conference":row.id})) ),
                dict(header='', body=lambda row: A('See agenda', _href=URL("agenda", vars={"conference":row.id})) ),
            ],
        csv=False,
        maxtextlength=200,
    )
    return locals()

@auth.requires(auth.has_membership('user'))
def new():
    db.conferences.organiser.writable = False
    db.conferences.organiser.default = auth.user.id
    crud.settings.create_next = URL('view')
    grid = crud.create(
            db.conferences,
        )
    return locals()

@auth.requires(auth.has_membership('user'))
def agenda():
    if(not db.conferences(request.vars["conference"]) or (db.conferences(request.vars["conference"]).organiser != auth.user.id)):
        redirect(URL("privilages","error"))
    return locals()

@auth.requires(auth.has_membership('user'))
def details():
    if(not db.conferences(request.vars["conference"]) or (db.conferences(request.vars["conference"]).organiser != auth.user.id)):
        redirect(URL("privilages","goaway"))
    db.conferences.organiser.writable = False
    crud.settings.update_next = URL('view')
    crud.settings.update_deletable = False
    grid = crud.update(db.conferences, request.vars["conference"])
    return locals()

@auth.requires(auth.has_membership('user'))
def schedule():
    fields = [
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.talks.topic,
        db.talks.description,
    ]
    
    proposals = SQLFORM.grid(db.talks.id_conference == request.vars['conference'] and db.talks.status == 'unverified',
        user_signature=False,
        editable=False,
        deletable=False,
        details=False,
        create=False,
        csv=False,
        searchable=False,
        left=db.talks.on(db.auth_user.id == db.talks.id_speaker),
        fields=fields,
        maxtextlength=200,
        links=[
            dict(
                header='',
                body=lambda row: A('Accept', _href=URL("api", args=[request.vars['conference'], row.talks.id, 'accepted']))
            ),
            dict(
                header='',
                body=lambda row: A('Reject', _href=URL("api", args=[request.vars['conference'], row.talks.id, 'rejected']))
            )
        ]
    )   

    # TODO ustawianie agendy
    grid = SQLFORM.grid(db.talks.id_conference == request.vars['conference'] and db.talks.status == 'accepted',
        user_signature=False,
        editable=False,
        deletable=False,
        details=False,
        create=False,
        csv=False,
        searchable=False,
        left=db.talks.on(db.auth_user.id == db.talks.id_speaker),
        fields=fields,
        maxtextlength=200,
        links=[
            # dict(
            #     header='',
            #     body=lambda row: A('Accept', _href=URL("api", args=[request.vars['conference'], row.talks.id, 'accepted']))
            # ),
            # dict(
            #     header='',
            #     body=lambda row: A('Reject', _href=URL("api", args=[request.vars['conference'], row.talks.id, 'rejected']))
            # )
        ]
    )   

    return locals()

@auth.requires(auth.has_membership('user'))
def api():
    if len(request.args) < 3:
        session.flash('Wrong aruments')
        redirect(URL("conference", "view"))
    db(db.talks.id == request.args(1)).update(status=request.args(2))
    session.flash = 'Talk proposal has been %s' % request.args(2)
    redirect(URL("conference", "schedule", vars={"conference": request.args(0)}))
    return locals()
