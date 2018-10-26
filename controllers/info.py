from flask import *
import extensions
from flask import url_for

info = Blueprint('info', __name__, template_folder='templates')

@info.route('/info', methods = ['GET', 'POST'])
def info_route():
	sampleid = request.args.get('sampleid')
	db = extensions.connect_to_database()
	cur = db.cursor()
	cur.execute('SELECT * FROM sampleInfo WHERE sampleid = %s', (sampleid, ))
	result = cur.fetchone()

	match = {}
	match['sample_id'] = result['sampleid']
	match['first_match'] = json.dumps([{"name": result['type1'][0:result['type1'].find('_')].title(), "value": float(result["per1"])}, {"name": "Other", "value": 1 - float(result["per1"])}])
	match['second_match'] = json.dumps([{"name": result['type2'][0:result['type2'].find('_')].title(), "value": float(result["per2"])}, {"name": "Other", "value": 1 - float(result["per2"])}])
	match['third_match'] = json.dumps([{"name": result['type3'][0:result['type3'].find('_')].title(), "value": float(result["per3"])}, {"name": "Other", "value": 1 - float(result["per3"])}])
	match['added'] = result['added'].strftime("%b %d %Y %X")
	match['latitude'] = result['latitude']
	match['longitude'] = result['longitude']
	match['humidity'] = int(round(result['humidity']))
	match['temperature'] = int(round(result['temp']))
	match['light'] = int(round(result['light']))

	options = {
		"match": match
	}
	return render_template("info.html", **options)
