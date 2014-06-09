@auth.requires(auth.has_membership('user'))
def lecture():
	return locals()