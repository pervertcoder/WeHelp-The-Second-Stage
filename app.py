from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv
import os
import mysql.connector
from pydantic import BaseModel
from typing import List

load_dotenv()

def split_maker(string:str) -> list:
	target_lis = string.split('https')
	target_lis[0] = ':jpg'
	new_target_lis = []
	for i in target_lis:
		x = i.replace(':', 'https:')
		new_target_lis.append(x)
	length_new = len(new_target_lis)
	for m in range(length_new):
		if new_target_lis[m][-3:].lower() == 'jpg' or new_target_lis[m][-3:].lower() == 'png':
			new_target_lis[m] == new_target_lis[m]
		else:
			new_target_lis[m] = '無'
	return new_target_lis

def get_db_connect():
	mydb = mysql.connector.connect(
		host = os.getenv('DB_HOST'),
		user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
	return mydb

def get_mrt_data() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select MRT_data, count(*) as 次數 from attraction_info group by MRT_data order by 次數 desc'
	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	return result

def get_data_name() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select name_data from attraction_info'

	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	return result


def get_cate_data() -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select cate_data from attraction_info group by cate_data'
	mycursor.execute(sql)
	result = [x[0] for x in mycursor]
	return result

def get_attraction_data(data_id:int) -> tuple:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select * from attraction_info where id = %s'
	mycursor.execute(sql, (data_id,))
	result = [x for x in mycursor]
	return result[0]

def page_date(page:int, category:str | None = None, keyword:str | None = None) -> tuple:
	offset = page * 8
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')
	sql = 'select * from attraction_info'
	mrt = get_mrt_data()
	name = get_data_name()
	sql_filter = []
	param = []
	if category:
		sql_filter.append('cate_data = %s')
		param.append(category)
	if keyword:
		if keyword in mrt:
			sql_filter.append('MRT_data = %s')
			param.append(keyword)
		for i in name:
			if keyword in i:
				sql_filter.append('name_data like %s')
				keyword_name = f'%{keyword}%'
				param.append(keyword_name)
				break
	if sql_filter:
		sql += ' where' + ' ' + ' and '.join(sql_filter)
	sql += ' limit %s, 8'
	param.append(offset)
	

	mycursor.execute(sql, tuple(param))
	result = mycursor.fetchall()
	return result
# print(page_date(1))


class DataResponse(BaseModel):
	data: List[str]

class ErrorResponse(BaseModel):
    error: bool
    message: str

class AttractionResponse(BaseModel):
	data: dict

class AttractionDataResponse(BaseModel):
	data: list


app=FastAPI()
@app.get('/api/mrts', response_model=DataResponse, responses={200 : {'description' : '正常運作'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def get_mrts():
	try:
		mrt_data = get_mrt_data()
		return {
			'data' : mrt_data
		}
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})

@app.get('/api/categories', response_model=DataResponse, responses={200 : {'description' : '正常運作'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def get_cate():
	try:
		cate_data = get_cate_data()
		return {
			'data' : cate_data
		}
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
# 範例{400: {'model' : ErrorResponse, 'description' : '景點編號不正確'}}
@app.get('/api/attraction/{attraction_id}', response_model=AttractionResponse, responses={200 : {'description' : '景點資料'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}, 400 : {'model' : ErrorResponse, 'description' : '景點編號不正確'}})
def get_attraction(attraction_id:int):
	if attraction_id > 58:
		return JSONResponse(status_code=400, content={'error' : True, 'message' : '查無資料'})
	try:
		att_data = get_attraction_data(attraction_id)
		file_data = split_maker(att_data[15])
		file_data.pop(0)
		file_data = [i for i in file_data if i != '無']
		return {
			'data' : {
				'id' : att_data[0],
				'name' : att_data[3],
				'category' : att_data[12],
				'description' : att_data[18],
				'adress' : att_data[-1],
				'transport' : att_data[2],
				'mrt' : att_data[9],
				'lat' : att_data[-5],
				'lng' : att_data[5],
				'image' : file_data
			}
		}
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
	

@app.get('/api/attractions', response_model=AttractionDataResponse, responses={500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def get_specific_data(page:int, category:str | None = None, keyword:str | None = None, ):
	try:
		result = page_date(page, category, keyword)
		data_list = []
		for rows in result:
			new_file = split_maker(rows[15])
			new_file.pop(0)
			new_file = [i for i in new_file if i != '無']
			data_list.append({
				'id' : rows[0],
				'name' : rows[3],
				'category' : rows[12],
				'description' : rows[18],
				'adress' : rows[-1],
				'transport' : rows[2],
				'mrt' : rows[9],
				'lat' : rows[-5],
				'lng' : rows[5],
				'image' : new_file
			}
			)
		
		return {
			'data' : data_list
		}
	
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
		
	
	

# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")