from flask import *
from extensions import connect_to_database
from flask import url_for

sqlpage = Blueprint('sqlpage', __name__, template_folder='templates')

@sqlpage.route('/sqlpage', methods = ['GET', 'POST'])
def sqlpage_route():
    db = connect_to_database()
    cur = db.cursor()

    result = ''
    search = ''
    error = ''
    cols = []

    if request.method == 'POST':
        search = request.form.get('command')
        lower = search.split(";")[0].lower()
        birds = lower.split("from")[0]

        if 'update' in lower or 'delete' in lower or 'insert' in lower:
            error = 'Command not allowed, please only use the SELECT command.'
        elif 'create' in lower or 'alter' in lower or 'drop' in lower:
            error = 'Command not allowed, please only use the SELECT command.'
        elif 'select' not in lower or 'from sampleinfo' not in lower:
            error = 'Command not allowed, please only use the SELECT command.'

        if '*' in birds or 'sampleid' in birds: cols.append('sampleid')
        if '*' in birds or 'deviceid' in birds: cols.append('deviceid')
        if '*' in birds or 'added' in birds: cols.append('added')
        if '*' in birds or 'type1' in birds: cols.append('type1')
        if '*' in birds or 'type2' in birds: cols.append('type2')
        if '*' in birds or 'type3' in birds: cols.append('type3')
        if '*' in birds or 'per1' in birds: cols.append('per1')
        if '*' in birds or 'per2' in birds: cols.append('per2')
        if '*' in birds or 'per3' in birds: cols.append('per3')
        if '*' in birds or 'humidity' in birds: cols.append('humidity')
        if '*' in birds or 'temp' in birds: cols.append('temp')
        if '*' in birds or 'light' in birds: cols.append('light')
        if '*' in birds or 'latitude' in birds: cols.append('latitude')
        if '*' in birds or 'longitude' in birds: cols.append('longitude')
        if '*' in birds or 'user' in birds: cols.append('user')

        if not error:
            try:
                cur.execute(search)
                result = cur.fetchall()
            except:
                error = 'The SQL command returned an error. Query is: "' + search + '".'

        if not result and not error:
            error = 'Search did not return any results.'

    options = {
		      "result": result,
        "search": search,
        "error": error,
        "cols": cols
	}
    return render_template("sqlpage.html", **options)
