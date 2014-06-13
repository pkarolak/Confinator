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
	        links=[dict(header='Join it!', body=lambda row: A('Give a speech', _href=URL("conference", "join", vars={"conference":row.id})) )],
	        csv=False,
	    )
	return locals()

@auth.requires(auth.has_membership('user'))
def join():
	return locals()

@auth.requires(auth.has_membership('user'))
def new():
	return locals()

@auth.requires(auth.has_membership('user'))
def details():
	return locals()