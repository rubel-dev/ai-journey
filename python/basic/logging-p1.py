import logging

logging.basicConfig(filename='AD_test.log',
                    level= logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s"
                    
                    )

num1 = int(input("Enter a number:"))
num2 = int(input("Please Enter a another number:"))

try:
    div = num1/num2
    print(div)
    logging.info("user got: %s", div )

except Exception as e:
    print("you can not divided by zero")
    logging.error("Error has Happened")
    logging.exception("Exception is "+str(e))