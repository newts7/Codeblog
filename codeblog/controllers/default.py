def index():
    rows=db(db.blog_post).select(orderby=db.blog_post.title.upper())
    return locals()

@auth.requires_login()
def create():
    form=SQLFORM(db.blog_post).process()
    if form.accepted:
        session.flash="Posted!"
        redirect(URL('index'))
    return locals()

@auth.requires_login()
def show():
    post=db.blog_post(request.args(0,cast=int))
    db.blog_comment.blog_post.default=post.id
    db.blog_comment.blog_post.writable=False
    db.blog_comment.blog_post.readable=False
    form=SQLFORM(db.blog_comment).process()
    comments=db(db.blog_comment.blog_post==post.id).select()
    return locals()

@auth.requires_membership('managers')
def manage():
    grid=SQLFORM.grid(db.blog_post)
    return locals()

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


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
