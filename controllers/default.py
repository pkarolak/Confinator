# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    if(auth.has_membership('admin')):
        redirect(URL('admin', 'index'))
    if(auth.has_membership('user')):
        redirect(URL('user', 'index'))
    
def user():
    return dict(form=auth())
