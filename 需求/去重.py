with open("d:/desktop/全部数据集-2.txt",encoding='utf-8')as f:
	a = set(f.readlines())

with open("d:/desktop/全部数据集-3.txt",'w+',encoding='utf-8')as f:
	#f.write('name,money,addr\n')
	f.write(''.join(list(a)))