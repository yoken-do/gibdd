from flask import Flask, request, render_template, redirect, url_for, abort, session, flash
from client import department_list, sign, passport, fines, ts, get_fines_sum

import uuid
app = Flask(__name__, static_url_path='/static')
app.secret_key = str(uuid.main())

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('sign-in.html')
    try:

        fio = request.form.get('fio')
        numer = request.form.get('numer')
        birth_date = request.form.get('birth_date')
        phone = request.form.get('phone')
        if not all([fio, numer, birth_date, phone]) or not sign(fio, numer, birth_date, phone):
            return render_template('sign-in.html')

        session['driver'] = {
                'fio': fio,
                'numer': numer,
                'birth_date': birth_date,
                'phone': phone
        }

        return redirect(url_for('lk'))


    except Exception as e:
        session.pop('driver', None)
        return render_template('sign-in.html')


@app.route('/about')
def about():
    return render_template('about.html')

def cabinet(param, page):
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('main'))

    if not session.get('driver'):
        return redirect(url_for('main'))
    else:
        driver_data = [
            session['driver']['fio'],
            session['driver']['numer'],
            session['driver']['birth_date'],
            session['driver']['phone']
        ]

        if not sign(*driver_data):
            return redirect(url_for('main'))

        match param:
            case 1:
                room = passport(driver_data)
            case 2:
                room = ts(driver_data)
                if sign(*driver_data) and not room:
                    return render_template("transport.html", status=True, message="ТС у владельца не обнаружено")
            case 3:
                room = fines(driver_data)
                if sign(*driver_data):
                    if get_fines_sum(driver_data):
                        return render_template("fine.html", fine_status=True, fine_sum=get_fines_sum(driver_data), room=room)
        if not room:
            session.clear()
            return redirect(url_for('main'))
        return render_template(f'{page}.html', room=room)

@app.route('/lk', methods=['GET', 'POST'])
def lk():
    return cabinet(1, "lk")
@app.route('/transport', methods=['GET', 'POST'])
def transport():
    res = cabinet(2, "transport")
    if res:
        return res
    return render_template("transport.html", status=True, message="ТС у владельца не обнаружено")
@app.route('/fines', methods=['GET', 'POST'])
def fine():
    return cabinet(3, "fine")

@app.route('/department', methods=['GET', 'POST'])
def departament():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('main'))

    if not session.get('driver'):
        return redirect(url_for('main'))
    else:
        return render_template('departament.html', locations=department_list())

@app.route('/data_policy')
def data_policy():
    return render_template('data_policy.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)