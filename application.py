import os
from flask import Flask, url_for, request, redirect, render_template
import logging
import json
import requests
import model

app = application = Flask(__name__)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


@app.route('/')
def index():
    app.logger.debug('application.py index BEGIN')
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'], defaults={'error': None})
@app.route('/login/<string:error>', methods=['GET', 'POST'])
def login_app(error=None):
    app.logger.debug('application.py login BEGIN')
    app.logger.info('application.py login error: %s', error)
    context = {'error': error}
    if request.method == 'POST':
        app.logger.info("login POST request: %s %s", request.form['email'], request.form['password'])
        login_validation = model.authenticate_login(request.form['email'], request.form['password'])
        app.logger.info('application.py login validation: %s', login_validation)
        if login_validation:
            return redirect(url_for('main', auth_id=model.encrypt(login_validation)))
        else:
            error = "Email or password is invalid"
            context = {'error': error}
    app.logger.info('application.py login context: %s', context)
    app.logger.debug('application.py login END')
    return render_template('login.html', context=context)


@app.route('/register', methods=['GET', 'POST'], defaults={'error': None})
@app.route('/register/<string:error>', methods=['GET', 'POST'])
def register(error=None):
    app.logger.debug('application.py register BEGIN')
    app.logger.info('application.py register error: %s', error)
    context = {'error': error}
    if request.method == 'POST':
        app.logger.info("login POST request: %s %s", request.form['email'], request.form['password'])
        err, new_user = model.register_new_user(request.form['email'], request.form['password'])
        app.logger.info('application.py register_new_user: %s', err)
        if not new_user:
            context = {'error': err}
        else:
            return redirect(url_for('login_app', error='Registration successful. Try logging in'))
    app.logger.info('application.py register context: %s', context)
    app.logger.debug('application.py register END')
    return render_template('register.html', context=context)


@app.route('/main', methods=['GET', 'POST'], defaults={'auth_id': None})
@app.route('/main/<string:auth_id>', methods=['GET', 'POST'])
def main(auth_id=None, error=None):
    app.logger.debug('application.py main BEGIN')
    app.logger.info('application.py main error: %s', error)
    context = {'error': error}
    if auth_id is None:
        return redirect(url_for('login_app', error='Auth ID error from Main'))
    auth_id_decrypted = model.decrypt(auth_id)
    if auth_id_decrypted is None:
        return redirect(url_for('login_app', error='Auth ID error from Profile login error'))
    if request.method == 'POST':
        app.logger.info("login POST request: %s", request)
        if request.form.get('form_type') == 'currency_exchange_box':
            amount = request.form.get('amount')
            curr1 = request.form.get('curr1')
            curr2 = request.form.get('curr2')
            rate = model.currency_exchange(curr1, curr2)
            context['currency_exchange'] = str(amount) + ' ' + curr1 + ' to ' + curr2 + ' is ' + str(
                round(float(rate) * float(amount), 5)) + curr2
        elif request.form.get('form_type') == 'urban_dictionary':
            word = request.form.get('word')
            context['urban_dictionary_list'] = model.urban_dictionary(word)
            context['urban_dictionary_word'] = word
            # print(context['urban_dictionary_list'])
        else:
            context['error'] = "Invalid form action"
    print(auth_id_decrypted)
    user_dict = model.get_user_details(auth_id_decrypted)
    print(user_dict)
    if not user_dict.get('details_updated'):
        user_dict['details_updated'] = False
    context['user_details'] = user_dict
    context['auth_id'] = auth_id
    context['currency_exchange_list'] = model.get_currency_list()
    context['weather'] = model.forecast_weather()
    app.logger.info('application.py login context: %s', context)
    app.logger.debug('application.py login END')
    return render_template('main.html', context=context)


@app.route('/profile', methods=['GET', 'POST'], defaults={'auth_id': None})
@app.route('/profile/<string:auth_id>', methods=['GET', 'POST'])
def profile(auth_id=None, error=None):
    app.logger.debug('application.py profile BEGIN')
    app.logger.info('application.py profile error: %s', error)
    context = {'error': error}
    if auth_id is None:
        return redirect(url_for('login_app', error='Auth ID error from Profile'))
    auth_id_decrypted = model.decrypt(auth_id)
    if auth_id_decrypted is None:
        return redirect(url_for('login_app', error='Auth ID error from Profile login error'))
    if request.method == 'POST':
        app.logger.info("profile POST request: %s", request)
        if request.form.get('form_type') == 'new_password':
            if model.rds_user_table_change_password(auth_id_decrypted, request.form['old_password'],
                                                    request.form['new_password']):
                context['new_password_error'] = "Password change successful"
            else:
                context['new_password_error'] = "Wrong password"
        elif request.form.get('form_type') == 'college_preference':
            new_dict = {}
            cname = ""
            cyear = ""
            csem = ""
            cohorts = []
            if request.form.get('college_name'):
                new_dict['college_name'] = request.form.get('college_name')
                cname = str(new_dict['college_name']).strip().lower().replace(' ', '-')
            if request.form.get('college_year'):
                new_dict['college_year'] = request.form.get('college_year')
                cyear = str(new_dict['college_year']).strip().lower().replace(' ', '-')
            if request.form.get('college_semester'):
                new_dict['college_semester'] = request.form.get('college_semester')
                csem = str(new_dict['college_semester']).strip().lower().replace(' ', '-')
            if request.form.getlist('college_subjects'):
                new_dict['college_subjects'] = request.form.getlist('college_subjects')
                for i in new_dict['college_subjects']:
                    coho = i.strip().lower().replace(' ', '-')
                    cohorts.append(cname + '-' + cyear + '-' + csem + '-' + coho)
                cohorts.append(cname + '-' + cyear + '-' + csem)
            new_dict['uid'] = auth_id_decrypted
            new_dict['details_updated'] = True
            # print(request.form)
            # print(cohorts)
            new_dict['cohort_list'] = cohorts
            if model.check_cohorts(cohorts):
                if model.update_user_details(new_dict):
                    context['college_preference_error'] = "Details change successful"
                else:
                    context['college_preference_error'] = "NO change"
            else:
                context['college_preference_error'] = "ERROR"
        elif request.form.get('form_type') == 'personal_details':
            new_dict = {}
            if request.form.get('name'):
                new_dict['name'] = request.form.get('name')
            if request.form.get('student_id'):
                new_dict['student_id'] = request.form.get('student_id')
            new_dict['uid'] = auth_id_decrypted
            # print(request.files.get('img'))
            if request.files.get('img'):
                file_dest = auth_id_decrypted + '.jpg'
                # f = open('./tmp/user.jpg', 'w')
                f = request.files['img']
                f.save('/home/ec2-user/images/' + auth_id_decrypted + '.jpg')
                f.close()
                if model.upload_user_image_s3(auth_id_decrypted):
                    user_image = 'https://unimate-user-s3.s3.ap-southeast-2.amazonaws.com/user-images/' + file_dest
                    new_dict['user_image'] = user_image
                else:
                    context['user_details_error'] = "Details not changed"
                    return
                os.remove('/home/ec2-user/images/' + auth_id_decrypted + '.jpg')
            if model.update_user_details(new_dict):
                context['user_details_error'] = "Details change successful"
            else:
                context['user_details_error'] = "Details not changed"
        else:
            context['error'] = "Invalid form action"

    auth_id_decrypted = model.decrypt(auth_id)
    user_dict = model.get_user_details(auth_id_decrypted)
    if 'details_updated' not in user_dict:
        user_dict['details_updated'] = False
    context['user_details'] = user_dict
    context['auth_id'] = auth_id
    context['uni_list'] = model.dynamodb_system_get_university_list()
    context['subject_list'] = model.dynamodb_system_get_subject_list()
    app.logger.info('application.py profile context: %s', context)
    app.logger.debug('application.py login END')
    return render_template('profile.html', context=context)


@app.route('/chatbot', defaults={'auth_id': None})
@app.route('/chatbot/<string:auth_id>')
def chatbot(auth_id=None):
    app.logger.debug('application.py chatbot BEGIN')
    if auth_id is None:
        return redirect(url_for('login_app', error='Auth ID error from Profile'))
    auth_id_decrypted = model.decrypt(auth_id)
    if auth_id_decrypted is None:
        return redirect(url_for('login_app', error='Auth ID error from Profile login error'))
    context = {'auth_id': auth_id}
    user_dict = model.get_user_details(auth_id_decrypted)
    context['user_details'] = user_dict
    app.logger.debug('application.py chatbot END')
    return render_template('bot.html', context=context)


@app.route('/get_cohort_data', defaults={'cohort_id': None})
@app.route('/get_cohort_data/<string:cohort_id>')
def get_cohort_data(cohort_id=None):
    new_dict = {}
    new_dict['cohort_id'] = cohort_id
    response = requests.post("https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/get-cohort",
                             data=json.dumps(new_dict))
    # print(response.content.decode())
    logging.debug('model.py rds_user_table_put END')
    if 'success' in response.content.decode():
        response_dict = json.loads(response.content.decode())
        return json.dumps(response_dict.get('items'))
    return json.dumps("{'body':'false'}")


@app.route('/put_cohort_data/', defaults={'auth_id': None}, methods=['GET', 'POST'])
@app.route('/put_cohort_data/<string:auth_id>', methods=['GET', 'POST'])
def put_cohort_data(auth_id=None):
    if request.method == 'POST':
        req_dict = json.loads(request.data.decode())
        print(req_dict)
        auth_id_decrypted = model.decrypt(auth_id)
        user_dict = model.get_user_details(auth_id_decrypted)
        new_dict = {}
        new_dict['auth_id'] = auth_id
        new_dict['author_name'] = user_dict.get('name')
        new_dict['author_image'] = user_dict.get('user_image')
        new_dict['subject'] = req_dict.get('subject')
        new_dict['message'] = req_dict.get('message')
        new_dict['contact'] = user_dict.get('name')
        new_dict['cohort_id'] = req_dict.get('cohort_id')
        print(new_dict)
        response = requests.post("https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/put-cohort",
                                 data=json.dumps(new_dict))
        print(response.content.decode())
        return json.dumps(response.content.decode())

    # new_dict['cohort_id'] = cohort_id
    # response = requests.post("https://1lubspxlkd.execute-api.ap-southeast-2.amazonaws.com/dev/get-cohort",
    #                          data=json.dumps(new_dict))
    # print(response.content.decode())
    # logging.debug('model.py rds_user_table_put END')
    # if 'success' in response.content.decode():
    #     response_dict = json.loads(response.content.decode())
    #     return json.dumps(response_dict.get('items'))
    # return json.dumps("{'body':'false'}")
    return json.dumps("{'body':'false'}")


@app.route('/logout')
def logout():
    app.logger.debug('application.py logout BEGIN')
    app.logger.debug('application.py logout END')
    return redirect(url_for('login_app', error='Logged out'))


if __name__ == '__main__':
    app.logger.debug('app.py __main__ BEGIN')
    app.debug = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    model.settings()
    app.run()
