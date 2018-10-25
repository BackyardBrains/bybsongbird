from flask import *
import bybsongbird.extensions as ex
from flask import url_for
import os
import bybsongbird.config

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/', methods = ['GET', 'POST'])
def main_route():
    db = ex.connect_to_database()
    cur = db.cursor()
    cur.execute("SELECT * FROM sampleInfo ORDER BY added DESC LIMIT 3")
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
            "wave": os.path.join(bybsongbird.config.env['UPLOAD_FOLDER'], 'users_clean/' + str(row['sampleid']) + '.png'),
            "id": str(row['sampleid']),
            "color": color
        })
        results.append(sample)

    options = {
		"results": results
	}
    return render_template("index.html", **options)
