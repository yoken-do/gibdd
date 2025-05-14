from flask import Flask, request, render_template, redirect, url_for, abort, session, flash
from client import driver_check, gen_vu, del_fine, add_fine, add_transport, del_transport

import uuid
app = Flask(__name__, static_url_path='/static')
app.secret_key = str(uuid.main())

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('vu.html')
    try:

        fio = request.form.get('fio')
        numer = request.form.get('numer')
        birth_date = request.form.get('birth_date')
        seria, nomer = str(request.form.get('passport_seria')), str(request.form.get('passport_numer'))
        if not all([fio, numer, birth_date, seria, nomer]):
            return render_template('vu.html')
        if driver_check([fio, seria, nomer, numer, birth_date]):
            status, vu, end = gen_vu(numer)
            return render_template('vu.html', status=status, vu=vu, end=end)


    except Exception as e:
        return render_template('vu.html')

@app.route('/fine', methods=['GET', 'POST'])
def fine():
    if request.method == 'GET':
        return render_template('fine.html')

    try:
        action = request.form.get('action')
        if action == "Удалить штраф":
            fio = request.form.get('fio')
            numer = request.form.get('numer')
            fine_num = request.form.get('fine_num')

            if not all([fio, numer, fine_num]):
                return render_template('fine.html')
            
            fine_num = int(fine_num)

            status, message = del_fine([fio, numer, fine_num])
            print(fine_num, status, message)

            return render_template("fine.html", status=status, message=message)

        if action == "Добавить штраф":
            fio = request.form.get('fio')
            numer = request.form.get('numer')
            nomer = request.form.get('fine')
            reason = request.form.get('reason')
            summa = request.form.get('sum')

            if not all([fio, numer, nomer, reason, summa]):
                return render_template('fine.html')
            nomer = int(nomer)
            summa = int(summa)
            status, message = add_fine([fio, numer, nomer, reason, summa])
            return render_template("fine.html", status=status, message=message)

        return render_template('fine.html')

    except Exception as e:
        return render_template('fine.html')

@app.route('/transport', methods=['GET', 'POST'])
def transport():
    if request.method == 'GET':
        return render_template('transport.html')

    try:
        
        action = request.form.get('action')
        if action == "Удалить ТС":
            fio = request.form.get('dfio')
            vin = request.form.get('dVIN')
            mark = request.form.get('dmark')
            model = request.form.get('dmodel')
            date = request.form.get('dmade_date')
            color = request.form.get('dcolor')

            if not all([fio, vin, mark, model, date, color]):
                return render_template('transport.html')
            print(f"Удаление ТС: {fio}, {vin}, {mark}, {model}, {date}, {color}")

            status, message = del_transport([fio, vin, mark, model, date, color])

            return render_template("transport.html", status=status, message=message)

        if action == "Добавить ТС":
            fio = request.form.get('fio')
            vin = request.form.get('VIN')
            mark = request.form.get('mark')
            model = request.form.get('model')
            date = request.form.get('made_date')
            color = request.form.get('color')

            if not all([fio, vin, mark, model, date, color]):
                return render_template('transport.html')

            print(f"Добавление ТС: {fio}, {vin}, {mark}, {model}, {date}, {color}")


            status, message = add_transport([fio, vin, mark, model, date, color])

            return render_template("transport.html", status=status, message=message)

        return render_template('transport.html')

    except Exception as e:
        return render_template('transport.html')


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)