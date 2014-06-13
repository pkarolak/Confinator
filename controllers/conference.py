@auth.requires(auth.has_membership('user'))
def view():
	if (request.vars["owner"]):
		message = "Welcome to your kingdom! Manage your existing conferences or add a new one if you want."
		grid = SQLFORM.grid(
			db.conferences.organiser == request.vars["owner"],
			fields=[db.conferences.name, db.conferences.time],
	        user_signature=False,
	        editable=False,
	        deletable=False,
	        details=False,
	        create=False,
	        searchable=False,
	        links=[dict(header='Wanna more info?', body=lambda row: A('Show me!', _href=URL("conference", "details", vars={"conference":row.id})) )],
	        csv=False,
	        maxtextlength=200,
	        
	    )
	else:
		message = "Just look how many conferences are looking for a brilliant speaker!"
		grid = SQLFORM.grid(
			db.conferences,
			fields=[db.conferences.name, db.conferences.time, db.conferences.organiser],
	        user_signature=False,
	        editable=False,
	        deletable=False,
	        details=False,
	        create=False,
	        links=[dict(header='Join it!', body=lambda row: A('Give a speech', _href=URL("lecture", "new", vars={"conference":row.id})) )],
	        csv=False,
	        maxtextlength=200,
	    )
	return locals()


@auth.requires(auth.has_membership('user'))
def new():
	db.conferences.organiser.writable = False
	db.conferences.organiser.default = auth.user.id
	crud.settings.create_next = URL('view', vars={"owner": auth.user.id})
	grid = crud.create(
			db.conferences,
		)
	return locals()

@auth.requires(auth.has_membership('user'))
def details():
	return locals()