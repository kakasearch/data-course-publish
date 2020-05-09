

with open("预测数据集-3-成都市.txt",encoding='utf-8')as f:
	a = set(f.readlines())
print(len(a))
with open("预测数据集-3-成都市.txt",'w+',encoding='utf-8')as f:
	#f.write('name,money,addr\n')
	f.write(''.join(list(a)))