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
    if(not db.conferences(request.vars["conference"])):
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
        db.talks.which,
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.talks.topic,
        db.talks.description,
    ]
    
    proposals = SQLFORM.grid(
        ((db.talks.id_conference == request.vars['conference']) & (db.talks.status == 'unverified')),
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
    grid = SQLFORM.grid(
        ((db.talks.id_conference == request.vars['conference']) & (db.talks.status == 'accepted')),
        orderby=db.talks.which,
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
        sortable=False,
        links=[
             dict(
                 header='',
                 body=lambda row: A('up', _href=URL("sort", vars={'conference':request.vars['conference'],'talk':row.talks.id, 'direction':'up', 'index':row.talks.which}))
             ),
             dict(
                 header='',
                 body=lambda row: A('down', _href=URL("sort", vars={'conference':request.vars['conference'],'talk':row.talks.id, 'direction':'down', 'index':row.talks.which}))
             )
        ]
    )   

    return locals()

@auth.requires(auth.has_membership('user'))
def api():
    if len(request.args) < 3:
        session.flash('Wrong aruments')
        redirect(URL("conference", "view"))
    if(request.args(2) == "accepted"):
        last = db((db.talks.id_conference == request.args(0)) & (db.talks.status == "accepted")).select(db.talks.which.max())
        last = last[0]['MAX(talks.which)'] if (last[0]['MAX(talks.which)'] != None) else 0
        db(db.talks.id == request.args(1)).update(which=last + 1)
    db(db.talks.id == request.args(1)).update(status=request.args(2))
    session.flash = 'Talk proposal has been %s' % request.args(2)
    redirect(URL("conference", "schedule", vars={"conference": request.args(0)}))
    return locals()

@auth.requires(auth.has_membership('user'))
def sort():
    last = db((db.talks.id_conference == request.vars["conference"]) & (db.talks.status == "accepted")).select(db.talks.which.max())
    last = last[0]['MAX(talks.which)'] if (last[0]['MAX(talks.which)'] != None) else 0
    
    if((request.vars["direction"] == "up") and (request.vars["index"] != str(1))):
        db((db.talks.which == int(request.vars["index"])-1) & (db.talks.status == "accepted")).update(which = int(request.vars["index"]))
        db(db.talks.id == request.vars["talk"]).update(which=int(request.vars["index"])-1)

    if((request.vars["direction"] == "down") and (request.vars["index"] != str(last))):
        db((db.talks.which == int(request.vars["index"])+1) & (db.talks.status == "accepted")).update(which = int(request.vars["index"]))
        db(db.talks.id == request.vars["talk"]).update(which=int(request.vars["index"])+1)

    redirect(URL("schedule", vars={"conference":request.vars["conference"]}))
    return locals()