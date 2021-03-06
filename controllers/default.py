# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

@auth.requires_login()
def myr():
    return dict()

@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict(message=T('Welcome to web2py!'))

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@auth.requires_login()
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@auth.requires_login()
def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def clicking():
    this=db.employee(request.args(0,cast=int)) or redirect(URL('default','index'))
    form=db(db.employee.id==this.id).select()
    return dict(form=form)

def show():
	this_page = db.employee(request.args(0,cast=int)) or redirect(URL('index'))
	recipeid = this_page.id
	form = SQLFORM(db.comments).process()
	db(form.vars.id == db.comments.id).update(recipe_id=recipeid)
	comments = db(recipeid == db.comments.recipe_id).select(db.comments.ALL)
	query = (auth.user_id == db.likez.liked_by)&(recipeid == db.likez.recipe_id)
	likes = db(query).select(db.likez.ALL) or 0
	if likes == 0:
		likes = 1
	else:
		likes = 2
	edit=0
	if auth.user_id == this_page.Author:
		edit = 1
	return dict(page=this_page,comments=comments,form=form,likes=likes,edit=edit)
@auth.requires_login()
def likez():
    this.page = db.employee(request.args(0,cast=int)) or redirect(URL('index'))
    db.likez.insert(recipe_id=this_page.id,liked_by=auth.user_id)
    
    redirect(URL('show',args=this_page.id))

@auth.requires_login()
def unlike():
    this_page=db.employee(request.args(0,cast=int))or redirect(URL('index'))
    query=(auth.user_id == db.likez.liked_by)&(this_page.id == db.likez.recipe_id)
    db(query).delete()
    redirect(URL('show',args=this_page.id))


@auth.requires_login()
def display_form():
   form = SQLFORM(db.person)

@auth.requires_login()
def upload():
   form = SQLFORM(db.employee, fields=['name','descr','recipe','image'])
   if form.process().accepted:
        session.flash = 'form accepted'
   return dict(form=form)
