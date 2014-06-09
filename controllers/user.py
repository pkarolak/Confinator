@auth.requires_membership('user')
def index():
	return locals()