from flask import *
from extensions import connect_to_database
from flask import url_for
import datetime
import os
import config

allsamples = Blueprint('allsamples', __name__, template_folder='templates')

@allsamples.route('/allsamples', methods = ['GET', 'POST'])
def allsamples_route():
    db = connect_to_database()
    cur = db.cursor()

    result = ''

    base = 'SELECT per1, type1, added, sampleid FROM sampleInfo '
    search, button, direction, column, equation, match = '', '', '', '', '', ''
    good = True

    if request.method == 'POST':
        button = request.form.get('sort')
        direction = request.form.get('dir')
        column = request.form.get('col')
        equation = request.form.get('equ')
        match = request.form.get('crit')

        if column != '' and equation != '' and match != '':
            good = False

            search = search + ' WHERE ' + column
            if equation == 'equal': search += ' = '
            elif equation == 'notequal': search += ' <> '
            elif equation == 'greater': search += ' > '
            elif equation == 'lesser': search += ' < '
            elif equation == 'greaterand': search += ' >= '
            elif equation == 'lesserand': search += ' <= '
            
            if column == 'type1':
              search = search + " LIKE '%" + match + "%' "
              good = True
            elif column == 'added':
              if len(match) == 8 and match.isdigit():
                month = match[0:2]
                day = match[2:4]
                year = match[4:]
                if int(month) < 1 or int(month) > 12 or int(day) < 1 or int(day) > 30:
                  search = search + " '" + year + "-" + month + "-" + day + " 00:00:00'"
                  good = True
                else: good = False
              else: good = False
            else:
              if match.isdigit(): good = True
              else: good = False

        search = search + ' ORDER BY ' + button

        if direction == 'descending':
            search += ' DESC'
    
    if good:
      base = base + search

    cur.execute(base)
    result = cur.fetchall()
    
    print(search)
    print(result)
    
    results = []

    for row in result:
      sample = ({
        "per": round(row['per1'] * 100, 2),
        "perR": int(round(row['per1'] * 100, 0)), 
        "type": row['type1'][0:row['type1'].find('_')].title(),
        "date": row['added'].strftime("%b %d %Y"),
        "wave": os.path.join(config.env['UPLOAD_FOLDER'], 'users_clean/' + str(row['sampleid']) + '.png'),
        "id": str(row['sampleid'])
      })
      results.append(sample)

    options = {
		    "results": results
	   }
    return render_template("allsamples.html", **options)