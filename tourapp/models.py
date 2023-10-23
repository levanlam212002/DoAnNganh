from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from tourapp import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

#dky
class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

#dky
class KhachHang(BaseModel, UserMixin):

    TenKH = Column(String(50), nullable=False)
    TenDangNhap = Column(String(50), nullable=False, unique=True)
    MatKhau = Column(String(50), nullable=False)
    Email = Column(String(50))
    SDT = Column(String(10))
    DiaChi = Column(String(50))
    CCCD = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    HoaDon = relationship('HoaDon', backref='KhachHang', lazy=False)

    def __str__(self):
        return self.TenKH

class QuanTriVien(BaseModel, UserMixin):

    TenQTV = Column(String(50), nullable=False)
    TenDangNhap = Column(String(50), nullable=False, unique=True)
    MatKhau = Column(String(50), nullable=False)
    NamSinh = Column(String(50))
    SDT = Column(String(10))
    DiaChi = Column(String(50))
    CCCD = Column(String(50))
    NgayVaoLam = Column(String(50))
    user_role = Column(Enum(UserRole), default=UserRole.ADMIN)

class DanhMuc(BaseModel):

    TenDanhMuc = Column(String(255), nullable=False)
    Tour = relationship('Tour', backref='DanhMuc', lazy=False)

    def __str__(self):
        return self.TenDanhMuc


class Tour(BaseModel):

    TenTour = Column(String(255), nullable=False)
    Gia = Column(Float, default=0)
    ThoiGianBatDau = Column(Date)
    ThoiGianKetThuc = Column(Date)
    DiaDiemBatDau = Column(String(100), nullable=False)
    DiaDiemKetThuc = Column(String(100), nullable=False)
    PhuongTienDiChuyen = Column(String(100), nullable=False)
    MoTa = Column(String(1000), nullable=True)
    DanhMuc_id = Column(Integer, ForeignKey(DanhMuc.id), nullable=False)
    ChiTietHoaDon_id = relationship('ChiTietHoaDon', backref='Tour', lazy=False)
    HinhAnh_id = relationship('HinhAnh', backref='Tour', lazy=False)

    def __str__(self):
        return self.TenTour

class HinhAnh(BaseModel):

    LinkHinhAnh =  Column(String(255))
    Tour_id = Column(Integer, ForeignKey(Tour.id), nullable=False)

class HoaDon(BaseModel):

    NgayThanhToan = Column(Date)
    TongTien = Column(Integer, nullable= False)
    TrangThai = Column(Boolean, nullable=False, default=True)
    KhachHang_id = Column(Integer, ForeignKey(KhachHang.id), nullable=False)
    ChiTietHoaDon_id = relationship('ChiTietHoaDon', backref='HoaDon', lazy=False)



class ChiTietHoaDon(BaseModel):

    SoLuongNguoiThamGia = Column(Integer)
    Tour_id = Column(Integer, ForeignKey(Tour.id), nullable=False)
    HoaDon_id = Column(Integer, ForeignKey(HoaDon.id), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        d1 = DanhMuc(TenDanhMuc='MIỀN BẮC')
        d2 = DanhMuc(TenDanhMuc='MIỀN TRUNG')
        d3 = DanhMuc(TenDanhMuc='MIỀN NAM')

        db.session.add_all([d1, d2, d3])
        db.session.commit()
        p1 = Tour(TenTour="DU LỊCH ĐẢO PHÚ QUỐC", Gia=241,
                     ThoiGianBatDau="2023-03-09", ThoiGianKetThuc="2023-03-13", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Phú Quốc", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=3)

        p2 = Tour(TenTour="DU LỊCH ĐÀ NẴNG", Gia=173,
                     ThoiGianBatDau="2023-03-09", ThoiGianKetThuc="2023-03-12", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Đà Nẵng", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=2)

        p3 = Tour(TenTour="DU LỊCH ĐÀ LẠT", Gia=67,
                     ThoiGianBatDau="2023-03-09", ThoiGianKetThuc="2023-03-13", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Đà Lạt", PhuongTienDiChuyen="Ôtô", MoTa='', DanhMuc_id=2)

        p4 = Tour(TenTour="Du LỊCH SAPA", Gia=305,
                     ThoiGianBatDau="2023-03-10", ThoiGianKetThuc="2023-03-14", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Điện Biên - SaPa", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=1)

        p5 = Tour(TenTour="DU LỊCH NHA TRANG", Gia=67,
                     ThoiGianBatDau="2023-03-11", ThoiGianKetThuc="2023-03-13", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Nha Trang", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=2)

        p6 = Tour(TenTour="DU LỊCH HẠ LONG",Gia=106,
                     ThoiGianBatDau="2023-03-14", ThoiGianKetThuc="2023-03-17", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Hạ Long", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=1)

        p7 = Tour(TenTour="DU LỊCH PHÚ YÊN", Gia=161,
                     ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-19", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Phú Yên - Tuy Hòa", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=3)

        p8 = Tour(TenTour="DU LỊCH HUẾ", Gia=466,
                     ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-21", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Huế", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=2)

        p9 = Tour(TenTour="DU LỊCH TÂY NGUYÊN", Gia=156,
                     ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-19", DiaDiemBatDau="TP. Hồ Chí Minh",
                     DiaDiemKetThuc="Tây Nguyên", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=2)

        p10 = Tour(TenTour="DU LỊCH MỸ THO", Gia=67,
                      ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-18", DiaDiemBatDau="TP. Hồ Chí Minh",
                      DiaDiemKetThuc="Mỹ Tho", PhuongTienDiChuyen="Ôtô", MoTa='', DanhMuc_id=3)

        p11 = Tour(TenTour="DU LỊCH HỘI AN", Gia=114,
                      ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-20",DiaDiemBatDau="TP. Hồ Chí Minh",
                      DiaDiemKetThuc="Hội An - Đà Nẵng", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=2)

        p12 = Tour(TenTour="DU LỊCH HÀ GIANG", Gia=254,
                      ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-20", DiaDiemBatDau="TP. Hồ Chí Minh",
                      DiaDiemKetThuc="Hà Giang", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=1)

        p13 = Tour(TenTour="DU LỊCH HÀ NỘI", Gia=106,
                      ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-20", DiaDiemBatDau="TP. Hồ Chí Minh",
                      DiaDiemKetThuc="Hà Nội", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=1)
        p14 = Tour(TenTour="DU LỊCH CẦN THƠ", Gia=63,
                      ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-18", DiaDiemBatDau="TP. Hồ Chí Minh",
                      DiaDiemKetThuc="Cần Thơ", PhuongTienDiChuyen="Ôtô", MoTa='', DanhMuc_id=3)

        p15 = Tour(TenTour="DU LỊCH BẮC NINH", Gia=152,
                      ThoiGianBatDau="2023-03-15", ThoiGianKetThuc="2023-03-20", DiaDiemBatDau="TP. Hồ Chí Minh",
                      DiaDiemKetThuc="Bắc Ninh", PhuongTienDiChuyen="Máy bay", MoTa='', DanhMuc_id=1)
        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15])
        db.session.commit()

        #
        u1 = KhachHang(TenKH='Huỳnh Minh Hoàng', TenDangNhap='hoang', MatKhau='202cb962ac59075b964b07152d234b70', Email='20172023218@gmail.com', SDT='0966287704', CCCD='29303983240', DiaChi='23 Lê Thị Hồng')
        u2 = KhachHang(TenKH='Thái Tấn Phát', TenDangNhap='phat', MatKhau='202cb962ac59075b964b07152d234b70',Email='phattan@ou.edu.vn', SDT='0123412234', CCCD='29719291792', DiaChi='37 Lê Văn Duyệt')
        u3 = KhachHang(TenKH='Lê Văn Lâm', TenDangNhap='lam', MatKhau='202cb962ac59075b964b07152d234b70', Email='levanlam@ou.edu.vn' , SDT='0926384628', CCCD='02808301280383', DiaChi='38 Hồ Hảo Hớn')
        u4 = KhachHang(TenKH='Nguyễn Thị Ngọc Yến', TenDangNhap='yen', MatKhau='202cb962ac59075b964b07152d234b70',Email='ngocyennguyen@ou.edu.vn', SDT='0234849204', CCCD='98397937493', DiaChi='83 Võ Văn Tần')
        db.session.add_all([u1, u2, u3, u4])
        db.session.commit()

        q1 = QuanTriVien(TenQTV='Nguyễn Thị Thanh', TenDangNhap='admin', MatKhau='202cb962ac59075b964b07152d234b70',NamSinh='2002-02-01', SDT='0966123312', CCCD='20920091202', DiaChi='21 Võ Văn Tần', NgayVaoLam='2022-09-13')
        db.session.add(q1)
        db.session.commit()

        b1 = HoaDon(NgayThanhToan="2023-02-20", TongTien=452, KhachHang_id=1)

        b2 = HoaDon(NgayThanhToan="2023-01-12", TongTien=939, KhachHang_id=2)

        b3 = HoaDon(NgayThanhToan="2023-02-21", TongTien=639, KhachHang_id=1)

        b4 = HoaDon(NgayThanhToan="2023-02-21", TongTien=6070, KhachHang_id=3)

        b5 = HoaDon(NgayThanhToan="2023-01-08", TongTien=358, KhachHang_id=3)
        db.session.add_all([b1, b2, b3, b4, b5])
        db.session.commit()

        c1 = ChiTietHoaDon(SoLuongNguoiThamGia=2, Tour_id=1, HoaDon_id=1)
        c2 = ChiTietHoaDon(SoLuongNguoiThamGia=3, Tour_id=4, HoaDon_id=2)
        c3 = ChiTietHoaDon(SoLuongNguoiThamGia=1, Tour_id=7, HoaDon_id=3)
        c4 = ChiTietHoaDon(SoLuongNguoiThamGia=4, Tour_id=1, HoaDon_id=4)
        c5 = ChiTietHoaDon(SoLuongNguoiThamGia=2, Tour_id=3, HoaDon_id=5)
        db.session.add_all([c1, c2, c3, c4, c5])
        db.session.commit()
