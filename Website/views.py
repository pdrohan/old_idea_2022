#Here we will store all of the route users can go to
#Liek thehome page - login pages goes to auth
from .models import User, Note, Notetype, Role, Coach, Team
from flask import Blueprint, render_template
from flask import request, redirect, url_for, render_template, flash, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from flask_admin import Admin
from flask_user import roles_required
from flask_admin.contrib.sqla import ModelView
from flask import Flask

views = Blueprint('views', __name__)



#Nameing concention is @ then the name of your blueprint
@views.route('/')
@roles_required('Admin')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/playerprofile')
@login_required
def playerprofile():
    return render_template("profile_with_data_and_skills.html", user=current_user)

@views.route('/updateinfo', methods=['Get', 'Post'])
@login_required
def updateinfo():
    if request.method == "POST":
        height = request.form.get('height')
        weight = request.form.get("weight")
        shootDir = request.form.get('shootDir')
        position = request.form.get('position')
        #data = Rating.query.filter_by()
        cur_user = flask_login.current_user
        flash('we here')
        new_info = current_user(height=height, weight=weight, shootDir=shootDir, position=position)
        db.session.add(new_info)
        db.session.commit()
        flash('Player information updated!', category='success')# Add them to database
        #return redirect(url_for('views.home'))
        return redirect(url_for('views.home'))
    return render_template('player_info_input.html', user =current_user)

@views.route('/test', methods=['Get', 'Post'])
@login_required
def testing():
    if request.method == "POST":
        #Add constraints for
        height = request.form.get('height')
        weight = request.form.get('weight')
        if height is None:
            flash("proper height", category='success')
        else:
            flash("Thank you for updating your player Info", category='success')
            new_userdata = User.query.filter_by(id=User.get_id(current_user)).update(dict(weight=weight, height=height))
            db.session.commit()
            return redirect(url_for('views.home'))

    return render_template("test.html", user=current_user)

@views.route('/goals', methods=['Get', 'Post'])
@login_required
def goals_input():
    if request.method == "POST":
        yearlyGoalsData = request.form.get('yearlyGoals')
        yearlyPlanData = request.form.get('yearlyPlan')
        longGoalsData = request.form.get('longGoals')
        longPlanData = request.form.get('longPlan')
        cur_user_id = int(User.get_id(current_user))
        yearlygoalsNoteId = Notetype.query.filter_by(id=1).first()
        yearlyplanNoteId = Notetype.query.filter_by(id=2).first()
        longGoalsDataId = Notetype.query.filter_by(id=3).first()
        longPlanDataId = Notetype.query.filter_by(id=4).first()
        if yearlyGoalsData is None:
            flash("Add to your Yearly Goals", category='error')
        if yearlyPlanData is None:
            flash("Add to your Execution Plan", category='error')
        if longGoalsData is None:
            flash("Add to your 5 year Plan", category='error')
        if longPlanData is None:
            flash("Add to your 5 year Execution Plan", category='error')
        else:
            flash("Thank you for Adding to your Goals! Your Coach can now review your input", category='success')
            yearlyGoals = Note(data=yearlyGoalsData, userId=cur_user_id, noteTypeId=yearlygoalsNoteId.id)
            yearlyPlan = Note(data=yearlyGoalsData, userId=cur_user_id, noteTypeId=yearlyplanNoteId.id)
            longGoals = Note(data=yearlyGoalsData, userId=cur_user_id, noteTypeId=longGoalsDataId.id)
            longPlan = Note(data=yearlyGoalsData, userId=cur_user_id, noteTypeId=longPlanDataId.id)
            db.session.add(yearlyGoals)
            db.session.add(yearlyPlan)
            db.session.add(longGoals)
            db.session.add(longPlan)
            db.session.commit()
            return redirect(url_for('views.playerprofile'))
    return render_template("goals_input.html", user=current_user)

@views.route('/noteinput', methods=['Get', 'Post'])
#@roles_required('Admin')
@login_required
def notetypeinput():
    if request.method == "POST":
        noteName = request.form.get('noteName')
        if len(noteName) < 1:
            flash('Please add a proper Note Type', category='error')
        else:
            new_note = Notetype()
            new_note.name = request.form.get('noteName')
            db.session.add(new_note)
            db.session.commit()
            print(new_note.name)
            flash(noteName, category='success')  # Add them to database
    return render_template("note_type_input.html", user=current_user)

# @views.route('/test1', methods=['Get', 'Post'])
# @login_required
# def tryit():
#     val = Notetype.query.filter_by(id=3).first()
#     val2 = Note.query.filter_by(id=1).first()
#     print(val2.data)
#     return render_template("home.html", user=current_user)


@views.route('/playergoals')
@login_required
def playergoals():
    cur_user_id = int(User.get_id(current_user))
    yearlyGoal = Note.query.filter_by(userId=cur_user_id, noteTypeId=1).first()
    yearlyPlan = Note.query.filter_by(userId=cur_user_id, noteTypeId=2).first()
    longGoal = Note.query.filter_by(userId=cur_user_id, noteTypeId=3).first()
    longPlan = Note.query.filter_by(userId=cur_user_id, noteTypeId=4).first()
    return render_template("goals_view.html", user=current_user, yearlyGoal=yearlyGoal, yearlyPlan=yearlyPlan, longGoal=longGoal, longPlan=longPlan)

#This is for the coach, list of players
@views.route('/playerlist', methods=['Get', 'Post'])
@roles_required(['Coach'])
@login_required
def playerlist():
    coach_id = int(Coach.get_id(current_user))
    coach = Coach.query.filter_by(id=current_user.get_id()).first()
    team_id = Team.query.filter_by(coach_id=coachId).first()
    player_data = User.query.filter_by(coachId=coach_id, teamId=team_id.id)
    return render_template("Complete_User_Profile_Page_for_Bootstrap.html", user=current_user, data=player_data)

# @login_required
# def tryit():
#     val = Notetype.query.filter_by(id=3).first()
#     val2 = Note.query.filter_by(id=1).first()
#     print(val2.data)
#     return render_template("home.html", user=current_user)





