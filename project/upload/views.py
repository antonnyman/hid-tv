import os, random, string, datetime
from flask import Blueprint, jsonify, flash
from project import db, app, login_manager, login_required, \
    login_user, redirect, render_template, request, logout_user, \
    session, current_user, OAuth2Session, HTTPError, url_for
from project.models import Page, Reload

upload_blueprint = Blueprint('upload', __name__)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            rand = ''.join(random.SystemRandom().choice(string.hexdigits) for _ in range(8))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], rand + ".jpg"))
            page = Page(
                picture = rand,
                name = rand,
                created_by = current_user.name,
                position = 0
            )
            db.session.add(page)
            db.session.commit()
            return jsonify({'result': rand + ''})
        else:
            if request.form:
                pos = request.form.getlist('position')
                name = request.form.getlist('name')

                for index, p in enumerate(request.form.getlist('id')):
                    page = Page.query.filter_by(id = p).first()
                    page.position = pos[index]
                    page.name = name[index]
                    db.session.commit()
                

    pages = Page.query.order_by(Page.position).all()
    return render_template('upload.html', pages = pages)

@app.route('/delete/<id>')
@login_required
def delete(id):
    page = Page.query.filter_by(id = id).first()
    db.session.delete(page)
    db.session.commit()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], page.picture + ".jpg"))
    return redirect('/upload')


@app.route('/reload-tv')
@login_required
def reload_tv():
    reload = Reload()
    db.session.add(reload)
    db.session.commit()
    return redirect('/upload')

@app.route('/get-reload')
def get_reload():
    reload = Reload.query.order_by(Reload.id.desc()).first()
    if datetime.datetime.now() > reload.reload:
        if reload.reloaded == False:
            reload.reloaded = True
            db.session.commit()
            return jsonify({"result": "true"})
        else:
            return jsonify({"result": "false"})
    else:
        return jsonify({"result": "false"})
