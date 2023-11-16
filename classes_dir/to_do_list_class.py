import datetime
from aiogram import F
import pytz
from classes_dir.task_class import Task


class ToDoList:
    def __init__(self, chat_id: int) -> None:
        """constructor

        Args:
            chat_id (int): chat id 
        """
        self.chat_id = chat_id
        self.tasks_template = [
            Task("Neural Networks", 3),
            Task("Eating", 5),
            Task("Programming", 10),
        ]

        self.tasks = [Task(task.name, task.remaining_time) for task in self.tasks_template]


    def __str__(self):
        accomplishments = False
        going = False
        message = 'W:\n\n'
        for task in self.tasks:
            if not accomplishments and '*' in task.__str__():
                message += '\n\n'
                accomplishments = True
            if not going and not task.going:
                message += '\n'
                going = True
            
            message += task.__str__() + '\n'
        message += '\n\n'

        return message
    
    def __dict__(self):
        dictionary = {'chat_id': self.chat_id, 'template': {}, 'working': {}}

        task_template_dict = {}
        for task_t in self.tasks_template:
            task_template_dict[task_t.name] = task_t.__dict__()
        dictionary['template'] = task_template_dict

        working_dict = {}
        for task in self.tasks:
            working_dict[task.name] = task.__dict__()
        dictionary['working'] = working_dict

        return dictionary
    
    def unpacking(self, dictionary:dict) -> None:
        self.chat_id = int(dictionary['chat_id'])
        self.tasks_template = []
 
        for task_t in dictionary['template'].values():
            
            self.tasks_template.append(task_t_ := Task(str(task_t['name']), int(task_t['remaining_time'])))
            task_t_.going = bool(task_t['going'])
            task_t_.last_time_hit_start_stop = datetime.datetime.strptime(task_t['last_time_hit_start_stop'], "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone('UTC')        
            # Convert the naive datetime to an aware datetime
            task_t_.last_time_hit_start_stop = timezone.localize(task_t_.last_time_hit_start_stop)
        del dictionary['chat_id']
        del dictionary['template']



        self.tasks = []
        for task in dictionary['working'].values():
            self.tasks.append(task_ := Task(str(task['name']), int(task['remaining_time'])))
            task_.going = bool(task['going'])
            task_.last_time_hit_start_stop = datetime.datetime.strptime(task['last_time_hit_start_stop'], "%Y-%m-%d %H:%M:%S")
            timezone = pytz.timezone('UTC')        
            # Convert the naive datetime to an aware datetime
            task_.last_time_hit_start_stop = timezone.localize(task_.last_time_hit_start_stop)
        print()
        print(list(map(lambda x: x.name, self.tasks)))
        print()
        print(list(map(lambda x: x.name, self.tasks_template)))
        print()
        self.check(datetime.datetime.now()) # type: ignore

    def check(self, date_time: datetime): # type: ignore
        for task in self.tasks:
            task.check(date_time) # type: ignore
        self.sorting()


    def __iter__(self):
        return iter(self.tasks)

    def append(self, new_task: Task) -> bool: 
        for task in self.tasks:
            if task.name == new_task.name:
                return False
        else:
            self.tasks.append(new_task)
        print('append', self.tasks == self.tasks_template)
        return True
    
    def append_to_template(self, new_task: Task) -> bool: 
        for task in self.tasks_template:
            if task.name == new_task.name:
                return False
        else:
            self.tasks_template.append(new_task)
        print('append', self.tasks == self.tasks_template)
        return True

    def sorting(self):
        sorted_task_list = sorted(self.tasks, key=lambda x: (int(x.going), int(x.remaining_time), -len(x.name)), reverse=True)
        self.tasks = list(sorted_task_list)

        sorted_task_list = sorted(self.tasks_template, key=lambda x: (int(x.going), int(x.remaining_time), -len(x.name)), reverse=True)
        self.tasks_template = list(sorted_task_list)
        print('sorting', self.tasks == self.tasks_template)
        

    def start_activity(self, task_name:str, date_time:datetime) -> bool: # type: ignore
        for index, task in enumerate(self.tasks):
            if task.name == task_name:
                task.start_stop_timer(date_time=date_time) # type: ignore
                return True
        return False

    def delete_task(self, task_name:str) -> bool:
        for index, task in enumerate(self.tasks):
            if task.name == task_name:
                self.tasks.pop(index)
                print('delete_task', self.tasks == self.tasks_template)
                return True
        return False

    def delete_task_from_template(self, task_name:str) -> bool:
        for index, task in enumerate(self.tasks_template):
            if task.name == task_name:
                self.tasks_template.pop(index)
                return True
                print('delete_task_from_template', self.tasks == self.tasks_template)
        return False
    
    def print_template(self):
        message = 'T:\n\n'
        for task in self.tasks_template:
            message += task.__str__() + '\n'
        message += '\n\n'
        return message

    def len_tasks(self):
        return len(self.tasks)

    def len_tasks_template(self):
        return len(self.tasks_template)
    
