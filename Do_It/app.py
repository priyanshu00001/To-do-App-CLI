import sys
from tabulate import tabulate
from datetime import datetime
from prompt_toolkit import prompt
from os import system, name
from database.model import Base,engine,Task,session





info = '''\n\t\t\t\t<--------------------- || DO-IT || --------------------->


          
            How to use:
          
            
                v - view all the tasks

                c - clear the terminal

                a - add a new task or tasks by seperating them by "/"

                m - mark a task done by id Or Ids seperating them by space
                    AND undone it by adding "-" sign at the begining

                e - edit a task by ID

                d - delete a task by id OR Ids by seperating them by space
                    OR -1 to delete all tasks

                0 - exit the app
        '''





def viewTasks():
    print()

    tasks = session.query(Task).all()
    data = [(t.taskId, t.task, t.time.strftime('%I:%M %p  %d-%m-%Y'), "✓" if t.is_done else "") for t in tasks]

    print(tabulate(data, headers=["ID", "Task", "Added/modified On"," "], tablefmt="psql"))
    print()





def addTask(s:str):
    s=s.strip().split("/")
    task=[Task(task=t.strip(), time=datetime.now()) for t in s if t.strip()]

    if any(task):
        try:
            for t in task:
                if t:
                    session.add(t)

        except Exception as e:
            session.rollback()
            print("\n\033[31mSomething went wrong\033[0m\n")

        else:
            session.commit()
            print("\n\033[32mTask Added\033[0m\n")
    else:
        print("\n\033[31mNo task was found to Add\033[0m\n")





def markTasks(ids):
    taskIds=[int(id) for id in ids.split(" ") if id.lstrip('-').isdigit() or id.lstrip('+').isdigit()]
    done=[]
    undone=[]

    for id in taskIds:
        if id<0 :
            undone.append(session.get(Task,abs(id)))
        else:
            done.append(session.get(Task,id))

    if any(done):
        try:      
            for d in done:
                if d:
                    d.is_done=True

        except Exception as e:
            session.rollback()
            print("\n\033[31mSomething went wrong\033[0m\n")
            
        else:
            session.commit()
            print("\n\033[32mTask marked done\033[0m\n")

    else:
        print("\n\033[31mNo Task was found for marking done\033[0m\n")
    
    if any(undone):
        try:      
            for d in undone:
                if d:
                    d.is_done=False

        except Exception as e:
            session.rollback()
            print("\n\033[31mSomething went wrong\033[0m\n")

        else:
            session.commit()
            print("\n\033[32mTask marked undone\033[0m\n")

    else:
        print("\n\033[31mNo Task was found for marking undone\033[0m\n")





def editTask(t,s:str):
    try:
        t.task=s.strip()
        t.time=datetime.now()

    except Exception as e:
        session.rollback()
        print("\n\033[31mSomething went wrong\033[0m\n")

    else:
        session.commit()
        print("\n\033[32mTask updated\033[0m\n")





def deleteTask(ids):
    tasks=[session.get(Task,id.strip()) for id in ids.split(" ")]

    if any(tasks):
        try:
            for t in tasks:
                if t:
                    session.delete(t)

        except Exception as e:
            session.rollback()
            print("\n\033[31mSomething went wrong\033[0m\n")

        else:
            session.commit()
            print("\n\033[31mTask deleted\033[0m\n")

    else:
        print("\n\033[31mNo task was found\033[0m\n")





def app():
    global info
    Base.metadata.create_all(engine)
    system("cls" if name == "nt" else "clear")
    print(info)
    viewTasks()
    print()
    
    while True:
        command=input(">>> ")
        command=command.lower()

        if command == "0":
           sys.exit()

        elif command == "v":
            viewTasks()
        
        elif command == "c":
            system("cls" if name == "nt" else "clear")
            print(info)
            viewTasks()

        elif command == "a":
            t=input("\nEnter the Task : ")
            addTask(t)

        elif command == "m":
            ids=input("\nEnter ID to mark done/undone : ")
            markTasks(ids)

        elif command == "e":
            i=input("\nEnter ID to edit : ")
            t=session.get(Task,i)
            
            if t:
                s=prompt("\nEdit task : ",default=t.task)
                editTask(t,s)
            else:
                print("\n\033[31mNo task was found\033[0m\n")

        elif command == "d":
            id=input("\nEnter ID to delete: ")

            if id.strip()=="-1":
                session.query(Task).delete()
                session.commit()
                print("\n\033[31mAll Tasks deleted\033[0m\n")
            else:
                deleteTask(id)





if __name__=="__main__":
    app()


