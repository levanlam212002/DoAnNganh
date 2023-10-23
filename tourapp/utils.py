import json, os
from tourapp import app, db
from tourapp.models import DanhMuc, Tour, KhachHang, QuanTriVien, UserRole, HoaDon, ChiTietHoaDon, HinhAnh
import hashlib

from functools import wraps
from flask_login import current_user
from flask import redirect
from sqlalchemy import func, extract

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_categories():
    return DanhMuc.query.all()


def load_product(cate_id=None, kw=None, from_price=None, to_price=None):
    products = Tour.query.filter(Tour.Gia.__ge__(0))
    if cate_id:
        products = products.filter(Tour.DanhMuc_id.__eq__(cate_id))
    if kw:
        products = products.filter(Tour.TenTour.contains(kw))
    if from_price:
        products = products.filter(Tour.Gia.__ge__(from_price))
    if to_price:
        products = products.filter(Tour.Gia.__le__(to_price))
    if from_price and to_price:
        products = products.filter(Tour.Gia.__le__(to_price) & Tour.Gia.__ge__(from_price))
    return products



def get_product_by_id(product_id):
    return Tour.query.get(product_id)


def load_image(product_id):
    return HinhAnh.query.filter(HinhAnh.Tour_id.__eq__(product_id))


def add_bill(pay_date, total, user_id):
    user = HoaDon(NgayThanhToan=pay_date,
                  TongTien=total, TrangThai=True, KhachHang_id=user_id)

    db.session.add(user)
    db.session.commit()


def add_bills(number, tour_id, bill_id):
    bills = ChiTietHoaDon(SoLuongNguoiThamGia=number, Tour_id=tour_id, HoaDon_id=bill_id)

    db.session.add(bills)
    db.session.commit()


def get_bill_by_user_id(user_id):
    bills = HoaDon.query.filter(HoaDon.TrangThai.__eq__(True))

    if user_id:
        bills = bills.filter(HoaDon.KhachHang_id.__eq__(user_id))
    return bills


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = KhachHang(TenKH=name.strip(),
                TenDangNhap=username.strip(),
                MatKhau=password,
                Email=kwargs.get('email'),
                SDT=kwargs.get('sdt'),
                DiaChi=kwargs.get('dc'),
                CCCD=kwargs.get('cccd'))
    db.session.add(user)
    db.session.commit()


def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return KhachHang.query.filter(KhachHang.TenDangNhap.__eq__(username.strip()),
                                 KhachHang.MatKhau.__eq__(password)).first()


def check_user(username, password, role=UserRole.USER):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return KhachHang.query.filter(KhachHang.TenDangNhap.__eq__(username.strip()),
                             KhachHang.MatKhau.__eq__(password),
                             KhachHang.user_role.__eq__(role)).first()

def check_admin(username, password, role=UserRole.ADMIN):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return QuanTriVien.query.filter(QuanTriVien.TenDangNhap.__eq__(username.strip()),
                             QuanTriVien.MatKhau.__eq__(password),
                             QuanTriVien.user_role.__eq__(role)).first()

def get_user_by_id(user_id):
    return KhachHang.query.get(user_id)

def get_user_by_username(username):
    return KhachHang.query.filter(KhachHang.TenDangNhap.__eq__(username))

def anmonymous_user(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect('/')
        return f(*args, **kwargs)

    return decorated_func


def stats_revenue(month=None):
    query = db.session.query(HoaDon.NgayThanhToan,KhachHang.id, func.sum(HoaDon.TongTien))\
                      .join(HoaDon, HoaDon.KhachHang_id.__eq__(KhachHang.id))

    if month:
        query = query.filter(extract('month', HoaDon.NgayThanhToan).__eq__(month))

    return query.group_by(HoaDon.NgayThanhToan, KhachHang.id).all()


def total_revenue(month = None):
    query = db.session.query(func.sum(HoaDon.TongTien))

    if month:
        query = query.filter(extract('month', HoaDon.NgayThanhToan).__eq__(month))

    return query.all()


def count_tour_by_cate(month = None):
    query = db.session.query(Tour.TenTour,Tour.Gia, func.count(ChiTietHoaDon.Tour_id))\
            .join(ChiTietHoaDon, ChiTietHoaDon.Tour_id.__eq__(Tour.id), isouter=True)
    if month:
        query = query.filter(extract('month', HoaDon.NgayThanhToan).__eq__(month))

    return query.group_by(Tour.TenTour, Tour.Gia).all()


def update_pass(username,p):
    p = str(hashlib.md5(p.strip().encode('utf-8')).hexdigest())
    KhachHang.query.filter_by(TenDangNhap=username).first().MatKhau = p
    db.session.commit()