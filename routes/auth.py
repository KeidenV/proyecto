from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Usuario, Rol, Actividad, Entrenamiento, Asistencia, Competicion, ResultadoCompeticion
from forms import LoginForm, RegistrationForm, UsuarioForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.dashboard')
            return redirect(next_page)
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            id_rol=form.id_rol.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.role == 'member':
        member = Member.query.filter_by(user_id=current_user.id).first()
        form = MemberForm(obj=member)
        
        if form.validate_on_submit():
            if member:
                form.populate_obj(member)
            else:
                member = Member(user_id=current_user.id)
                form.populate_obj(member)
                db.session.add(member)
            
            db.session.commit()
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('auth.profile'))
        
        return render_template('auth/member_profile.html', form=form, member=member)
    
    elif current_user.role == 'trainer':
        trainer = Trainer.query.filter_by(user_id=current_user.id).first()
        form = TrainerForm(obj=trainer)
        
        if form.validate_on_submit():
            if trainer:
                form.populate_obj(trainer)
            else:
                trainer = Trainer(user_id=current_user.id)
                form.populate_obj(trainer)
                db.session.add(trainer)
            
            db.session.commit()
            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('auth.profile'))
        
        return render_template('auth/trainer_profile.html', form=form, trainer=trainer)
    
    return redirect(url_for('main.dashboard'))
