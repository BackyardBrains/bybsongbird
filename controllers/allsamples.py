import os

from flask import *

import config
from extensions import connect_to_database

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

        if 'update' in match.lower() or 'delete' in match.lower() or 'insert' in match.lower():
            good = False
        elif 'create' in match.lower() or 'alter' in match.lower() or 'drop' in match.lower():
            good = False
        elif ';' in match.lower() or 'select' in match.lower():
            good = False

        if equation != '' and match != '' and good == True:
            good = False

            search = search + ' WHERE ' + column
            
            if column == 'type1':
              if equation == 'equal': search = search + " LIKE '%" + match + "%' "
              elif equation == 'notequal': search = search + " NOT LIKE '%" + match + "%' "
              elif equation == 'greater': search = search + " > '" + match + "' "
              elif equation == 'lesser': search = search + " < '" + match + "' "
              elif equation == 'greaterand': search = search + " >= '" + match + "' "
              elif equation == 'lesserand': search = search + " <= '" + match + "' "
              good = True
            else:
              if equation == 'equal': search += ' = '
              elif equation == 'notequal': search += ' <> '
              elif equation == 'greater': search += ' > '
              elif equation == 'lesser': search += ' < '
              elif equation == 'greaterand': search += ' >= '
              elif equation == 'lesserand': search += ' <= '
              
              if column == 'added' and match.isdigit() and len(match) == 8:
                month = match[0:2]
                day = match[2:4]
                year = match[4:]
                if int(month) > 0 and int(month) < 13 and int(day) > 0 and int(day) < 32:
                  search = search + " '" + year + "-" + month + "-" + day + " 00:00:00'"
                  good = True
                else: good = False
              else:
                try:
                  match = float(match)
                  if column == 'per1' and match > 100:
                    match = match / 100.0
                  search += str(match)
                  good = True
                except:
                  good = False

        search = search + ' ORDER BY ' + button

        if direction == 'descending':
            search += ' DESC'
    
    if good:
      cur.execute(search)
      result = cur.fetchall()
    
    results = []

    for row in result:
      birdType = row['type1'][0:row['type1'].find('_')]
      if 'robin' in birdType:
        color = 'green'
      elif 'gold' in birdType:
        color = 'orange'
      elif 'jay' in birdType:
        color = 'lightgr'
      elif 'chicadee' in birdType:
        color = 'red'
      elif 'crow' in birdType:
        color = 'lightbl'
      elif 'titmouse' in birdType:
        color = 'indigo'
      elif 'cardinal' in birdType:
        color = 'purple'
      elif 'sparrow' in birdType:
        color = 'brown'
      else:
        color = 'blue'
      
      sample = ({
        "per": round(row['per1'] * 100, 2),
        "perR": int(round(row['per1'] * 100, 0)), 
        "type": birdType.title(),
        "date": row['added'].strftime("%b %d %Y"),
        "wave": os.path.join(config.env['UPLOAD_FOLDER'], 'users_clean/' + str(row['sampleid']) + '.png'),
        "id": str(row['sampleid']),
        "color": color
      })
      results.append(sample)

    options = {
		    "results": results
	   }
    return render_template("allsamples.html", **options)
