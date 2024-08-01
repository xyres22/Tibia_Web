from flask import Flask, render_template,request,redirect,url_for,session
import requests
from api import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'DsdDFASDSFsddsf'



@app.route('/', methods=['GET','POST'])
def home():
    session.clear()
    news = latest_news()
    newsticker = latest_newsticker()
    if news and newsticker:
        return render_template('home.html',latest_news=news,newsticker=newsticker)
    else:
        return render_template('home.html',alert = True)


vocation = ['None','Knight','Paladin','Sorcerer','Druid']
category = ['Achievements','Axe Fighting','Charm Points','Club Fighting','Distance Fighting','Experience','Fishing','Fist Fighting',"Goshnar's Taint",'Loyalty Points','Magic Level','Shielding','Sword Fighting','Drome Score','Boss Points']
@app.route('/highscores',methods=['GET','POST'])
def index():
    world_lst = world_list()
    world='all'
    check_api = highscores(world ='all')
    select_cat = 'Experience'
    selected_page = int(request.args.get('page', 1))
    if world_lst and check_api:    
        if request.method == 'POST':
            world = request.form.get('world')
            cat = request.form.get('category').replace(' ','')
            voc = request.form.get('vocation')
            select_cat = request.form.get('category')
            session['world'] = world
            session['voc'] = voc
            session['cat'] = cat   
            session['select_cat'] = select_cat   
            selected_page = 1  

            info = highscores(world,cat,voc)
            return render_template('top1000.html', lst = info,    cat_list=category,   selected_cat = select_cat,    wrld = world_lst,    selected_world = world,    selected_voc = voc,     voc_list = vocation,  selected_page= selected_page,  highscores = info)
        else:
            world = session.get('world', 'all')
            voc = session.get('voc', 'all')
            cat = session.get('cat', 'Experience')   
            select_cat = session.get('select_cat', 'Experience')
            main_info = highscores(world,cat,voc,page = selected_page)

            return render_template('top1000.html', lst = main_info,cat_list=category,wrld = world_lst,selected_cat = select_cat,voc_list = vocation,selected_page=selected_page,selected_world=world,selected_voc = voc)
    else:
        return render_template('top1000.html',alert = True)


@app.route('/worlds', methods=['GET','POST'])
def worlds_page():
    data_worlds = worlds_table()
    if data_worlds:
        data_worlds = data_worlds['worlds']
        online = data_worlds['players_online']
        record = data_worlds['record_players']
        record_date = data_worlds['record_date']
        record_date = datetime.strptime(record_date, "%Y-%m-%dT%H:%M:%SZ")
        return render_template('worlds.html',world_online_list = data_worlds, players_online = online, record=record, record_date = record_date )
    else:
        return render_template('worlds.html', alert = True)

@app.route('/world/<name>',methods=['GET','POST'])
def world_details(name): 
    world_table = world_details_api(name)
    if world_table:
        return render_template('world_details.html',world_table = world_table, name=name)
    else:
        return render_template('world_details.html',alert=True,world_table = world_table, name=name)


@app.route('/guild/<guild_name>',methods=['GET','POST'])
def guild_page(guild_name):
    #guild_name = request.args.get('guildName', '')
    guild = guild_info(guild_name)
    if guild:
        if guild == 'Invalid status':
            return render_template('search_guild.html',alert = True)
        else:
            return render_template('guild.html',main_guild_name = guild_name,guild_info = guild)
    else:
        return render_template('guild.html', alert = True,main_guild_name = guild_name,guild_info = guild)
    

@app.route('/search_guild/',methods=['GET','POST'])
def search_guild():
    if request.method == 'POST':
        name = request.form.get('search_guild_name')
        if guild_info(name):
            if guild_info(name) == 'Invalid status':
                return render_template('search_guild.html',alert = True, name=name)
            else:

                return redirect(url_for('guild_page',guild_name = name))
        else:
            return render_template('search_guild.html',alert_page = True,guild_name = name)
    else:
        return render_template('search_guild.html', alert = False)
    

@app.route('/calculators', methods=['GET','POST'])
def calculators():
    return render_template('calculators.html')


@app.route('/search_character',methods=['GET','POST'])
def search_character_page():
    if request.method == 'POST':
        char_name = request.form.get('search_char_name')
        if char_details(char_name):
            if char_details(char_name) == 'Invalid status':
                return render_template('search_character.html', alert=True, name=char_name)
            else:
                return redirect(url_for('character_page', name=char_name))
        else:
            return render_template('search_character.html', alert_page=True, name=char_name)
    else:
        return render_template('search_character.html')

@app.route('/character/<name>',methods=['GET','POST'])
def character_page(name):
    char_info = char_details(name)
    if char_info:
        if char_info == 'Invalid status':
            return render_template('search_character.html', alert = True)
        else:
            return render_template('character.html',name=char_info)
    else:
        return render_template('character.html',alert = True, name=char_info)

    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)