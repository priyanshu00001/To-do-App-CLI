import sys
from tabulate import tabulate
from datetime import datetime
from prompt_toolkit import prompt
from os import system, name
from database.model import Task, session, createDb


info = """\n\t\t\033[93m<--------------------- || DO-IT || --------------------->\033[0m
          

        \033[95mHow to use:\033[0m
    
            \033[96ma - add a new task OR tasks by seperating them by " ` "
            m - mark a task done/undone by id OR Ids seperating them by space
            e - edit a task by ID
            c - edit comment by ID
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
            t.time.strftime("%d-%m-%Y"),
            t.comment,
            "\033[92m✓\033[0m" if t.is_done else "",
        )
        for t in tasks
    ]

    print(
        tabulate(
            data,
            headers=["ID", "Task", "Added/Modified", "Comment", ""],
            tablefmt="psql",
        )
    )
    print()


def addTask(s: str):
    s = s.strip().split("`")
    task = []

    for t in s:
        t = t.strip()

        if len(t) > 35:
            formated_t = ""
            pre = 0

            for i in range(35, len(t), 35):
                dash = "" if t[i] == " " else "-"
                st = t[pre:i]
                formated_t += st + dash + "\n" if st[0] != " " else st[1:] + dash + "\n"
                pre = i

            formated_t += t[pre:] + "\n\0"
            task.append(Task(task=formated_t, time=datetime.now()))

        elif len(t) > 0:
            task.append(Task(task=t+"\n\0", time=datetime.now()))

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
        id = int(id.strip())
        t = session.get(Task, id)

        if t:
            print("\n\033[92mEdit Task : \033[0m", end="")
            s = prompt(default=t.task.replace("-\n", "").replace("\n", "")[:-1])
        else:
            return "\n\033[91mNo task was found for editing\033[0m\n"

        ts = s.strip()
        if len(ts) > 35:
            formated_t = ""
            pre = 0

            for i in range(35, len(ts), 35):
                dash = "" if ts[i] == " " else "-"
                st = ts[pre:i]
                formated_t += st + dash + "\n" if st[0] != " " else st[1:] + dash + "\n"
                pre = i

            formated_t += ts[pre:]
            t.task = formated_t + "\n\0"

        elif len(ts) > 0:
            t.task = ts + "\n\0"

        else:
            return "\n\033[91mTask can NOT be EMPTY\033[0m\n"

        t.time = datetime.now()
        t.is_done = False

    except Exception as e:
        session.rollback()
        return "\n\033[91mError : Please Enter a valid ID\033[0m\n"

    else:
        session.commit()
        return f"\n\033[92mTask ID-{id} updated\033[0m\n"


def editComment(id):
    try:
        id = int(id.strip())
        t = session.get(Task, id)

        if t:
            print("\n\033[92mEdit Comment : \033[0m", end="")
            s = prompt(default=t.comment.replace("-\n", "").replace("\n", "")[:-1])
        else:
            return "\n\033[91mNo task was found for editing\033[0m\n"

        ts = s.strip()
        if len(ts) > 15:
            formated_t = ""
            pre = 0

            for i in range(15, len(ts), 15):
                dash = "" if ts[i] == " " else "-"
                st = ts[pre:i]
                formated_t += st + dash + "\n" if st[0] != " " else st[1:] + dash + "\n"
                pre = i

            formated_t += ts[pre:]
            t.comment = formated_t + "\n\0"

        else:
            t.comment = ts + "\n\0"

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
        return "\n\033[91mNo task was found for deletion\033[0m\n"


def app():
    global info
    createDb()

    msg = "\nJUST DO IT !!\n"
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
            msg = addTask(t)

        elif command == "m":
            ids = input("\n\033[96mEnter ID to mark done/undone : \033[0m")
            msg = markTasks(ids)

        elif command == "c":
            id = input("\n\033[96mEnter ID to edit : \033[0m")
            msg = editComment(id)

        elif command == "e":
            id = input("\n\033[96mEnter ID to edit : \033[0m")
            msg = editTask(id)

        elif command == "d":
            id = input("\n\033[96mEnter ID to delete: \033[0m")
            msg = deleteTask(id)


if __name__ == "__main__":
    app()
