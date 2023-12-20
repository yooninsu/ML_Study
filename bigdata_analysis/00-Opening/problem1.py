# %%
# num1
daum_stock = 89000
naver_stock = 751000
stock_total = daum_stock*100+naver_stock*20
print(stock_total)

# num2
daum_loss = 0.05
naver_loss = 0.1
total_loss = daum_stock*(1-daum_loss)*100 + naver_stock*(1-naver_loss)*20
print(total_loss)

# num3
# %%
myweight = int(input("몸무게를 입력하시오:(kg)"))
myheight = float(input("키를 입력하시오:(m)"))
bmi = myweight/(myheight)**2
print(f'당신의 BMI 지수는{bmi}입니다.')

# num 4
# %%

s = "Daum Kakao"
a = "".join(s[5:10]+" "+s[0:5])
print(a)

# num 5
# %%
myphotodir = "C:\myphoto\helloworld.jpg"
path = myphotodir.rfind('\\')
photoname =  myphotodir.rfind('.')

dic1 = {"폴더의 위치": myphotodir[:path],
        "파일 이름": myphotodir[path+1:photoname],
        "확장자":myphotodir[photoname+1:]}
dic1

# num 6

# %%
scorelist = [82,74,93,65,32,71,90,88,74]
top3 = sorted(scorelist)[-3:]
result = 0
for val in top3:
    result += val
print(f'Top 3의 평균값은{result/len(top3)}')

# num 7
# %%
yourage = int(input("당신의 나이를 입력하시오:"))
if yourage < 10:
    print('당신은 어린이입니다.')
elif yourage < 20:
    print('당신은 1o대입니다.')
elif yourage < 30:
    print('당신은 20대입니다.')
elif yourage < 40:
    print('당신은 30대입니다.')
elif yourage < 50:
    print('당신은 40대입니다.')
elif yourage < 60:
    print('당신은 50대입니다.')
else:
    print('당신은 노년층입니다.')


# 더 알고리즘적 사고 방식
level = yourage // 10

if level ==0:
    print('당신은 어린이입니다.')
elif level > 5:
    print("당신은 노년층입니다.")
else:
    print(f"당신은 {level*10}대입니다.") 



# num 8
# %%
myweight = int(input("몸무게를 입력하시오:(kg)"))
myheight = float(input("키를 입력하시오:(m)"))

if myheight <= 150:
    standardweight = myheight -110
else:
    standardweight = (myheight - 110) * 0.9

obesity = ((myweight-standardweight)/standardweight)*100

if obesity <= 20:
    print('정상(안심)')
elif obesity <=30:
    print('경도비만(주의)')
elif obesity <=50:
    print('중등도 비만(위험)')
else:
    print("고도비만(매우 위험)")

# num 9
# %%
result = 0
for n in range(0,101,2):
    result += n
result

# num 10
# %%
bloodtypelist = ['A','A','A','O','B','B','O','AB','AB','O']
result = {}
for sub in bloodtypelist:
    if sub not in result.keys():
        result[sub] = bloodtypelist.count(sub)
print(result)

# 다른 방식
result2 ={'A':0, "B ":0,"AB":0,"O":0}
for item in bloodtypelist:
    result2[item] += 1
result2

# num 11
# %%
x = int(input('값을 입력하시오'))
result = 1
for i in range(1,x+1):
    result *= i
result


# num 12
# %%
count =0
for i in range(1,7):
    for j in range(1,7):
        if i+j == 6:
            print([i,j])
            count +=1

print(f'경우의 수는 {count}개 입니다.')

# num 13
# %%
x = int(input("x 값 (1~100):"))
y = int(input('y 값 (1~100):'))
commonmultiple = []
for i in range(1,101):
    if i%x == 0 and i%y == 0:
        commonmultiple.append(i)
result = 0
for j in commonmultiple:
    result += j
print(commonmultiple,f'공배수의 합은 {result}')

# num 14
# %%
workhour = {"월":4,"화":3,"수":3,"목":4,
            "금":5,"토":7,"일":6}
weekdayPay = 9500
wekendPay = 13000
pay = 0
for i in workhour.keys():
    if i in ["월","화","수","목","금"]:
        pay += workhour.get(i)* weekdayPay
    else:
        pay += workhour.get(i)* wekendPay  
print(pay)

# num 15
# %%

itemlist = [{"수량": 291,"단가": 500},
            {"수량": 586,"단가": 320},
            {"수량":460, "단가": 100},
            {"수량":558, "단가":120},
            {"수량": 18, "단가":92},
            {"수량":72, "단가":30}]
volume = []
price = []
for i in itemlist:
    vl = list(i.values())
    for j in range(len(vl)):
        if j % 2 == 0:
            volume.append(vl[j])
        else:
            price.append(vl[j])
print(sum((map(lambda x,y: x*y*0.9 ,volume,price))))

total = 0
for item in itemlist:
    total += item['수량']*item['단가']*0.9
total 
# %%

# %%
