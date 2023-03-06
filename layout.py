# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\layout.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(621, 606)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_pesquisa = QtWidgets.QFrame(self.centralwidget)
        self.frame_pesquisa.setMinimumSize(QtCore.QSize(0, 90))
        self.frame_pesquisa.setMaximumSize(QtCore.QSize(600, 90))
        self.frame_pesquisa.setStyleSheet("")
        self.frame_pesquisa.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_pesquisa.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_pesquisa.setObjectName("frame_pesquisa")
        self.bt_pesquisar = QtWidgets.QPushButton(self.frame_pesquisa)
        self.bt_pesquisar.setGeometry(QtCore.QRect(460, 10, 111, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_pesquisar.setFont(font)
        self.bt_pesquisar.setObjectName("bt_pesquisar")
        self.ed_nome = QtWidgets.QLineEdit(self.frame_pesquisa)
        self.ed_nome.setGeometry(QtCore.QRect(10, 10, 441, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ed_nome.setFont(font)
        self.ed_nome.setObjectName("ed_nome")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame_pesquisa)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 591, 25))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rb_union = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rb_union.setFont(font)
        self.rb_union.setObjectName("rb_union")
        self.horizontalLayout.addWidget(self.rb_union)
        self.rb_firemangas = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rb_firemangas.setFont(font)
        self.rb_firemangas.setObjectName("rb_firemangas")
        self.horizontalLayout.addWidget(self.rb_firemangas)
        self.rb_muito = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rb_muito.setFont(font)
        self.rb_muito.setChecked(True)
        self.rb_muito.setObjectName("rb_muito")
        self.horizontalLayout.addWidget(self.rb_muito)
        self.rb_scan = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rb_scan.setFont(font)
        self.rb_scan.setObjectName("rb_scan")
        self.horizontalLayout.addWidget(self.rb_scan)
        self.rb_yabu = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.rb_yabu.setFont(font)
        self.rb_yabu.setObjectName("rb_yabu")
        self.horizontalLayout.addWidget(self.rb_yabu)
        self.verticalLayout.addWidget(self.frame_pesquisa)
        self.frame_lista_animes = QtWidgets.QFrame(self.centralwidget)
        self.frame_lista_animes.setMinimumSize(QtCore.QSize(580, 200))
        self.frame_lista_animes.setMaximumSize(QtCore.QSize(650, 600))
        self.frame_lista_animes.setStyleSheet("")
        self.frame_lista_animes.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_lista_animes.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_lista_animes.setObjectName("frame_lista_animes")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.frame_lista_animes)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.lista_animes = QtWidgets.QListWidget(self.frame_lista_animes)
        self.lista_animes.setObjectName("lista_animes")
        self.gridLayout_5.addWidget(self.lista_animes, 0, 0, 1, 1)
        self.lbl_pic = QtWidgets.QLabel(self.frame_lista_animes)
        self.lbl_pic.setMinimumSize(QtCore.QSize(0, 0))
        self.lbl_pic.setMaximumSize(QtCore.QSize(180, 180))
        self.lbl_pic.setText("")
        self.lbl_pic.setObjectName("lbl_pic")
        self.gridLayout_5.addWidget(self.lbl_pic, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame_lista_animes)
        self.frame_lista_cap = QtWidgets.QFrame(self.centralwidget)
        self.frame_lista_cap.setMaximumSize(QtCore.QSize(600, 300))
        self.frame_lista_cap.setStyleSheet("")
        self.frame_lista_cap.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_lista_cap.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_lista_cap.setObjectName("frame_lista_cap")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_lista_cap)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame_ = QtWidgets.QFrame(self.frame_lista_cap)
        self.frame_.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_.setMaximumSize(QtCore.QSize(600, 100))
        self.frame_.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_.setObjectName("frame_")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.ed_inicio = QtWidgets.QLineEdit(self.frame_)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ed_inicio.setFont(font)
        self.ed_inicio.setObjectName("ed_inicio")
        self.gridLayout_3.addWidget(self.ed_inicio, 0, 1, 1, 1)
        self.ed_fim = QtWidgets.QLineEdit(self.frame_)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.ed_fim.setFont(font)
        self.ed_fim.setObjectName("ed_fim")
        self.gridLayout_3.addWidget(self.ed_fim, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame_)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 4, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame_, 1, 0, 1, 1)
        self.tx_capitulos = QtWidgets.QPlainTextEdit(self.frame_lista_cap)
        self.tx_capitulos.setObjectName("tx_capitulos")
        self.gridLayout_2.addWidget(self.tx_capitulos, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_lista_cap)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.ed_nome, self.rb_muito)
        MainWindow.setTabOrder(self.rb_muito, self.rb_scan)
        MainWindow.setTabOrder(self.rb_scan, self.rb_yabu)
        MainWindow.setTabOrder(self.rb_yabu, self.bt_pesquisar)
        MainWindow.setTabOrder(self.bt_pesquisar, self.lista_animes)
        MainWindow.setTabOrder(self.lista_animes, self.ed_inicio)
        MainWindow.setTabOrder(self.ed_inicio, self.ed_fim)
        MainWindow.setTabOrder(self.ed_fim, self.pushButton_2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Manga Downloader"))
        self.bt_pesquisar.setText(_translate("MainWindow", "Buscar\n"
"mangá"))
        self.rb_union.setText(_translate("MainWindow", "Union Mangás"))
        self.rb_firemangas.setText(_translate("MainWindow", "Firemangas"))
        self.rb_muito.setText(_translate("MainWindow", "Muito Mangá"))
        self.rb_scan.setText(_translate("MainWindow", "Project Scan"))
        self.rb_yabu.setText(_translate("MainWindow", "MangaYabu"))
        self.label.setText(_translate("MainWindow", "Cap. Inicio"))
        self.label_2.setText(_translate("MainWindow", "Cap Final"))
        self.pushButton_2.setText(_translate("MainWindow", "Baixar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
