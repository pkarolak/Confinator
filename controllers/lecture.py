@auth.requires(auth.has_membership('user'))
def view():
	return locals()