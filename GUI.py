def sum(monthly, years, months_retired):
    sum = 0
    sum_inf = 0
    for i in range(years*12):
        monthly_now = monthly #if i>=24 else monthly*0.3  # if i>12*5 else monthly-monthly_inp
        if i % 12 == 0:
            sum = sum*1.07 + monthly_now #1.0692
        else:
            sum += monthly_now
    sum_inf = 9260000*(0.97**(years))
    sum_tax = sum*0.85
    return f'{sum:.2f}',f'{sum_inf:.2f}' ,(sum_inf)//(months_retired*12), f'{sum_tax:.2f}'
def sum2(monthly,years):
    sum = 0
    for i in range(years):
        sum+=monthly*12
        sum*=1.07
    return sum
def sum3(monthly,years):
    sum = 0
    for i in range(years*12):
        sum+=monthly
        sum*=(1.07/12)
    return sum
print(sum(int(input('měsíční vklad: ')), int(input('počet let: ')),int(input('počet let v důchodu: '))))
print(sum2(int(input('měsíční vklad: ')), int(input('počet let: ') )), '    ',sum3(int(input('měsíční vklad: ')), int(input('počet let: ') )))