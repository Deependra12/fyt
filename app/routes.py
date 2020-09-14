from flask import (
    render_template, 
    redirect, 
    url_for, 
    jsonify, 
    request, 
    flash,
    session,
    abort,
    jsonify,
)

from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)

import os
import secrets
from PIL import Image

from . import app, db
from . import login_manager
from . import email as em
from .forms import (
    RegistrationForm, 
    LoginForm, 
    ResetForm, 
    ResetLinkForm, 
    MyLocationForm, 
    PersonalInfoForm,
    StudentPersonalInfoForm,
    AccountInfoForm,
    MyCourseForm,
    MyExperienceForm,
    MyAchievementForm,
    MyQualificationForm
)
from .models import User, Student, Tutor, Location, Course, Experience, Achievement, Qualification, Mycourse


def redirect_user(user):
    if user.role == 'student':
        return redirect(url_for('student'))
    elif user.role == 'tutor':
        return redirect(url_for('tutor'))
    elif user.role == 'admin':
        return redirect('/admin')


def is_tutor(user):
    if user.role == 'tutor':
        return True
    elif user.role == 'student':
        return False
    elif user.role == 'admin':
        return False


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect_user(current_user)
    return render_template('index.html')


@app.route('/about-us')
def about_us():
    """ Render the about us page """
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_user(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect (url_for('login'))
        login_user(user)
        flash('Successfully logged in.', 'success')
        return redirect_user(current_user)
    return render_template('login.html', form=form)


@app.route('/check/username/<username>')
def check_username_availability(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({"message": "Username not available", "availability": False})
    else:
        return jsonify({"message": "Username available", "availability": True})


@app.route('/check/email/<email>')
def check_email_availability(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"message": "Email already registered", "availability": False})
    else:
        return jsonify({"message": "Email available", "availability": True})


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect_user(current_user)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        if is_tutor(user):
            user.set_tutor()
            user.update_tutor(phone=form.phone.data)
        else:
            user.set_student()
            user.update_student(phone=form.phone.data)
        user.set_location()
        db.session.commit()
        #message = "Welcome to Find Your Tutor"
        #em.send_mail(username, role, message, email)
        flash('Your account was created.\nYou can now Login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/password-reset', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetLinkForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Sorry, no user with that email registered!', 'danger')
            return redirect(url_for('reset_request'))
        em.send_reset_mail(user)
        flash('An email has been sent with instruction to reset your password','info')
        return redirect(url_for('login'))

    return render_template('resetlink.html',form=form)


@app.route('/password-reset/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is invalid token!', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been updated!','info')
        return redirect(url_for('login'))
    else: 
        print('blabla')
    return render_template('reset.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You are now logged out. Log in to continue!', 'success')
    return redirect(url_for('login'))

@app.route("/user/delete/<username>")
@login_required
def delete_user_account(username):
    user_to_be_deleted = User.query.filter_by(username=username).first()
    if current_user == user_to_be_deleted:
        profile_pic = getattr(current_user, current_user.role).profile_pic
        if profile_pic:
            delete_picture(profile_pic)
        db.session.delete(user_to_be_deleted)
        db.session.commit()
        flash('Successfully deleted account! But we\'re sad to see you go!', 'success')
        return redirect(url_for('user_register'))
    flash('You are not allowed to delete anyone else\'s account! Have you gone nuts?', 'danger')
    if is_tutor(current_user):
        return redirect(url_for('tutor')) 
    else:   
        return redirect(url_for('student'))

# Utility functions


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics/', picture_fn)
    output_size = (200,200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_docs(docs, directory):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(docs.filename)
    docs_fn = random_hex + f_ext
    docs_path = os.path.join(app.root_path, 'static/docs/' ,directory, docs_fn)
    docs.save(docs_path)
    return docs_fn


def delete_picture(user_picture):
    picture_path = os.path.join(app.root_path, 'static','profile_pics', user_picture)
    os.remove(picture_path)

def delete_docs(docs,directory):
    docs_path = os.path.join(app.root_path,'static','docs', directory, docs)
    os.remove(docs_path)


def fetch_default_profile_pic(user_obj):
    if isinstance(user_obj, Tutor):
        return url_for('static', filename='profile_pics/tutor.jpg')
    else:
        return url_for('static', filename='profile_pics/student.jpg')


def fetch_profile_pic(user_obj):
    try:
        pic_name_from_db = getattr(user_obj, 'profile_pic')
        picture_path = os.path.join(app.root_path, 'static/profile_pics')
        if pic_name_from_db in os.listdir(picture_path):
            profile_pic = url_for('static',filename='profile_pics/' + pic_name_from_db)
            return profile_pic
        return fetch_default_profile_pic(user_obj)
    except:
        return fetch_default_profile_pic(user_obj)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username), 'danger')
        if is_tutor(current_user):
            return redirect(url_for('tutor'))
        else:
            return redirect(url_for('student'))
    if is_tutor(user) and not is_tutor(current_user):
        current_user.follow(user)       
    else:
        flash('This action is not allowed!', 'danger')
        return redirect(url_for('profile', username=username))
    if user == current_user:
        flash('You cannot follow yourself!', 'info')
        return redirect(url_for('profile', username=username))
    db.session.commit()
    flash('You followed {}!'.format(username), 'success')
    return redirect(url_for('profile', username=username))

 
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username),'danger')
        if is_tutor(current_user):
            return redirect(url_for('tutor'))
        else:
            return redirect(url_for('student'))
    if is_tutor(user) and not is_tutor(current_user):
        current_user.unfollow(user)       
    else:
        flash('This action is not allowed!', 'danger')
        return redirect(url_for('profile', username=username))
    if user == current_user:
        flash('You cannot unfollow yourself!','info')
        return redirect(url_for('profile', username=username))
    db.session.commit()
    flash('You unfollowed {}.'.format(username),'danger')
    return redirect(url_for('profile', username=username))
# Public Profile


@app.route('/profiles/<username>')
@login_required
def profile(username):
    google_api = app.config.get('GOOGLE_MAP_API_KEY')
    user = User.query.filter_by(username=current_user.username).first()
    if is_tutor(user):
        user_obj = Tutor.query.filter_by(user_id=user.id).first()
    else:
        user_obj = Student.query.filter_by(user_id=user.id).first()
    view_user = User.query.filter_by(username=username).first_or_404()
    return render_template('public-profile.html', user=user, view_user=view_user, profilepic= fetch_profile_pic(user_obj), google_api_key=google_api)


# Student Routes

@app.route('/student')
@app.route('/student/home')
@login_required
def student():
    google_api = app.config.get('GOOGLE_MAP_API_KEY')
    tutor_list = User.query.filter_by(role="tutor")
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect('/admin')
    user = User.query.filter_by(username=current_user.username).first()
    mycourse = db.session.query(User,Mycourse,Course).select_from(User).join(Mycourse).join(Course).filter(User.id==current_user.id).all()
    all_tutor_course = db.session.query(User,Mycourse,Course).select_from(User).join(Mycourse).join(Course).filter(User.role=='tutor').all()   
    if user.username == current_user.username and user.role == 'student':
        student = Student.query.filter_by(user_id=user.id).first()
        return render_template('student.html', user=user, student=student, tutor_list=tutor_list, profilepic= fetch_profile_pic(student), google_api_key=google_api)
    abort(404)


@app.route('/student/my-location', methods=['POST','GET'])
@login_required
def student_location():
    form = MyLocationForm()
    google_api = app.config.get('GOOGLE_MAP_API_KEY')
    opencage_api = app.config.get('OPENCAGE_GEOCODE_API_KEY')
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        user.update_location(
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            place_details=form.place.data
        )
    location = Location.query.filter_by(user_id=user.id).first()
    
    if user.username == current_user.username and not is_tutor(user):
        student=Student.query.filter_by(user_id=user.id).first()
        return render_template("my-location.html", user=user, student=student, profilepic= fetch_profile_pic(student), form=form, google_api_key=google_api,
            opencage_api_key=opencage_api, location=location)
    elif user.username == current_user.username and is_tutor(user):
        return redirect(url_for('tutor_location'))


@app.route('/student/personal-info', methods=['POST','GET'])
@login_required
def student_personal_info():
    if is_tutor(current_user):
        return redirect(url_for('tutor_personal_info'))
    else:
        user = User.query.filter_by(username=current_user.username).first()
        student=Student.query.filter_by(user_id=user.id).first()
        form = StudentPersonalInfoForm()
        form.create_state_choices()
        form.create_district_choices()
        if form.validate_on_submit():
            if form.profile_pic.data:
                if student.profile_pic:
                    delete_picture(student.profile_pic)
                current_user.update_student(profile_pic = save_picture(form.profile_pic.data))
            current_user.update_student(
                full_name=form.name.data, 
                state=form.state.data,
                district = form.district.data,
                date_of_birth = form.date_of_birth.data,
                municipality = form.municipality.data,
                ward_no = form.ward_no.data,
                phone = form.phone.data ,
                description = form.self_description.data.strip(),
                guardian_name = form.guardian_name.data,
                guardian_address = form.guardian_address.data,
                guardian_phone = form.guardian_phone.data
                
            )
        return render_template("personal-info.html", user=user, user_obj=student, profilepic= fetch_profile_pic(student), form=form)


@app.route('/student/account-activities', methods=['POST','GET'])
@login_required
def student_account_activities():
    form = AccountInfoForm()
    user = User.query.filter_by(username=current_user.username).first()
    if user.username == current_user.username and not is_tutor(user):
        student = Student.query.filter_by(user_id=user.id).first()
        if form.validate_on_submit():
            if not user.check_password(form.old_password.data):
                flash("Wrong password!","danger")
                return redirect(url_for('student_account_info'))
            else:
                user.set_password(form.new_password.data)
                db.session.commit()
                flash("Successfully changed password!", "success")
                return redirect(url_for('student'))
        return render_template("account-activities.html", user=user, student=student, profilepic= fetch_profile_pic(student), form=form)
    elif user.username == current_user.username and is_tutor(user):
        return redirect(url_for('tutor_account_info'))


@app.route('/student/my-courses', methods=['POST','GET'])
@login_required
def student_courses():
    user = User.query.filter_by(username=current_user.username).first()
    my_courses = Mycourse.query.filter_by(user_id=current_user.id)
    form = MyCourseForm()
    form.create_cost_choices()
    if user.username == current_user.username and not is_tutor(user):
        student = Student.query.filter_by(user_id=user.id).first()
        return render_template("my-courses.html", user=user, student=student, 
        profilepic= fetch_profile_pic(student), my_courses=my_courses, form=form)
    elif user.username == current_user.username and is_tutor(user):
        return redirect(url_for('tutor'))

    
@app.route('/student/delete/mycourse/<int:id>', methods=['POST', 'GET'])
def delete_student_courses(id):
    user = User.query.filter_by(username=current_user.username).first()

    if user.username == current_user.username and not is_tutor(user):
        mycourse_to_be_deleted = Mycourse.query.filter_by(id=id).first_or_404()
        db.session.delete(mycourse_to_be_deleted)
        db.session.commit()
        return redirect(url_for('student_courses'))  
    elif user.username == current_user.username and is_tutor(user):
        return redirect(url_for('student'))


@app.route('/student/my-tutors', methods=['POST', 'GET'])
@login_required
def student_followed_tutors():
    user = User.query.filter_by(username=current_user.username).first()
    followed_tutors=user.followed.all()
    if user.username == current_user.username and not is_tutor(user):
        student = Student.query.filter_by(user_id=user.id).first()
        return render_template('my-tutors.html', profilepic= fetch_profile_pic(student), user=user, followed_tutors=followed_tutors)
    elif user.username == current_user.username and is_tutor(user):
        return redirect(url_for('tutor_followers'))
        

# Tutor Routes


@app.route('/tutor')
@app.route('/tutor/home')
@login_required
def tutor():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect('/admin')
    user = User.query.filter_by(username=current_user.username).first()
    if user.username == current_user.username and is_tutor(user):
        tutor=Tutor.query.filter_by(user_id=user.id).first()
        return render_template("tutor.html", user=user, tutor=tutor, profilepic= fetch_profile_pic(tutor))
    abort(404)


@app.route('/tutor/my-location', methods=['POST','GET'])
@login_required
def tutor_location():
    form = MyLocationForm()
    google_api = app.config.get('GOOGLE_MAP_API_KEY')
    opencage_api = app.config.get('OPENCAGE_GEOCODE_API_KEY')
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        user.update_location(
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            place_details=form.place.data
        )
    location = Location.query.filter_by(user_id=user.id).first()
    
    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student_location'))
    elif user.username == current_user.username and is_tutor(user):
        tutor=Tutor.query.filter_by(user_id=user.id).first()
        return render_template("my-location.html", user=user, tutor=tutor, profilepic= fetch_profile_pic(tutor), form=form, google_api_key=google_api,
            opencage_api_key=opencage_api, location=location)


@app.route('/tutor/personal-info', methods=['POST' ,'GET'])
@login_required
def tutor_personal_info():
    if is_tutor(current_user):
        user = User.query.filter_by(username=current_user.username).first()
        tutor=Tutor.query.filter_by(user_id=user.id).first()
        form = PersonalInfoForm()
        form.create_state_choices()
        form.create_district_choices()
        if form.validate_on_submit():   
            if form.profile_pic.data:
                if tutor.profile_pic:
                    delete_picture(tutor.profile_pic)
                user.update_tutor(profile_pic = save_picture(form.profile_pic.data))
            user.update_tutor(
                full_name=form.name.data, 
                state=form.state.data,
                district = form.district.data,
                date_of_birth = form.date_of_birth.data,
                municipality = form.municipality.data,
                ward_no = form.ward_no.data,
                phone = form.phone.data,
                description = form.self_description.data
            )
        return render_template("personal-info.html", user=user, user_obj=tutor, profilepic= fetch_profile_pic(tutor), form=form)
    else:
        return redirect(url_for('student_personal_info'))


@app.route('/tutor/account-activities', methods=['POST','GET'])
@login_required
def tutor_account_activities():
    form = AccountInfoForm()
    user = User.query.filter_by(username=current_user.username).first()
    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student_account_info'))
    elif user.username == current_user.username and is_tutor(user):
        tutor = Tutor.query.filter_by(user_id=user.id).first()
        if form.validate_on_submit():
            if not user.check_password(form.old_password.data):
                flash("Wrong password!","danger")
                return redirect(url_for('tutor_account_info'))
            else:
                user.set_password(form.new_password.data)
                db.session.commit()
                flash("Successfully changed password!", "success")
                return redirect(url_for('tutor'))
        return render_template("account-activities.html", user=user, tutor=tutor, profilepic=fetch_profile_pic(tutor), form=form)


@app.route('/tutor/my-courses', methods=['POST', 'GET'])
@login_required
def tutor_courses():
    user = User.query.filter_by(username=current_user.username).first()
    my_courses = Mycourse.query.filter_by(user_id=current_user.id)
    form = MyCourseForm()
    form.create_cost_choices()
    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student'))
    elif user.username == current_user.username and is_tutor(user):
        tutor=Tutor.query.filter_by(user_id=user.id).first()
        return render_template("my-courses.html", user=user, tutor=tutor,
         profilepic=fetch_profile_pic(tutor), my_courses=my_courses ,form=form)


@app.route('/tutor/delete/mycourse/<int:id>', methods=['POST', 'GET'])
def delete_tutor_courses(id):
    user = User.query.filter_by(username=current_user.username).first()

    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student'))
    elif user.username == current_user.username and is_tutor(user):
        mycourse_to_be_deleted = Mycourse.query.filter_by(id=id).first_or_404()
        db.session.delete(mycourse_to_be_deleted)
        db.session.commit()
        return redirect(url_for('tutor_courses'))   


@app.route('/tutor/my-educational-profile', methods=['POST','GET'])
@login_required
def tutor_educational_profile():
    form_experience = MyExperienceForm()
    form_qualification = MyQualificationForm()
    form_achievement = MyAchievementForm()
    user = User.query.filter_by(username=current_user.username).first()
    tutor=Tutor.query.filter_by(user_id=user.id).first()
    if form_experience.validate_on_submit():
        experience = Experience(
            title=form_experience.title.data,
            institution=form_experience.institution.data,
            experience=form_experience.experience.data, 
            experience_file=save_docs(form_experience.experience_certificate.data, "experience"), 
            Tutor=tutor
        )
        db.session.add(experience)
        db.session.commit()
        return redirect(url_for('tutor_educational_profile'))
    elif form_achievement.validate_on_submit():
        achievement = Achievement(
            achievement=form_achievement.achievement.data, 
            awarded_by= form_achievement.awarded_by.data,
            awarded_date=form_achievement.awarded_date.data,
            achievement_file=save_docs(form_achievement.achievement_certificate.data, "achievement"), 
            Tutor=tutor
        )
        db.session.add(achievement)
        db.session.commit()
        return redirect(url_for('tutor_educational_profile'))
    elif form_qualification.validate_on_submit():
        qualification = Qualification(
            qualification=form_qualification.qualification.data,
            institution=form_qualification.institution.data,
            qualification_date=form_qualification.qualification_date.data,
            qualification_file=save_docs(form_qualification.qualification_certificate.data, "qualification"),
            Tutor=tutor)
        db.session.add(qualification)
        db.session.commit()
        return redirect(url_for('tutor_educational_profile'))
    qualifications = Qualification.query.filter_by(tutor_id=user.id)
    achievements = Achievement.query.filter_by(tutor_id=user.id)
    experiences = Experience.query.filter_by(tutor_id=user.id)
    if user.username == current_user.username and is_tutor(user):
        return render_template('my-educational-profile.html', profilepic=fetch_profile_pic(tutor), user=user, tutor=tutor, 
            qualifications=qualifications, achievements=achievements, experiences=experiences,
            form_experience=form_experience, form_qualification=form_qualification, form_achievement=form_achievement)
    elif user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student'))


@app.route('/delete/experience/<int:id>')
@login_required
def delete_tutor_experience(id):
    user = User.query.filter_by(username=current_user.username).first()

    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student'))
    elif user.username == current_user.username and is_tutor(user):
        experience_to_be_deleted = Experience.query.filter_by(id=id).first_or_404()
        delete_docs(experience_to_be_deleted.experience_file,'experience')
        db.session.delete(experience_to_be_deleted)
        db.session.commit()
        return redirect(url_for('tutor_educational_profile'))   


@app.route('/delete/qualification/<int:id>')
@login_required
def delete_tutor_qualification(id):
    user = User.query.filter_by(username=current_user.username).first()

    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student'))
    elif user.username == current_user.username and is_tutor(user):
        qualification_to_be_deleted = Qualification.query.filter_by(id=id).first_or_404()
        delete_docs(qualification_to_be_deleted.qualification_file,'qualification')
        db.session.delete(qualification_to_be_deleted)
        db.session.commit()
        return redirect(url_for('tutor_educational_profile'))  


@app.route('/delete/achievement/<int:id>')
@login_required
def delete_tutor_achievement(id):
    user = User.query.filter_by(username=current_user.username).first()

    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student'))
    elif user.username == current_user.username and is_tutor(user):
        achievement_to_be_deleted = Achievement.query.filter_by(id=id).first_or_404()
        delete_docs(achievement_to_be_deleted.achievement_file,'achievement')
        db.session.delete(achievement_to_be_deleted)
        db.session.commit()
        return redirect(url_for('tutor_educational_profile')) 


@app.route('/edit/experience/<int:id>')
@login_required
def edit_tutor_experience(id):
    pass


@app.route('/edit/qualification/<int:id>')
@login_required
def edit_tutor_qualification(id):
    pass


@app.route('/edit/achievement/<int:id>')
@login_required
def edit_tutor_achievement(id):
    pass


@app.route('/tutor/my-followers', methods=['POST', 'GET'])
@login_required
def tutor_followers():
    user = User.query.filter_by(username=current_user.username).first()
    my_followers = user.followers.all()
    if user.username == current_user.username and not is_tutor(user):
        return redirect(url_for('student_followed_tutors'))
    elif user.username == current_user.username and is_tutor(user):
        tutor=Tutor.query.filter_by(user_id=user.id).first()
        return render_template('my-followers.html', profilepic=fetch_profile_pic(tutor), tutor=tutor, user=user, my_followers=my_followers)


#Courses


@app.route('/courses')
@login_required
def courses():
    educational_level = request.args.get('educational_level', None)
    if educational_level:
        courses = Course.query.filter_by(course_level=educational_level)
    else:
        courses = Course.query.all()
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('courses.html',profilepic=fetch_profile_pic(getattr(user, user.role)), courses=courses, user=user)
    

@app.route('/courses/<int:id>')
@login_required
def courses_by_id(id):
    course = Course.query.filter_by(id=id).first_or_404()
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('course-details.html', course=course, profilepic=fetch_profile_pic(getattr(user, user.role)), user=user)


# MyCourse


@app.route('/my-courses/add/<int:id>', methods=['GET','POST'])
@login_required
def add_course(id):
    user = User.query.filter_by(username=current_user.username).first()
    form = MyCourseForm()
    form.create_cost_choices()
    course= Course.query.filter_by(id=id).first_or_404()
    if form.validate_on_submit():
        mycourse = Mycourse(Course=course, User=current_user, time=form.time.data, cost=form.cost.data)
        db.session.add(mycourse)
        db.session.commit()
        if is_tutor(user):
            return redirect(url_for('tutor_courses'))
        else:
            return redirect(url_for('student_courses'))
    return render_template('add-my-courses.html', form=form, profilepic=fetch_profile_pic(getattr(user, user.role)), user=user, course=course)


@app.route('/edit/my-course/<int:id>', methods=['GET','POST'])
@login_required
def edit_mycourse(id):
    user = User.query.filter_by(username=current_user.username).first()
    form = MyCourseForm()
    form.create_cost_choices()
    my_course = Mycourse.query.filter_by(id=id,User=user).first_or_404()
    if form.validate_on_submit():
        my_course.time=form.time.data
        my_course.cost=form.cost.data
        db.session.commit()
        if is_tutor(user):
            return redirect(url_for('tutor_courses'))
        else:
            return redirect(url_for('student_courses'))
    return render_template('edit-my-courses.html', form=form, profilepic=fetch_profile_pic(getattr(user, user.role)), user=user, course=my_course)


# Error Handlers


@app.errorhandler(404)
def content_not_found_handler(e):
    """ For Handling 404 error """
    return render_template('404.html')


@app.errorhandler(401)
def unauthorized_access_handler(e):
    """ For Handling 401 error """
    flash('You must be logged in to access this page!', 'danger')
    return redirect(url_for('login'))