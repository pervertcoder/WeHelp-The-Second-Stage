import json
from dotenv import load_dotenv
import os
import mysql.connector


file_path = r'data\taipei-attractions.json'
with open(file_path, 'r', encoding='utf-8') as file:
	data = json.load(file)

data_usage = data['result']['results']
data_usage[20]['CAT'] = '其他'


for i in data_usage:
	mrts = i['MRT']
	if mrts == None:
		mrts = '無'



def split_maker(string):
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
	

load_dotenv()
def get_db_connect():
	mydb = mysql.connector.connect(
		host = os.getenv('DB_HOST'),
		user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD')
    )
	return mydb

def insert_data(data:list):
	test = []
	for i in range(21):
		test.append(i)
	placeholder = ','.join(['%s'] * len(test))
	conn = get_db_connect()
	mycursor = conn.cursor()
	sql = f'''insert into attraction_info(
		rate_data,
		direction_data,
		name_data,
		date_data,
		longitude_data,
		REF_WP_data,
		avBegin_data,
		langinfo_data,
		MRT_data,
		SERIAL_NO_data,
		RowNumber_data,
		cate_data,
		MEMO_TIME_data,
		POI_data,
		file_data,
		idpt_data,
		latitude_data,
		description_data,
		_id_data,
		avEnd_data,
		address_data
			)values
			({placeholder})
	'''
	data_lis = [x.keys() for x in data][0]
	new_data_lis = list(data_lis)
	use_data = []
	for i in data:
		i['SERIAL_NO'] = str(i['SERIAL_NO'])
	for i in data:
		sub_use_data = [i[new_data_lis[j]] for j in range(len(new_data_lis))]
		use_data.append(tuple(sub_use_data))

	mycursor.execute('use tourist_attraction')
	mycursor.executemany(sql, use_data)
	conn.commit()
	conn.close()
	print('data inserted successfully')

# insert_data(data_usage)
