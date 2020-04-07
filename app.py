# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#


from datetime import datetime
import dateutil.parser
import babel
import logging
from logging import Formatter, FileHandler
from forms import *
from models import *
import sys


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    areas = Venues.query.all()

    return render_template('pages/venues.html', areas=areas)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    venues_returned = Venues.query.filter(Venues.city.ilike('%' + search_term + '%'))
    return render_template('pages/search_venues.html', results=venues_returned, search_term=search_term)


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    form = VenueForm()
    venue = Venues.query.filter_by(id=venue_id).first()
    shows = Show.query.filter_by(venue_id=venue_id).all()

    def upcoming_shows():
        upcoming = []

        for show in shows:
            if show.start_time > datetime.now():
                upcoming.append({
                    "artist_id": show.artist_id,
                    "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                    "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
        return upcoming

    def past_show():
        past = []

        for show in shows:
            if show.start_time < datetime.now():
                past.append({
                    "artist_id": show.artist_id,
                    "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
                    "artist_image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
        return past

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_show(),
        "upcoming_shows": upcoming_shows(),
        "past_shows_count": len(past_show()),
        "upcoming_shows_count": len(upcoming_shows())
    }
    return render_template('pages/show_venue.html', form=form, venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # venue = len(Venues.query.all())
    # v#enue += 1
    try:

        form = VenueForm()

        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        genres = form.genres.data
        facebook = form.facebook_link.data
        address = form.address.data

        new_venue = Venues(name=name, city=city, state=state,
                           phone=phone, facebook_link=facebook, genres=genres, address=address)

        db.session.add(new_venue)
        db.session.commit()
        flash('Venue ' + form['name'].data + ' was successfully added!')
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed. ')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

    try:
        delete_venue = Venues.query.filter(Venues.id == venue_id).first()
        venue_name = delete_venue.name
        db.session.delete(delete_venue)
        db.session.commit()
        flash(venue_name + '  was successfully deleted.')

    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred.  ' + venue_name + '  could not be deleted.')
    finally:
        db.session.close()
        print("finally and at last")
        return jsonify({'success': True})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    return render_template('pages/artists.html', artists=artists)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists_returned = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
    return render_template('pages/search_artists.html', results=artists_returned, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()
    shows = Show.query.filter_by(artist_id=artist_id).all()

    def upcoming_shows():
        upcoming = []

        for show in shows:
            if show.start_time > datetime.now():
                upcoming.append({
                    "venue_id": show.venue_id,
                    "venue_name": Venues.query.filter_by(id=show.venue_id).first().name,
                    "venue_image_link": Venues.query.filter_by(id=show.venue_id).first().image_link,
                    "start_time": format_datetime(str(show.start_time))
                })
        return upcoming

    def past_show():
        past = []

        for show in shows:
            if show.start_time < datetime.now():
                past.append({
                    "venue_id": show.venue_id,
                    "venue_name": Venues.query.filter_by(id=show.venue_id).first().name,
                    "venue_image_link": Venues.query.filter_by(id=show.venue_id).first().image_link,
                    "start_time": format_datetime(str(show.start_time))

                })
        return past

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_show(),
        "upcoming_shows": upcoming_shows(),
        "past_shows_count": len(past_show()),
        "upcoming_shows_count": len(upcoming_shows()),
    }

    return render_template('pages/show_artist.html', form=form, artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.filter_by(id=artist_id).first()

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

    try:
        form = ArtistForm()
        edit_artist = Artist.query.get(artist_id)
        edit_artist.name = form.name.data
        edit_artist.genres = form.genres.data
        edit_artist.city = form.city.data
        edit_artist.state = form.state.data
        edit_artist.phone = form.phone.data
        edit_artist.facebook_link = form.facebook_link.data

        # commit changes, flash message if successful

        db.session.add(edit_artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed. ')

    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venues.query.filter_by(id=venue_id).first()

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

    try:
        form = VenueForm()
        edit_venue = Venues.query.get(venue_id)
        print(edit_venue.name)
        edit_venue.name = form.name.data
        edit_venue.genres = form.genres.data
        edit_venue.city = form.city.data
        edit_venue.state = form.state.data
        edit_venue.address = form.address.data
        edit_venue.phone = form.phone.data
        edit_venue.facebook_link = form.facebook_link.data

        # commit changes, flash message if successful

        db.session.add(edit_venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
        # rollback session if error
        db.session.rollback()
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed. ')

    finally:
        # always close the session
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # artist = len(Artist.query.all())
    # artist += 1

    try:
        form = ArtistForm()
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        genres = form.genres.data
        facebook = form.facebook_link.data

        new_artist = Artist(name=name, city=city, state=state,
                            phone=phone, facebook_link=facebook, genres=genres)

        print(new_artist.name, new_artist.id)

        db.session.add(new_artist)
        db.session.commit()
        flash('Artist ' + form['name'].data + ' was successfully added!')
    except:
        db.session.rollback()
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed. ')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    Show_page = Show.query.all()
    Data = []
    # get venue and artist information for each show
    for show in Show_page:
        Data.append({
            "venue_id": show.venue_id,
            "venue_name": Venues.query.filter_by(id=show.venue_id).first().name,
            "artist_id": show.artist_id,
            "artist_name": Artist.query.filter_by(id=show.artist_id).first().name,
            "image_link": Artist.query.filter_by(id=show.artist_id).first().image_link,
            "start_time": format_datetime(str(show.start_time))
        })

    return render_template('pages/shows.html', shows=Data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    try:

        form = ShowForm()
        artist_id = form.artist_id.data
        venue_id = form.venue_id.data
        start_time = form.start_time.data
        print("hello")
        new_show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
        #
        db.session.add(new_show)
        db.session.commit()
        flash('Show  was successfully added!')
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
