import code
import smtplib
import string
from random import Random, random
from datetime import date

import paypalrestsdk
from flask import render_template, request, redirect, url_for,jsonify, session

import utils
from tourapp import app,login
from flask_login import login_user,logout_user
from tourapp.models import UserRole

@app.route("/")
def home():
    cats = utils.load_categories()
    products = utils.load_product()
    return render_template("index.html", categories=cats,
                           products=products)


@app.route("/products")
def product_list():
    cate_id = request.args.get("category_id")
    kw = request.args.get("Keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    cates = utils.load_categories()
    products = utils.load_product(cate_id=cate_id,
                                  kw=kw, from_price=from_price, to_price=to_price)
    return render_template("products.html", products=products, categories=cates)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    cates = utils.load_categories()
    products = utils.get_product_by_id(product_id)
    images = utils.load_image(product_id)
    return render_template("product_detail.html", products=products, categories=cates, images=images)


@app.route("/pay/<int:product_id>")
def pay_product(product_id):
    cates = utils.load_categories()
    products = utils.get_product_by_id(product_id)

    return render_template("pay.html", products=products, categories=cates)


@app.route('/payment/<product_id>', methods=['GET', 'POST'])
def payment(product_id):
    msg = ''
    if request.method.__eq__('POST'):
        amount_young = request.form['amount_young']
        product_id = product_id
        user_id = current_user.id
        price_young = request.form['price_young']
        session['price'] = (float(price_young) * float(amount_young))

        # Tạo một Payment với các thông tin cần thiết
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "transactions": [{
                "amount": {
                    "total": session['price'],
                    "currency": "USD"
                },
                "description": "Mua hàng trên Flask Shop"
            }],
            "redirect_urls": {
                "return_url": url_for('success', _external=True),
                "cancel_url": url_for('pay_product', product_id=product_id, _external=True)
            }
        })

        # Lưu thông tin Payment
        if payment.create():
            # Lưu Payment ID vào session
            session['payment_id'] = payment.id
            # Redirect user đến trang thanh toán của PayPal
            for link in payment.links:
                if link.method == 'REDIRECT':
                    redirect_url = str(link.href)
                    try:
                        utils.add_bill(
                                       pay_date=date.today(),
                                       user_id=user_id,
                                       total=session['price'])
                        bill_id = utils.get_bill_by_user_id(user_id)[-1].id
                        utils.add_bills(number=amount_young,
                                        tour_id=product_id,
                                        bill_id=bill_id)
                    except:
                        print("Lỗi")
                    return redirect(redirect_url)
        else:
            return "Lỗi trong quá trình tạo Payment"

@app.route('/success')
def success():

    # Lấy Payment ID từ session
    payment_id = session.get('payment_id')

    # Xác nhận thanh toán với PayPal
    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):

        # Thanh toán thành công, hiển thị trang hoàn tất thanh toán

        return redirect(url_for('home'))
    else:
        return "Lỗi trong quá trình xác nhận thanh toán"

@app.route('/pay_history/<int:user_id>')
def pay_history(user_id):
    bills = utils.get_bill_by_user_id(user_id=user_id)
    return render_template('pay_history.html', bills=bills)




#dky
@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        sdt = request.form.get('sdt')
        cccd = request.form.get('cccd')
        dc = request.form.get('dc')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_user(name=name, username=username, password=password, email=email, sdt=sdt, cccd=cccd, dc=dc)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mật khẩu không khớp'
        except Exception as ex:
            err_msg = 'Tên đăng nhập đã tồn tại'

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login',methods=['get','post'])
def user_signin():
    err_msg=''
    if request.method.__eq__('POST'):
        username=request.form.get('username')
        password = request.form.get('password')

        user = utils.check_user(username=username,password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg='Tên đăng nhập hoặc mật khẩu không chính xác'

    return render_template('login.html',err_msg=err_msg)


@login.user_loader
def user_load(user_id):
    return  utils.get_user_by_id(user_id=user_id)

@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))




@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user=utils.check_admin(username=username,
                            password=password,
                            role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/forget-password',methods=['get','post'])
def forget_password():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        email = utils.get_user_by_username(username)[0].Email
        user = 'thanhtoanpaypalonline@gmail.com'
        password = 'kdgfnhszhmlisgfk'
        val= '518751'
        mssg = val
        client = smtplib.SMTP("smtp.gmail.com",587)
        client.starttls()
        client.login(user,password)
        client.sendmail(user,email,mssg)
        client.quit()
        msg = 'Mã code đã được gửi đến email bạn đăng ký.'
        return render_template('code.html',msg=msg)
    return render_template('forgetPassword.html')


@app.route('/code',methods=['get','post'])
def code():
    msg=''
    if request.method.__eq__('POST'):
        code = request.form.get('code')
        if(code.__eq__('518751')):
            return render_template('pass.html')
        else:
            msg='Bạn đã nhập sai code!!!'
    return render_template('code.html',msg=msg)

@app.route('/pass-register', methods=['get', 'post'])
def pass_register():
    mgs = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                utils.update_pass(username=username,p=password)
                return redirect(url_for('user_signin'))
            else:
                mgs = 'Mật khẩu không khớp'
        except Exception as ex:
            mgs = 'Hệ thống đang lỗi!!!' + str(ex)

    return render_template('pass.html', mgs=mgs)

@app.route('/admin1',methods=['get','post'])
def admin1():
    return redirect('/admin')



if __name__ == '__main__':
    from tourapp.admin import *
    app.run(debug=True)
