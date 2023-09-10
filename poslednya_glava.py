data=[i 
      for i in range (1,9)]
evens=[num 
       for num in data 
       if not num %2]


data1=list('So i want to cumshotick v popik'.split())
title=[word for word in data1]


data3={1:'one',2:'two'}
changer={v:k for k,v in data3.items()}
print (changer)