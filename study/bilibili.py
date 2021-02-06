a='hello word'
print(type(a))
#输出数据类型--布尔型
b = True
print(type(b))
#list
c=[10,20,30]
print(type(c))
#tuple--元组
d=(10,20,30,40)
print(type(d))
#set--集合
e={10,20,30}
print(type(e))
age=18
name = 'Wonder'
weight=50.5
stu_id=1
print('今年我的年龄是%d'% age)
print('今年我的名字是%s'% name)
#使用%f时加上.2表示保留两位小数
print('我的体重是%.2f'% weight)
#用%d在前面加上03可以在前面不足三位的以0补齐
print('我的学号是%03d'% stu_id)
#使用多个字符时可以在后面百分号后加括号之后按照前面的顺序输入定义的值名称
print('我的名字是%s,我的体重是%.2f,我的学号是%02d'%(name,weight,stu_id))







