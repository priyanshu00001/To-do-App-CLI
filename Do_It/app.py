import sys
from tabulate import tabulate
from datetime import datetime
from prompt_toolkit import prompt
from os import system, name
from database.model import Task, session, createDb


info = """\n\t\t\t\t\033[33m<--------------------- || DO-IT || --------------------->\033[0m


          
            \033[35mHow to use:\033[0m
          
            
                \033[36mv - view all the tasks

                c - clean the Screen

                a - add a new task OR tasks by seperating them by " ` "

                m - mark a task done/undone by id OR Ids seperating them by space

                e - edit a task by ID

                d - delete a task by id OR Ids by seperating them by space
                    OR -1 to delete all tasks

                0 - exit the app\033[0m
                
        """


def viewTasks():
    print()
    tasks = session.query(Task).all()
    data = [
        (
            t.taskId,
            t.task,
            t.time.strftime("%I:%M %p  %d-%m-%Y"),
            "\033[32m✓\033[0m" if t.is_done else "",
        )
        for t in tasks
    ]

    print(
        tabulate(data, headers=["ID", "Task", "Added/Modified", " "], tablefmt="psql")
    )
    print()


def addTask(s: str):
    s = s.strip().split("`")
    task = [Task(task=t.strip(), time=datetime.now()) for t in s if t.strip()]

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
    taskIds = [int(id) for id in ids.split(" ") if id.strip().isdigit()]

    marking = [session.get(Task, abs(id)) for id in taskIds]

    if any(marking):
        try:
            for m in marking:
                if m:
                    m.is_done = not m.is_done

        except Exception as e:
            session.rollback()
            print("\n\033[31mSomething went wrong\033[0m\n")

        else:
            session.commit()
            print("\n\033[32mTask marked\033[0m\n")

    else:
        print("\n\033[31mNo Task was found for marking\033[0m\n")


def editTask(t, s: str):
    try:
        t.task = s.strip()
        t.time = datetime.now()

    except Exception as e:
        session.rollback()
        print("\n\033[31mSomething went wrong\033[0m\n")

    else:
        session.commit()
        print("\n\033[32mTask updated\033[0m\n")


def deleteTask(ids):
    tasks = [session.get(Task, id.strip()) for id in ids.split(" ")]

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
    createDb()
    system("cls" if name == "nt" else "clear")
    print(info)
    viewTasks()
    print()

    while True:
        command = input("\033[33m>>> \033[0m")
        command = command.lower()

        if command == "0":
            sys.exit()

        elif command == "v":
            viewTasks()

        elif command == "c":
            system("cls" if name == "nt" else "clear")
            print(info)
            viewTasks()

        elif command == "a":
            t = input("\n\033[36mEnter new Task : \033[0m")
            addTask(t)

        elif command == "m":
            ids = input("\n\033[36mEnter ID to mark done/undone : \033[0m")
            markTasks(ids)

        elif command == "e":
            i = input("\n\033[36mEnter ID to edit : \033[0m")
            t = session.get(Task, i)

            if t:
                s = prompt("\n\033[36mEdit task : \033[0m", default=t.task)
                editTask(t, s)
            else:
                print("\n\033[31mNo task was found\033[0m\n")

        elif command == "d":
            id = input("\n\033[36mEnter ID to delete: \033[0m")

            if id.strip() == "-1":
                session.query(Task).delete()
                session.commit()
                print("\n\033[31mAll Tasks deleted\033[0m\n")
            else:
                deleteTask(id)


if __name__ == "__main__":
    app()
