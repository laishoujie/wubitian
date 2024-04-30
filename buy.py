from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import MySQLdb
import os
import sys
import importlib
@app.route('/myOrder',methods=['GET', 'POST'])
def shoppingCartPage():
    global sum
    global restaurant
    global orderID
    if request.method == 'GET':
        print("myOrder-->GET")
        db = MySQLdb.connect("localhost", "root", "1234", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # 查询
        sql = "SELECT * FROM SHOPPINGCART"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        sum = len(res)
        if len(res) != 0:
            msg = "done"
            # print(msg)
            # print(len(res))
            return render_template('myOrder.html', username=username, result=res, messages=msg,sum=sum)
        else:
            print("NULL")
            msg = "none"
            return render_template('myOrder.html', username=username, messages=msg,sum=0)
    elif request.form["action"] == "加入购物车":
        print("myOrder-->加入购物车")
        restaurant = request.form['restaurant']
        dishname = request.form['dishname']
        price = request.form['price']
        img_res = request.form['img_res']
        db = MySQLdb.connect("localhost", "root", "1234", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql1 = "insert into shoppingcart values ('{}','{}','{}','{}','{}') ".format(username, restaurant, dishname, price, img_res)
        cursor.execute(sql1)
        db.commit()
        res1 = cursor.fetchall()
        print(len(res1))
        sql = "SELECT * FROM shoppingcart"
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            sum = len(res)
            return render_template('myOrder.html', username=username, result=res, messages=msg,sum=sum)
        else:
            print("NULL")
            msg = "none"
        return render_template('myOrder.html', username=username, messages=msg,sum=0)

    elif request.form["action"] == "购买":
        print("myOrder-->购买")
        restaurant = request.form['restaurant']
        dishname = request.form['dishname']
        price = request.form['price']
        sales = request.form['sales']
        sales = int(sales)+1
        img_res = request.form['img_res']
        db = MySQLdb.connect("localhost", "root", "1234", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "SELECT * FROM order_comment"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        orderID=len(res)+1
        # sql2 = "Update dishes SET sales = '{}' where dishname = '{}' and restaurant = '{}'".format(sales, dishname, restaurant)
        # cursor.execute(sql2)
        # db.commit()
        # except:
        #     print("Error: unable to use database!")
        sql1 = "insert into ORDER_COMMENT (orderID,username,dishname,cost,imgsrc,isFinished,restaurant) " \
               "values ('{}','{}','{}','{}','{}','{}','{}') ".format(orderID,username, dishname, price, img_res,0,restaurant)
        try:
            cursor.execute(sql1)
            db.commit()
        except Exception as e:
            print("Error: unable to use database!")
            print(str(e))
        sql2 = "Update dishes SET sales = '{}' where dishname = '{}' and restaurant = '{}'".format(sales, dishname,
                                                                                                   restaurant)
        cursor.execute(sql2)
        db.commit()
        # res1 = cursor.fetchall()
        # print(len(res1))
        # 查询
        sql = "SELECT * FROM DISHES WHERE restaurant = '%s'" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            msg1="yes"
            print(msg1)
            print(len(res))
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg,message1=msg1)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "结算":
        print("结算啦")
        restaurant = request.form['restaurant']
        print(restaurant)
        dishname = request.form['dishname']
        price = request.form['price']
        img_res = request.form['img_res']
        mode = request.form['mode']
        db = MySQLdb.connect("localhost", "root", "1234", "appDB", charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # restuarant = request.form['restaurant']
        # print(restuarant)
        # dishname = request.form['dishname']
        # price = request.form['price']
        # img_res = request.form['img_res']
        # mode = request.form['mode']
        print("==*==")
        print(mode)
        if mode == 1:
            print("堂食")

        else:
            print("外送")
        return render_template('index.html')
    # elif request.form["action"] == "查看营养成分":
    #     dishname = request.form['dishname']
    #     print(dishname)
    #     msg = ""
    #     # 连接数据库，默认数据库用户名root，密码空
    #     db = MySQLdb.connect("localhost", "root", "1234", "appDB", charset='utf8')
    #     cursor = db.cursor()
    #     try:
    #         cursor.execute("use appDB")
    #     except:
    #         print("Error: unable to use database!")
    #     # 查询
    #     sql = "SELECT * FROM DISHES WHERE dishname = '%s'" % dishname
    #     cursor.execute(sql)
    #     res = cursor.fetchall()
    #     # print(res)
    #     # print(len(res))
    #     if len(res) != 0:
    #         msg1 = "see"
    #         msg = "done"
    #         print(msg)
    #         print(len(res))
    #         return render_template('Menu.html', username=username, dishname=dishname, result1=res, messages1=msg1,messages=msg)
    #     else:
    #         print("NULL")
    #         msg = "done"
    #         msg1 = "none"
    #         return render_template('Menu.html', username=username, dishname=dishname, messages1=msg1,messages=msg)
    else:
        print("咋回事")
        return render_template('index.html')