import json
import flask

app = flask.Flask(__name__)
in_ = ['coating', 'temp_condition', 'load_area', 'admin_room',
       'domestic_room', 'sludge_plut', 'fire_system', 'floor']

with open('classes.json', encoding='utf-8') as f:
    config = json.load(f)


def test(d: dict) -> str:
    for row in config:
        for key in in_:
            if row[key] is None:
                continue
            if d[key] not in row[key]:
                break
        else:
            if row['height_min'] < d.get('height', 0) <= row['height_max']:
                return d['id'], row['class']
    return d['id'], ''


@app.route('/class', methods=['GET', 'POST'])
def classify():
    req = flask.request.json
    res = []
    for record in req:
        id, class_ = test(record)
        res.append({'id': id, 'class': class_})
    return json.dumps(res, ensure_ascii=False)


# print(test())
app.run('10.199.13.111', 9513)
