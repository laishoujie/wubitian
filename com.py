from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import MySQLdb
import os
import sys
import importlib


# 商家修改菜品信息
@app.route('/MenuModify', methods=['GET', 'POST'])
def MenuModify():
    msg = ""

    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "修改菜品信息":
        dishname = request.form['dishname']  # 传递过去菜品名
        rest = request.form['restaurant']  # 传递过去商家名
        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = request.form.get('isSpecialty')
        # imagesrc = request.form['imagesrc']
        print(dishname)
        print(isSpecialty)
        print(type(isSpecialty))

        return render_template('MenuModify.html', dishname=dishname, rest=rest, dishinfo=dishinfo,
                               nutriention=nutriention, price=price, username=username, messages=msg,
                               isSpecialty=isSpecialty)
    elif request.form["action"] == "提交修改":

        dishname = request.form.get('dishname')
        rest = request.form.get('rest')

        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = int(request.form.get('isSpecialty'))
        f = request.files['imagesrc']
        filename = ''

        if f != '' and allowed_file(f.filename):
            filename = secure_filename(f.filename)

        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename

        print(isSpecialty)
        print(type(isSpecialty))
        db = MySQLdb.connect("localhost", "root", "1234", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        if filename == '':
            sql = "Update dishes SET dishinfo = '{}', nutriention = '{}', price = {} , isSpecialty = {} where dishname = '{}' and restaurant = '{}'".format(
                dishinfo, nutriention, price, isSpecialty, dishname, rest)
        else:
            sql = "Update dishes SET dishinfo = '{}', nutriention = '{}', price = {} ,imagesrc = '{}', isSpecialty = {} where dishname = '{}' and restaurant = '{}'".format(
                dishinfo, nutriention, price, imgsrc, isSpecialty, dishname, rest)
        print(sql)

        try:
            cursor.execute(sql)
            db.commit()
            print("菜品信息修改成功")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("菜品信息修改失败失败")
            msg = "fail"
        return render_template('MenuModify.html', dishname=dishname, rest=rest, username=username, messages=msg)


@app.route('/MenuAdd', methods=['GET', 'POST'])
def MenuAdd():
    msg = ""
    rest = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "增加菜品":
        rest = request.form['restaurant']  # 传递过去商家名
        return render_template('MenuAdd.html', rest=rest)
    elif request.form["action"] == "确认增加":
        dishname = request.form.get('dishname')
        rest = request.form.get('rest')
        dishinfo = request.form.get('dishinfo')
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        f = request.files['imagesrc']
        print(f)
        isSpecialty = int(request.form.get('isSpecialty'))
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
        db = MySQLdb.connect("localhost", "root", "1234", "appDB", charset='utf8')

        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql1 = "SELECT * from DISHES where dishname = '{}' ".format(dishname)
        cursor.execute(sql1)
        db.commit()
        res1 = cursor.fetchall()
        num = 0
        for row in res1:
            num = num + 1
        # 如果已经存在该商家
        if num == 1:
            print("失败！该菜品已经添加过！")
            msg = "fail1"
        else:
            sql2 = "insert into DISHES  values ('{}', '{}','{}', '{}',{}, {},'{}', {}) ".format(dishname, rest,
                                                                                                dishinfo, nutriention,
                                                                                                price, 0, imgsrc,
                                                                                                isSpecialty)
            print(sql2)
            try:
                cursor.execute(sql2)
                db.commit()
                print("菜品添加成功")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("菜品添加失败")
                msg = "fail"
        return render_template('MenuAdd.html', messages=msg, username=username)
