@auth.requires_membership('admin')
def index():
	return locals()