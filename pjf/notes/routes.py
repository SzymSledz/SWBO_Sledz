from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from pjf import db
from pjf.models import notes as NotesModel
from datetime import datetime

notes_bp = Blueprint('notes_bp', __name__)

@notes_bp.route('/notes')
def notes_page():
    if 'login' in session:
        all_notes = NotesModel.query.filter_by(user_id=session['login']).all()
        return render_template('notes.html', notes=all_notes)
    else:
        flash('You must be logged in to view your notes.', 'danger')
        return redirect(url_for('user.login_page'))

@notes_bp.route('/add_note', methods=['GET', 'POST'])
def add_note():
    if 'login' in session:
        if request.method == 'POST':
            title = request.form['title']
            text = request.form['text']
            new_note = NotesModel(title=title, text=text, user_id=session['login'])
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', 'success')
            return redirect(url_for('notes_bp.notes_page'))
        return render_template('add_note.html')
    else:
        flash('You must be logged in to add notes.', 'danger')
        return redirect(url_for('user.login_page'))

@notes_bp.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    if 'login' in session:
        note = NotesModel.query.get_or_404(note_id)
        if note.user_id == session['login']:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully!', 'success')
        else:
            flash('You do not have permission to delete this note.', 'danger')
    else:
        flash('You must be logged in to delete notes.', 'danger')
    return redirect(url_for('notes_bp.notes_page'))
