import datetime
import pytz
from typing import List, Dict, Optional

class RoutineTask:
    def __init__(self, name: str, duration: int, optional: bool = False, notes: str = ""):
        self.name = name
        self.duration = duration
        self.optional = optional
        self.notes = notes
        self.completed = False
        self.completed_at = None
        self.skipped = False

    
    def mark_complete(self):
        self.completed = True
        self.completed_at = datetime.datetime.now(pytz.UTC)
    
    def reset(self):
        self.completed = False
        self.completed_at = None
        self.skipped = False
    
    def to_dict(self):
        return {
            'name': self.name,
            'duration': self.duration,
            'optional': self.optional,
            'notes': self.notes,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'skipped': self.skipped
        }
    
    @classmethod
    def from_dict(cls, data):
        task = cls(data['name'], data['duration'], data.get('optional', False), data.get('notes', ''))
        task.completed = data.get('completed', False)
        task.skipped = data.get('skipped', False)
        if data.get('completed_at'):
            task.completed_at = datetime.datetime.fromisoformat(data['completed_at'])
        return task

class MorningRoutine:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.tasks: List[RoutineTask] = []
        self.current_streak = 0
        self.best_streak = 0
        self.total_completions = 0
        self.history: Dict[str, Dict] = {}
        self.routine_started = False
        self.start_time = None
        self.is_setup_complete = False
        self.paused = False
        self.pause_time = None
        self.total_pause_duration = 0
        # Customizable time window (hours and minutes)
        self.window_start = 5
        self.window_start_minute = 0  # NEW
        self.window_end = 11
        self.window_end_minute = 0    # NEW
        self.timezone = 'Europe/Helsinki'
    
    def add_task(self, name: str, duration: int, optional: bool = False, notes: str = "") -> tuple[bool, str]:
        """Add task with validation. Returns (success, error_message)"""
        if len(self.tasks) >= 15:
            return False, "Max 15 tasks"
        if not name or not name.strip():
            return False, "Task name required"
        if duration <= 0:
            return False, "Duration must be positive"
        if duration > 999:
            return False, "Duration too long (max 999)"
        
        self.tasks.append(RoutineTask(name.strip(), duration, optional, notes))
        return True, ""
    
    def remove_task(self, index: int) -> bool:
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            return True
        return False
    
    def edit_task(self, index: int, name: str = None, duration: int = None, 
                  optional: bool = None, notes: str = None) -> tuple[bool, str]:
        """Edit task properties. Returns (success, error_message)"""
        if not (0 <= index < len(self.tasks)):
            return False, "Invalid task number"
        
        task = self.tasks[index]
        
        if name is not None:
            if not name.strip():
                return False, "Name cannot be empty"
            task.name = name.strip()
        
        if duration is not None:
            if duration <= 0:
                return False, "Duration must be positive"
            if duration > 999:
                return False, "Duration too long"
            task.duration = duration
        
        if optional is not None:
            task.optional = optional
        
        if notes is not None:
            task.notes = notes
        
        return True, ""
    
    def move_task(self, from_index: int, to_index: int) -> bool:
        """Reorder tasks"""
        if not (0 <= from_index < len(self.tasks) and 0 <= to_index < len(self.tasks)):
            return False
        task = self.tasks.pop(from_index)
        self.tasks.insert(to_index, task)
        return True
    
    def start_routine(self):
        if not self.can_start_routine():
            return False
        self.routine_started = True
        self.start_time = datetime.datetime.now(pytz.UTC)
        self.paused = False
        self.total_pause_duration = 0
        for task in self.tasks:
            task.reset()
        return True
    
    def can_start_routine(self) -> bool:
        """Check if within time window and not already done today"""
        user_tz = pytz.timezone(self.timezone)
        now = datetime.datetime.now(user_tz)
        today = now.date().isoformat()
        
        # Check if already completed today
        if today in self.history:
            return False
        
        # Check time window with minutes
        current_minutes = now.hour * 60 + now.minute
        start_minutes = self.window_start * 60 + self.window_start_minute
        end_minutes = self.window_end * 60 + self.window_end_minute
        
        return start_minutes <= current_minutes < end_minutes
    
    def pause_routine(self):
        """Pause routine"""
        if self.routine_started and not self.paused:
            self.paused = True
            self.pause_time = datetime.datetime.now(pytz.UTC)
            return True
        return False
    
    def resume_routine(self):
        """Resume routine"""
        if self.routine_started and self.paused:
            pause_duration = (datetime.datetime.now(pytz.UTC) - self.pause_time).total_seconds()
            self.total_pause_duration += pause_duration
            self.paused = False
            self.pause_time = None
            return True
        return False
    
    def complete_task(self, index: int) -> bool:
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_complete()
            return True
        return False
    
    def get_completion_percentage(self) -> float:
        if not self.tasks:
            return 0
        required_tasks = [t for t in self.tasks if not t.optional]
        if not required_tasks:
            return 100
        completed = sum(1 for t in required_tasks if t.completed)
        return (completed / len(required_tasks)) * 100
    
    def finish_routine(self):
        if not self.routine_started:
            return False
        
        completion = self.get_completion_percentage()
        
        # Calculate actual duration (excluding pauses)
        total_seconds = (datetime.datetime.now(pytz.UTC) - self.start_time).total_seconds()
        active_duration = (total_seconds - self.total_pause_duration) / 60
        
        today = datetime.date.today().isoformat()
        self.history[today] = {
            'completion': completion,
            'duration': int(active_duration),
            'tasks': [t.to_dict() for t in self.tasks]
        }
        
        # Streak: 100% = maintain, else reset
        if completion >= 100:
            self.current_streak += 1
            self.total_completions += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
        else:
            self.current_streak = 0
        
        for task in self.tasks:
            task.reset()
        
        self.routine_started = False
        self.start_time = None  # Also reset start_time
        self.paused = False
        self.pause_time = None
        self.total_pause_duration = 0
        
        return True
    
    def check_missed_routine(self):
        user_tz = pytz.timezone(self.timezone)
        now = datetime.datetime.now(user_tz)
        today = now.date().isoformat()
        
        # Check if past window end
        current_minutes = now.hour * 60 + now.minute
        end_minutes = self.window_end * 60 + self.window_end_minute
        
        if current_minutes >= end_minutes and today not in self.history:
            self.history[today] = {
                'completion': 0,
                'duration': 0,
                'tasks': [],
                'missed': True
            }
            self.current_streak = 0
            # Reset tasks for next day
            for task in self.tasks:
                task.reset()
            self.routine_started = False
            self.start_time = None
    
    def get_weekly_stats(self):
        last_7_days = []
        for i in range(6, -1, -1):
            date = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
            last_7_days.append(self.history.get(date, {'completion': 0}))
        
        completed_days = sum(1 for d in last_7_days if d.get('completion', 0) >= 100)
        avg_completion = sum(d.get('completion', 0) for d in last_7_days) / 7
        
        return {
            'completed_days': completed_days,
            'avg_completion': avg_completion,
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'total_completions': self.total_completions
        }
    
    def get_status_display(self) -> str:
        lines = []
        
        if self.routine_started:
            if self.paused:
                elapsed = (self.pause_time - self.start_time).total_seconds() / 60
                header = f"PAUSED · {int(elapsed)}m"
            else:
                elapsed = (datetime.datetime.now(pytz.UTC) - self.start_time).total_seconds() / 60
                elapsed -= (self.total_pause_duration / 60)
                header = f"ROUTINE · {int(elapsed)}m"
        else:
            header = "ROUTINE"
        
        lines.append(f"┏━━━━━━━━━━━━━━━━━━━━┓\n")
        lines.append(f"                 {header:^18}  \n")
        lines.append(f"┗━━━━━━━━━━━━━━━━━━━━┛\n\n")
        
        if self.tasks:
            max_name_length = max(len(t.name) for t in self.tasks)
        else:
            max_name_length = 0
        
        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task.completed else "○"
            opt = " `opt`" if task.optional else ""
            padding = max_name_length - len(task.name)
            spaces = "\u2009" * padding
            
            lines.append(f"{status} `{task.name}{spaces}  {task.duration}m`{opt}\n")
        
        if self.routine_started:
            completion = self.get_completion_percentage()
            lines.append(f"\n`{completion:.0f}%` complete")
        
        if self.current_streak > 0:
            lines.append(f" · `{self.current_streak}d` 🔥")
        
        return "".join(lines)
    
    def to_dict(self):
        return {
            'chat_id': self.chat_id,
            'tasks': [t.to_dict() for t in self.tasks],
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'total_completions': self.total_completions,
            'history': self.history,
            'routine_started': self.routine_started,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'is_setup_complete': self.is_setup_complete,
            'paused': self.paused,
            'pause_time': self.pause_time.isoformat() if self.pause_time else None,
            'total_pause_duration': self.total_pause_duration,
            'window_start': self.window_start,
            'window_start_minute': self.window_start_minute,  # NEW
            'window_end': self.window_end,
            'window_end_minute': self.window_end_minute,      # NEW
            'timezone': self.timezone
        }

    @classmethod
    def from_dict(cls, data):
        routine = cls(data['chat_id'])
        routine.tasks = [RoutineTask.from_dict(t) for t in data.get('tasks', [])]
        routine.current_streak = data.get('current_streak', 0)
        routine.best_streak = data.get('best_streak', 0)
        routine.total_completions = data.get('total_completions', 0)
        routine.history = data.get('history', {})
        routine.routine_started = data.get('routine_started', False)
        if data.get('start_time'):
            routine.start_time = datetime.datetime.fromisoformat(data['start_time'])
        routine.is_setup_complete = data.get('is_setup_complete', False)
        routine.paused = data.get('paused', False)
        if data.get('pause_time'):
            routine.pause_time = datetime.datetime.fromisoformat(data['pause_time'])
        routine.total_pause_duration = data.get('total_pause_duration', 0)
        routine.window_start = data.get('window_start', 5)
        routine.window_start_minute = data.get('window_start_minute', 0)  # NEW
        routine.window_end = data.get('window_end', 11)
        routine.window_end_minute = data.get('window_end_minute', 0)      # NEW
        routine.timezone = data.get('timezone', 'Europe/Helsinki')
        return routine