# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

 
@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome %s" %auth.user.username)
    formpr = SQLFORM(db.search_pr, submit_button='search')
    if formpr.process().accepted: 
        redirect(URL("default","professor",args=[formpr.vars.Name]))
    formcr = SQLFORM(db.search_course, submit_button='search')
    if formcr.process().accepted: 
        redirect(URL("default","course",args=[formcr.vars.Title]))
    return dict(formpr=formpr, formcr=formcr, message=T('Hello World'))



@auth.requires_login()
def rateC_update(form):
    boo = 0
    form.vars.name=form.vars.Title
    courses = db(db.Course_data.Title==form.vars.Title).select()
    for course in courses:
        if course.Title==form.vars.Title:
            boo = boo + 1
            return
    
    db.Course_data.insert(Title=form.vars.Title, name=form.vars.Title)
    return

@auth.requires_login()
def rate_course():
    form = SQLFORM(db.Course_rate)
    if form.process(onvalidation=rateC_update).accepted: 
        redirect(URL("default","course",args=[form.vars.Title]))
    return dict(form=form)

@auth.requires_login()
def rateP_update(form):
    boo = 0
    form.vars.Title=form.vars.Name
    profs = db(db.Prof_data.name==form.vars.Name).select()
    for prof in profs:
        if prof.name==form.vars.Name:
            boo = boo + 1
            return
    
    db.Prof_data.insert(Title=form.vars.Name, name=form.vars.Name)
    return
    
@auth.requires_login()
def rate_professor():
    form = SQLFORM(db.Prof_rate)
    if form.process(onvalidation=rateP_update).accepted:
        redirect(URL("default", "professor", args=[form.vars.Name]))
    return dict(form=form)

@auth.requires_login()
def all_courses():
    courses = db().select(db.course.ALL, orderby=db.course.name)
    return dict(courses=courses)

@auth.requires_login()
def all_professors():
    profs = db().select(db.pr.ALL, orderby=db.pr.name)
    return dict(profs=profs)

@auth.requires_login()
def course():
    courses=db.course(request.args(0, cast=int)) or redirect(URL('all_courses'))
    everythings = db().select(db.Course_data.ALL)
    db.Course_data.name.default=courses.id
    db.Course_data.Title.default=courses.id
    rates = db(db.Course_rate.name==courses.id).select()
    comp_sum = 0
    easiness_sum = 0
    struggle_sum = 0
    rela_sum = 0
    counter_sum = 0
    for rate in rates:
        comp_sum= float(comp_sum) + float(rate.Comprehensibility)
        easiness_sum = float(easiness_sum) + float(rate.Easiness)
        struggle_sum = float(struggle_sum) + float(rate.Struggle_Level)
        rela_sum = float(rela_sum) + float(rate.Relativity)
        counter_sum = float(counter_sum) + float(rate.Counter)
    boolean = 0
    
    for everything in everythings:
        if everything.name==courses.id:
            boolean = 1
            
    if boolean==1:
        db(db.Course_data.Title==courses.id).update(Counter = counter_sum)
        db(db.Course_data.Title==courses.id).update(Total_Comprehensibility = comp_sum)
        db(db.Course_data.Title==courses.id).update(Total_Easiness = easiness_sum)
        db(db.Course_data.Title==courses.id).update(Total_Struggle_Level = struggle_sum)
        db(db.Course_data.Title==courses.id).update(Total_Relativity = rela_sum)
        db(db.Course_data.Title==courses.id).update(Avg_Comprehensibility = comp_sum/counter_sum)
        db(db.Course_data.Title==courses.id).update(Avg_Easiness = easiness_sum/counter_sum)
        db(db.Course_data.Title==courses.id).update(Avg_Struggle_Level = struggle_sum/counter_sum)
        db(db.Course_data.Title==courses.id).update(Avg_Relativity = rela_sum/counter_sum) 
        
    Course_data=db(db.Course_data.name==courses.id).select()
    db.comments.Course_name.default = courses.id
    db.comments.Username.default=auth.user.username
    form=SQLFORM(db.comments)
    if form.process().accepted:
        response.flash='Your comment is posted'
    comments=db(db.comments.Course_name==courses.id).select()
    return dict(courses=courses, message = T('true'), comments=comments, form=form, Course_data=Course_data)

@auth.requires_login()
def professor():
    professor=db.pr(request.args(0, cast=int)) or redirect(URL('all_professors'))
    everythings = db().select(db.Prof_data.ALL)
    db.Prof_data.name.default=professor.id
    db.Prof_data.Title.default=professor.id
    rates = db(db.Prof_rate.Name==professor.id).select()
    Clarity_sum = 0
    Easiness_sum = 0
    Workload_sum = 0
    Helpfulness_sum = 0
    counter_sum = 0
    for rate in rates:
        Clarity_sum = float(Clarity_sum) + float(rate.Clarity)
        Easiness_sum = float(Easiness_sum) + float(rate.Easiness)
        Workload_sum = float(Workload_sum) + float(rate.Workload)
        Helpfulness_sum = float(Helpfulness_sum) + float(rate.Helpfulness)
        counter_sum = float(counter_sum) + float(rate.Counter)
    boolean = 0
    
    for everything in everythings:
        if everything.name==professor.id:
            boolean = 1
            
    if boolean==1:
        db(db.Prof_data.Title==professor.id).update(Counter = counter_sum)
        db(db.Prof_data.Title==professor.id).update(Total_Clarity = Clarity_sum)
        db(db.Prof_data.Title==professor.id).update(Avg_Clarity = Clarity_sum/counter_sum)
        db(db.Prof_data.Title==professor.id).update(Total_Easiness = Easiness_sum)
        db(db.Prof_data.Title==professor.id).update(Avg_Easiness = Easiness_sum/counter_sum)
        db(db.Prof_data.Title==professor.id).update(Total_Workload = Workload_sum)
        db(db.Prof_data.Title==professor.id).update(Avg_Workload = Workload_sum/counter_sum)
        db(db.Prof_data.Title==professor.id).update(Total_Helpfulness = Helpfulness_sum)
        db(db.Prof_data.Title==professor.id).update(Avg_Helpfulness = Helpfulness_sum/counter_sum)
    
    Prof_data = db(db.Prof_data.name==professor.id).select()
    db.comments.Professor_name.default=professor.id
    db.comments.Username.default=auth.user.username
    form=SQLFORM(db.comments)
    if form.process().accepted:
        response.flash = 'Your comment is posted'
    comments = db(db.comments.Professor_name==professor.id).select()
    return dict(professor=professor, message = T('true'), comments=comments, form=form, Prof_data=Prof_data)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
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


def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
