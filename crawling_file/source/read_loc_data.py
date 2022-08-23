import pandas as pd

def read_location_csv():
	df = pd.read_csv("20220804_도로명범위.csv", encoding='cp949')
	return df


def to_dict(df_location):
	df = read_location_csv()
	top_region = list(set(df['시도'].values))

	map_dict ={}

	for i in top_region:
		region_df = df[df['시도']==i]
		mid_region_list = list(set(list(region_df['시군구'].values)))
		map_dict[i] = mid_region_list

	return map_dict
