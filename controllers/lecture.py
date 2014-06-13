@auth.requires(auth.has_membership('user'))
def view():
	return locals()

@auth.requires(auth.has_membership('user'))
def new():
	if(not request.vars["conference"]):
		redirect(URL("conference", "view", vars={"owner":auth.user.id}))
	db.talks.id_speaker.writable = False
	db.talks.id_speaker.default = auth.user.id
	db.talks.id_conference.writable = False
	db.talks.id_conference.default = request.vars["conference"]
	crud.settings.create_next = URL('lecture','view', vars={"owner": auth.user.id})
	grid = crud.create(db.talks)
	return locals()

@auth.requires(auth.has_membership('user'))
def view():
	query = (db.talks.id_speaker == auth.user.id)
	fields = [
				db.talks.topic,
				db.talks.description,
				db.conferences.name,
				db.conferences.time,
			]
	left = [db.talks.on(db.conferences.id == db.talks.id_conference)]
	grid = SQLFORM.grid(query, fields=fields, left=left,
 			user_signature=False,
 			maxtextlength=200,
	        editable=False,
	        deletable=False,
	        details=False,
	        create=False,
	        csv=False,
	        searchable=False,
	    )
	return locals()