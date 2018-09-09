import dash

app = dash.Dash()
server = app.server
app.config.suppress_callback_exceptions = True
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/dZVMbK.css'})
# app.css.append_css({'external_url':'https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css'})
app.css.append_css({'external_url':"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" })
