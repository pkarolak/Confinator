@auth.requires(auth.has_membership('user'))
def conference():
	return locals()