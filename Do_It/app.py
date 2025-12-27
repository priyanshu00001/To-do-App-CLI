import sys
from tabulate import tabulate
from datetime import datetime
from prompt_toolkit import prompt
from os import system, name
from database.model import Task, session, createDb


info = """\n\t\033[93m<--------------------- || DO-IT || --------------------->\033[0m
          

    \033[95mHow to use:\033[0m
    
        \033[96ma - add a new task OR tasks by seperating them by " ` "
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
            "\033[92m✓\033[0m" if t.is_done else "",
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
            return "\n\033[91mSomething went wrong\033[0m\n"

        else:
            session.commit()
            return f"\n\033[92m{len(task)} - Tasks Added\033[0m\n"
    else:
        return "\n\033[91mNo task was found to Add\033[0m\n"


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
            return "\n\033[91mSomething went wrong\033[0m\n"

        else:
            session.commit()
            return f"\n\033[92mTask marked\033[0m\n"

    else:
        return "\n\033[91mNo Task was found for marking\033[0m\n"


def editTask(id):
    try:
        id=int(id.strip())
        t = session.get(Task, id)

        if t:
            s = prompt("\nEdit task : ", default=t.task)
        else:
            return "\n\033[91mNo task was found\033[0m\n"
        t.task = s.strip()
        t.time = datetime.now()
        t.is_done=False

    except Exception as e:
        session.rollback()
        return "\n\033[91mError : Please Enter a valid ID\033[0m\n"

    else:
        session.commit()
        return f"\n\033[92mTask ID-{id} updated\033[0m\n"


def deleteTask(ids):
    if ids.strip() == "-1":
        session.query(Task).delete()
        session.commit()
        return "\n\033[91mAll Tasks are deleted\033[0m\n"
    
    tasks = [session.get(Task, id.strip()) for id in ids.split(" ")]

    if any(tasks):
        try:
            for t in tasks:
                if t:
                    session.delete(t)

        except Exception as e:
            session.rollback()
            return "\n\033[91mSomething went wrong\033[0m\n"

        else:
            session.commit()
            return "\n\033[91mTask deleted\033[0m\n"

    else:
        return "\n\033[91mNo task was found\033[0m\n"


def app():
    global info
    createDb()
    msg="\nJUST DO IT !!\n"
    print()

    while True:
        system("cls" if name == "nt" else "clear")
        print(info)
        viewTasks()
        print(msg)
        
        command = input("\033[93m>>> \033[0m")
        command = command.lower()

        if command == "0":
            sys.exit()

        elif command == "a":
            t = input("\n\033[96mEnter new Task : \033[0m")
            msg=addTask(t)

        elif command == "m":
            ids = input("\n\033[96mEnter ID to mark done/undone : \033[0m")
            msg=markTasks(ids)

        elif command == "e":
            id = input("\n\033[96mEnter ID to edit : \033[0m")
            msg=editTask(id)

        elif command == "d":
            id = input("\n\033[96mEnter ID to delete: \033[0m")
            msg=deleteTask(id)


if __name__ == "__main__":
    app()
