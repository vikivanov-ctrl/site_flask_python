from flask import Flask,render_template, request,session,copy_current_request_context
from vsearch import search4leters
from DBcm import UseDatabase,ConnectionError,CredentialsError,SQLError
from checker import check_logged_in
from threading import Thread


app=Flask(__name__)
app.secret_key="Cumshotic"

app.config['dbconfig']={'host':'127.0.0.1','port':'3306',
              'user':'user','password':'25143',
              'database':'vsearchlogDB',}

@app.route('/login') 
def do_login() -> str: 
    session['logged_in'] = True 
    return 'You are now logged in.'

@app.route('/logout')
def do_logout() -> str:
   session.pop('logged_in')
   return 'You are now logged out.'



@app.route('/search4', methods=['POST'])
def do_search() ->'html':
    @copy_current_request_context
    def log_request(req: 'flask_request',res: str) ->None:
        req.user_agent.browser='Yandex'
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """insert into log (phrase,letters,ip,browser_string,results)
                    values(%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL,(req.form['phrase'], req.form['letters'], 
                                req.remote_addr, req.user_agent.browser, res))

        return
    
    phrase=request.form['phrase']
    letters=request.form['letters']
    title='Here are your results'
    results =str(search4leters(phrase,letters))
    try:
        t=Thread(target=log_request,args=(request,results))
        t.start()
    except Exception as err:
        print('**** Logging failed with this erroe',str (err))

    return render_template('results.html',the_title=title,
                           the_phrase=phrase,the_letters=letters,the_results=results)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
@check_logged_in
def view_the_log() ->'html': 
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log"""
            cursor.execute(_SQL)
            contents=cursor.fetchall()

        titles=('Phrase','Letters','Form Data', 'Remote_addr', 'User_agent','Results')
        return render_template('viewlog.html',
                                the_title='View Log',
                                the_row_titles=titles,
                                the_data=contents,)
    except ConnectionError as err:
        print('Is your database switched on? Error:',str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:',str(err))
    except SQLError as err:
        print('Is your query correct? Error:',str(err))
    except Exception as err:
        print('Something went wrong:', str)
    return 'Error'



if __name__=="__main__":
    app.run(debug=True)