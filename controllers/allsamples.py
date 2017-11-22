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

    search = 'SELECT per1, type1, added, sampleid FROM sampleInfo '
    good = True

    if request.method == 'POST':
        button = request.form.get('sort')
        direction = request.form.get('dir')
        column = request.form.get('col')
        equation = request.form.get('equ')
        match = request.form.get('crit')

        if equation != '' and match != '':
            good = False

            search = search + ' WHERE ' + column
            
            if column == 'type1':
              if equation == 'equal': 
                search = search + " LIKE '%" + match + "%' "
              elif equation == 'notequal':
                search = search + " NOT LIKE '%" + match + "%' "
              elif equation == 'greater':
                search = search + " > '" + match + "' "
              elif equation == 'lesser':
                search = search + " < '" + match + "' "
              elif equation == 'greaterand':
                search = search + " >= '" + match + "' "
              elif equation == 'lesserand':
                search = search + " <= '" + match + "' "
              good = True
            else:
              if match.isdigit():
                if equation == 'equal': search += ' = '
                elif equation == 'notequal': search += ' <> '
                elif equation == 'greater': search += ' > '
                elif equation == 'lesser': search += ' < '
                elif equation == 'greaterand': search += ' >= '
                elif equation == 'lesserand': search += ' <= '
                if column == 'added':
                  if len(match) == 8:
                    month = match[0:2]
                    day = match[2:4]
                    year = match[4:]
                    if int(month) > 0 and int(month) < 13 and int(day) > 0 and int(day) < 32:
                      search = search + " '" + year + "-" + month + "-" + day + " 00:00:00'"
                      good = True
                    else: good = False
                  else: good = False
                else:
                  search += match
                  good = True
              else: good = False
        elif equation == '' and match != '':
          good = False

        search = search + ' ORDER BY ' + button

        if direction == 'descending':
            search += ' DESC'
    
    print("search :: " + search)

    if good:
      cur.execute(search)
      result = cur.fetchall()

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