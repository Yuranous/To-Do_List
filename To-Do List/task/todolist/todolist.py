from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
session = sessionmaker(bind=engine)()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
rows = session.query(Table).all()

while True:
    print("1) Today's Tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit")
    user_option = input()

    if user_option == '1':
        today = datetime.today().date()
        rows1 = session.query(Table).filter(Table.deadline == today).all()
        print(f'Today {today.day} {today.strftime("%b")}:')
        if len(rows1) > 0:
            for count, item in enumerate(rows1):
                print(f'{count + 1}. {item.task}. {item.deadline.day} {item.deadline.strftime("%b")}')
            print()
        else:
            print('Nothing to do!\n')

    elif user_option == '2':
        today = datetime.today().date()
        week = today + timedelta(days=7)
        rows2 = session.query(Table).filter(Table.deadline.between(today, week)).all()
        for d in range(7):
            print(f'{today.strftime("%A")} {today.day} {today.strftime("%b")}:')
            rows2 = session.query(Table).filter(Table.deadline == today).all()
            if len(rows2) > 0:
                for count, item in enumerate(rows2):
                    print(f'{count + 1}. {item.task}')
                print()
            else:
                print('Nothing to do!\n')
            today += timedelta(days=1)

    elif user_option == '3':
        print('All tasks:')
        if len(rows) > 0:
            for count, item in enumerate(rows):
                print(f'{count + 1}. {item.task}. {item.deadline.day} {item.deadline.strftime("%b")}')
            print()
        else:
            print('Nothing to do!\n')

    elif user_option == '4':
        task = input('Enter task\n')
        deadline = input('Enter deadline\n')
        deadline = datetime.strptime(deadline, '%Y-%m-%d')
        new_row = Table(task=task, deadline=deadline)
        session.add(new_row)
        session.commit()
        print('The task has been added!\n')

    elif user_option == '0':
        print('\nBye!')
        exit()