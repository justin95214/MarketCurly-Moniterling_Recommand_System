import pandas as pd
import numpy as np
import re
import read_loc_data as csv_data



def location(s, df, map_dict):

	if s !="":
		#df = pd.read_csv("20220804_도로명범위.csv", encoding='cp949')
		top_region = list(set(df['시도'].values)) 
		
		big_region = None
		small_region = None

		#map_dict ={}

		##특수문자 제거
		
		s = re.sub('[-=+,#/\?:^.@*\"※~ㆍ!』‘|\(\)\[\]`\'…》\”\“\’·]', ' ' ,s)
		s = ' '.join(s.split())
		if s == "":
			return "", ""

		#print(f'전처리된 문자 : {s}')
		##줄임말 변경
		short_word_dict ={'충북': '충청북도', '충남':'충청남도', '전북':'전라북도','전남':'전라남도','경남':'경상남도', '경북':'경상북도'}
		
		for short in short_word_dict:
			if short == s:
				s = short_word_dict[short]
		#print(f'전처리된 문자 : {s}')
		mid_region_list = []

		## 지역 비교
		for i in top_region:
			
			region_df = df[df['시도']==i]
			mid_region_list = list(set(list(region_df['시군구'].values)))
			
			#map_dict[i] = mid_region_list

			#print(map_dict)
					
			#제목에 시도가 있을 때
			for big_r in top_region:
				if s in big_r:
					big_region = big_r
					#print(big_region)
					break;

			#제목에 시군구가 있을 때
			
			if mid_region_list !=[np.NaN]:
				for sm_r in mid_region_list:
					#print(sm_r,s)
					if s in sm_r:
						big_region = i
						break;
				
			if mid_region_list !=[np.NaN]:
				for a in mid_region_list:
					search_a = a[:-1]
					if search_a == '동' or search_a == '서' or search_a == '남' or search_a == '북' or search_a == '중':
						search_a = a											
					
					#print(search_a, s)
					if search_a in s:
						#print('answer :' ,a)

						for g in top_region:
							if a in map_dict[g]:
								big_region = g
								break;

			for tt in top_region:
				if tt[:2] in s:
					big_region =tt

		

	else:
		return ""


			
	return  big_region

"""
df_location = csv_data.read_location_csv()
dict_location = csv_data.to_dict(df_location)
s = "청송배"
big = location(s, df_location, dict_location)

print(big)
"""
