from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL

 
app = Flask(__name__, template_folder = 'templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ibukun33'
app.config['MYSQL_DB'] = 'bincom'

mysql = MySQL(app)

@app.route('/' , methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        uniquepolid = request.form
        uid = uniquepolid['upi']
        cur = mysql.connection.cursor()


        select_polling_unit_uniqueid = """SELECT polling_unit_uniqueid FROM announced_pu_results"""
        cur.execute(select_polling_unit_uniqueid)
        idpol = cur.fetchall()
        ids = [item for t in idpol for item in t]
        
        select_party_abbreviation = """SELECT party_abbreviation FROM announced_pu_results"""
        cur.execute(select_party_abbreviation)
        partyname = cur.fetchall()
        names = [item for t in partyname for item in t]
        dicts = {key: [] for key in names}
        for k, v in zip(names, ids):
            dicts[k].append(v)

        keyslist = list(dicts.values())

        select_party_score = """SELECT party_score FROM announced_pu_results"""
        cur.execute(select_party_score)
        partyscore = cur.fetchall()
        scores = [item for t in partyscore for item in t]

        dicts2 = {key: [] for key in names}
        for k, v in zip(names, scores):
            dicts2[k].append(v)
            
        vallist = list(dicts2.values())

        oya = []
        shee=[]
        def getindex(inp):
            for i in keyslist:
                if inp in i:
                    index_pos_list = get_index_positions(keyslist, i)
                    for a in list(index_pos_list):
                        shee.append(a)
            return(set(shee))
        def okay(sets, inp):
            for i in sets:
                if inp in i:
                    oya.append([i.index(inp)])
            return(oya)

        def get_index_positions(list_of_elems, element):
            
            index_pos_list = []
            index_pos = 0
            while True:
                try:
                    # Search for item in list from indexPos to the end of list
                    index_pos = list_of_elems.index(element, index_pos)
                    # Add the index position in list
                    index_pos_list.append(index_pos)
                    index_pos += 1
                except ValueError as e:
                    break
            return index_pos_list
        listc = []
        def get_keys_from_value(dicts,val):
            return [k for k, v in dicts.items() if val in v]
        def donezo(oyao):
            for i in oyao:
                listc.append(vallist[i[0]][i[1]])
            return listc

        keys = get_keys_from_value(dicts, uid)
        indexx = getindex(uid)
        yo = okay(keyslist, uid)

        result = [] 
        for i in yo: 
            if i not in result: 
                result.append(i) 
        keys = get_keys_from_value(dicts, uid)
        flat_list = [item for sublist in yo for item in sublist]
        list_c = [[x, y] for x, y in zip(list(indexx),flat_list)]
        doneo = donezo(list_c)

        
        

        res = "\n".join("{:} {:}".format(x, y) for x, y in zip(keys,doneo))
        
        mysql.connection.commit()
        cur.close()
        return render_template('results.html', variable= res)

                

    return render_template('index.html')

 
if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)
