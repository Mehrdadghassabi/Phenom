import sys

height=int(sys.argv[1])
weight=int(sys.argv[2])
language=sys.argv[3]

bmi=weight*10000/(height*height)
if(language=='en'):
    if(bmi<18.5):
        print(f'Your BMI is {bmi}. You are in Underweight.')
    elif(bmi>=18.5 and bmi<=24.9):
        print(f'Your BMI is {bmi}. You are in Normal weight.')
    elif(bmi>24.9 and bmi<=29.9):
        print(f'Your BMI is {bmi}. You are in Overweight.')
    else:
        print(f'Your BMI is {bmi}. You are in Obesity.')
else:
    if (bmi < 18.5):
        print(f'BMI شما برابر است با {bmi}. شما کم وزن هستید.')
    elif (bmi >= 18.5 and bmi <= 24.9):
        print(f'BMI شما برابر است با {bmi}. شما در وزن طبیعی هستید.')
    elif (bmi > 24.9 and bmi <= 29.9):
        print(f'BMI شما برابر است با {bmi}. شما در اضافه وزن هستید.')
    else:
        print(f'BMI شما برابر است با {bmi}. شما در چاقی هستید.')