from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import mysql.connector
from pydantic import BaseModel
from typing import List
import jwt
from datetime import datetime, timedelta, timezone
import time

load_dotenv()
load_dotenv('.env_jwt')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

def create_jwt(data:dict):
	payload = data.copy()
	expire_time = datetime.now(timezone.utc) + timedelta(hours=1)
	payload["exp"] = int((expire_time).timestamp())
	token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
	return token

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

def insert_register_data(n:str, m:str, p:str):
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use web_attraction_mem')
	sql = 'insert into web_attraction_memberinfo (name, email, password) values (%s, %s, %s)'
	mycursor.execute(sql, (n, m, p))

	conn.commit()
	conn.close()
	print('data inserted successfully')

def check_member(m:str) -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use web_attraction_mem')
	sql = 'select * from web_attraction_memberinfo where email = %s'
	mycursor.execute(sql, (m,))
	result = [x for x in mycursor]
	conn.close()
	return result

print(check_member('test@test.com'))

def check_rigisted_mem(m:str) -> list:
	pass

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
	# mrt = get_mrt_data()
	# name = get_data_name()
	sql_filter = []
	param = []
	if category:
		sql_filter.append('cate_data = %s')
		param.append(category)
	if keyword:
		mrt = get_mrt_data()
		name = get_data_name()
		if keyword in mrt:
			sql_filter.append('MRT_data = %s')
			param.append(keyword)
			# and name_data LIKE %s
		else:
			sql_filter.append('name_data LIKE %s')
			param.append(f'%{keyword}%')
	if sql_filter:
		sql += ' where' + ' ' + ' and '.join(sql_filter)
	sql += ' limit %s, 8'
	param.append(offset)
	
	mycursor.execute(sql, tuple(param))
	result = mycursor.fetchall()
	return result

def diff_page(page:int, category:str | None = None, keyword:str | None = None) -> list:
	conn = get_db_connect()
	mycursor = conn.cursor()
	mycursor.execute('use tourist_attraction')

	sql = 'select count(*) as total_count, ceil(count(*) / 8) as total_page from attraction_info'
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
	
	mycursor.execute(sql, tuple(param))
	result = [x for x in mycursor]
	final_result = []
	final_result.append(result[0][0])
	final_result.append(int(result[0][1]))
	return final_result


class DataResponse(BaseModel):
	data: List[str]

class ErrorResponse(BaseModel):
    error: bool
    message: str

class AttractionResponse(BaseModel):
	data: dict

class AttractionDataResponse(BaseModel):
	nextPage: int | None
	data: list

class stateResponse(BaseModel):
	ok : bool

class registDataRequest(BaseModel):
	username : str
	useremail : str
	userpass : str

class loginDataRequest(BaseModel):
	usermail :str
	userpassword : str

class loginDataResponse(BaseModel):
	access_token : str
	token_type : str = 'bearer'

app=FastAPI()
@app.post('/api/user', response_model=stateResponse, responses={200 : {'description' : '註冊成功'}, 400:{'model' : ErrorResponse, 'description' : '註冊失敗，重複的 Email 或其他原因'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
async def register (request:registDataRequest):
	try:
		username = request.username
		useremail = request.useremail
		userpass = request.userpass
		state = True
		# 檢查有無重複
		check_email = check_member(useremail)
		print(check_email)
		# 存入資料庫
		if check_email != []:
			state = False
			# raise HTTPException(status_code=400, detail='Email已存在')
		if state:
			insert_register_data(username, useremail, userpass)
			return {
				'ok' : True
			}
		else:
			return JSONResponse(status_code=400, content={
				'error' : True,
				'message' : 'email已存在'
			})
		
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})

@app.put('/api/user/auth')
async def member_data (request:loginDataRequest):
	try:
		usermail = request.usermail
		userpassword = request.userpassword
		check = check_member(usermail)
		print(check[0][0], check[0][2])
		if check != [] and userpassword == check[0][3]:
			token = create_jwt({'id' : check[0][0], 'email' : check[0][2]})
			return {
				'access_token' : token
			}
		else:
			return JSONResponse(status_code=400, content={
				'error' : True,
				'message' : 'email和密碼不正確'
			})
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})

@app.get('/api/mrts', response_model=DataResponse, responses={200 : {'description' : '正常運作'}, 500: {'model' : ErrorResponse, 'description' : '伺服器內部錯誤'}})
def get_mrts() -> DataResponse | ErrorResponse:
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
def get_cate() -> DataResponse | ErrorResponse:
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
def get_attraction(attraction_id:int) -> AttractionResponse | ErrorResponse:
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
				'address' : att_data[-1],
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
def get_specific_data(page:int, category:str | None = None, keyword:str | None = None) -> AttractionDataResponse | ErrorResponse:
	try:
		result = page_date(page, category, keyword)
		total_page = diff_page(page, category, keyword)[1]
		used_page = None
		if page == total_page - 1:
			final_page = used_page
		else:
			final_page = page + 1
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
				'address' : rows[-1],
				'transport' : rows[2],
				'mrt' : rows[9],
				'lat' : rows[-5],
				'lng' : rows[5],
				'image' : new_file
			}
			)
		
		return {
			'nextPage' : final_page,
			'data' : data_list
		}
	
	except Exception as e:
		return JSONResponse(status_code=500, content={
			'error' : True,
			'message' : str(e)
		})
		
	
	
app.mount('/static', StaticFiles(directory='static'), name='static')
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