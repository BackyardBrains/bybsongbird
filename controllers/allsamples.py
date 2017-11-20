from flask import *
from extensions import connect_to_database
from flask import url_for
import datetime
import os

allsamples = Blueprint('allsamples', __name__, template_folder='templates')

@allsamples.route('/allsamples', methods = ['GET', 'POST'])
def allsamples_route():
    db = connect_to_database()
    cur = db.cursor()

    result = ''

    search = 'SELECT per1, type1, added, sampleid FROM sampleInfo '
    where = 'WHERE '
    order = ' ORDER BY '
    des = ' DESC'
    equal = ' = '
    notequal = ' = '
    greater = ' > '
    lesser = ' < '
    greaterand = ' >= '
    lesserand = ' <= '

    if request.method == 'POST':
        button = request.form.get('sort')
        direction = request.form.get('dir')
        column = request.form.get('col')
        equation = request.form.get('equ')
        match = request.form.get('crit')

        if column != '' and equation != '' and match != '':
            search = search + where + column
            if equation == 'equal': search += equal
            elif equation == 'notequal': search += notequal
            elif equation == 'greater': search += greater
            elif equation == 'lesser': search += lesser
            elif equation == 'greaterand': search += greaterand
            elif equation == 'lesserand': search += lesserand
            if column == 'type1': search += " '"
            search += match
            if column == 'type1': search += "' "

        search = search + order + button

        if direction == 'descending':
            search += des

    cur.execute(search)
    result = cur.fetchall()

    results = []

    for row in result:
      sample = ({
        "per": round(row[0] * 100, 2),
        "perR": round(row[0] * 100, 0), 
        "type": row[1][0:row[1].find('_')].title(),
        "date": row[2].strftime("%b %d %Y"),
        "wave": os.path.join(config.env['UPLOAD_FOLDER'], 'users_clean/' + row[3] + '.png'),
        "id": row[3]
      })
      results.append(sample)

    options = {
		    "results": results
	   }
    return render_template("allsamples.html", **options)