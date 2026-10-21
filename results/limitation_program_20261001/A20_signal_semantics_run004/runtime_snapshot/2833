import random 

List=[10,20,30,40,50,60]

def addElement(a):
    List.append(a)
    return list
def insertion(b,x):
    List.insert(b,x)
def addlist(L):
    List.append(L)
def delete_elementfromposition(f):
    List.pop(f)
def delete_elementwithvalue(d):
    List.remove(d)
def sorting_list(List):
    List.sort()
def sorting_reverse(List):
    List.sort(reverse=True)
def display(List):
    print(List)
operations=["append_element","insertion","append_list","pop","remove","sort","sort_reverse"]
while True:
    
    op=random.choice(operations)
    if op=="append_element":
        a=random.randint(1,100)
        print("The element adding is",a)
        List.append(a)
        display(List)
    elif op=="insertion":
        b=random.randint(0,5)
        x=random.randint(1,1111)
        print("Index is", b)
        print("Value is", x)
        List.insert(b,x)
        display(List)
    '''
    elif op=="append_list":
        L=[]
        for i in range(random.randint(2,10)):
            new_element=random.randint(1,500)
            L.append(new_element)
        List.append(L)
        display(List)
    '''
    elif op=="pop":
        f=random.randint(0,4)
        List.pop(f)
        display(List)
    elif op=="remove":
        d=random.randint(0,100)
        if d in List:
            List.remove(d)
        else:
            print("Not present in List")
        display(List)
    elif op=="sort":
        List.sort()
        display(List)
    elif op=="sort_reverse":
        List.sort(reverse=True)
        display(List)
    else:
        print("Invalid Operation")
        break
            
