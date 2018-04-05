from flask import Blueprint, redirect, render_template, request, url_for

from forms import EntryForm
from helpers import object_list
from models import Entry, Tag, entry_tags

from app import db

entries = Blueprint('entries', __name__, template_folder='templates')


@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    return entry_list('entries/index.html', entries)


@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('entries/tag_index.html', tags)


@entries.route('/tags/<slug>/')
def tag_detail(slug):
    tag_names = slug.split('+')
    entries = Entry.query.join(entry_tags).join(Tag).filter(Tag.slug.in_(tag_names))
    return entry_list('entries/tag_detail.html', entries)

@entries.route('/create/', methods=['GET', 'POST'])
def create():
    form = EntryForm()
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry())
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
    return render_template('entries/create.html', form=form)

@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    return render_template('entries/detail.html', entry=entry)

@entries.route('/<slug>/edit/', methods=['GET', 'POST'])
def edit(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    if request.method == 'POST':
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry = form.save_entry(entry)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm(obj=entry)
    return render_template('entries/edit.html', entry=entry, form=form)



def entry_list(template, query, **context):
    search = request.args.get('q')
    query = query.filter(Entry.status == Entry.STATUS_PUBLIC)
    if search:
        query = query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search))
        )
    return object_list(template, query, **context)
