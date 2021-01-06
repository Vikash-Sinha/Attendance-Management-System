# Attendance-System

Attendance System Application is mainly design for coaching institute.
who use biometric attendance system in his institute. 
In this Application user can add new student, teacher, staff and set there time of entry in institute.
the application accept EXCEL sheet of attandace and calculate total present days, absent days, if the institute add absent amount
then this system also calcuate total absent amount
you can view update delete records of student teacher staff of that institute.


# package required


import tkinter.ttk as ttk
from tkinter import *
from tkcalendar import *
import datetime
import time
from tkinter.ttk import Progressbar
import xlrd
from tkinter import filedialog

#mysql connection
import mysql.connector
