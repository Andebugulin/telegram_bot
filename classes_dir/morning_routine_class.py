import datetime
import pytz
from typing import List, Dict, Optional

class RoutineTask:
    def __init__(self, name: str, duration: int, optional: bool = False):
        self.name = name
        self.duration = duration  # minutes
        self.optional = optional
        self.completed = False
        self.completed_at = None
    
    def mark_complete(self):
        self.completed = True
        self.completed_at = datetime.datetime.now(pytz.UTC)
    
    def reset(self):
        self.completed = False
        self.completed_at = None
    
    def to_dict(self):
        return {
            'name': self.name,
            'duration': self.duration,
            'optional': self.optional,
            'completed': self.completed,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        task = cls(data['name'], data['duration'], data.get('optional', False))
        task.completed = data.get('completed', False)
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
        self.history: Dict[str, Dict] = {}  # date -> {completion: %, tasks: [], duration: mins}
        self.routine_started = False
        self.start_time = None
        self.is_setup_complete = False
    
    def add_task(self, name: str, duration: int, optional: bool = False):
        if len(self.tasks) < 15:  # max 15 tasks
            self.tasks.append(RoutineTask(name, duration, optional))
            return True
        return False
    
    def remove_task(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            return True
        return False
    
    def start_routine(self):
        if not self.can_start_routine():
            return False
        self.routine_started = True
        self.start_time = datetime.datetime.now(pytz.UTC)
        # Reset all tasks
        for task in self.tasks:
            task.reset()
        return True
    
    def can_start_routine(self) -> bool:
        """Check if it's within morning window (5 AM - 11 AM local time)"""
        now = datetime.datetime.now()
        return 5 <= now.hour < 11
    
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
        """Call when user finishes routine"""
        if not self.routine_started:
            return False
        
        completion = self.get_completion_percentage()
        duration = (datetime.datetime.now(pytz.UTC) - self.start_time).total_seconds() / 60
        
        today = datetime.date.today().isoformat()
        self.history[today] = {
            'completion': completion,
            'duration': int(duration),
            'tasks': [t.to_dict() for t in self.tasks]
        }
        
        # Update streaks
        if completion >= 80:  # 80% = streak counts
            self.current_streak += 1
            self.total_completions += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
        else:
            self.current_streak = 0
        
        self.routine_started = False
        return True
    
    def check_missed_routine(self):
        """Check if user missed today's routine (called after 11 AM)"""
        now = datetime.datetime.now()
        today = datetime.date.today().isoformat()
        
        if now.hour >= 11 and today not in self.history:
            self.history[today] = {
                'completion': 0,
                'duration': 0,
                'tasks': [],
                'missed': True
            }
            self.current_streak = 0
    
    def get_weekly_stats(self):
        """Get last 7 days statistics"""
        last_7_days = []
        for i in range(6, -1, -1):
            date = (datetime.date.today() - datetime.timedelta(days=i)).isoformat()
            last_7_days.append(self.history.get(date, {'completion': 0}))
        
        completed_days = sum(1 for d in last_7_days if d.get('completion', 0) >= 80)
        avg_completion = sum(d.get('completion', 0) for d in last_7_days) / 7
        
        return {
            'completed_days': completed_days,
            'avg_completion': avg_completion,
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'total_completions': self.total_completions
        }
    
    def get_status_display(self) -> str:
        """Format current routine status for display with aligned times"""
        lines = []
        
        if self.routine_started:
            elapsed = (datetime.datetime.now(pytz.UTC) - self.start_time).total_seconds() / 60
            header = f"ROUTINE · {int(elapsed)}m"
        else:
            header = "ROUTINE"
        
        # Header with box
        lines.append(f"┏━━━━━━━━━━━━━━━━━━━━┓\n")
        lines.append(f"                 {header:^18}  \n")
        lines.append(f"┗━━━━━━━━━━━━━━━━━━━━┛\n\n")
        
        # Find longest task name for alignment
        if self.tasks:
            max_name_length = max(len(t.name) for t in self.tasks)
        else:
            max_name_length = 0
        
        # Build task list with proper alignment using inline code
        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task.completed else "○"
            opt = " `opt`" if task.optional else ""
            
            # Calculate padding to align times (each char = 1 space in monospace)
            padding = max_name_length - len(task.name)
            # Use hair space (U+200A) which Telegram preserves better
            spaces = "\u2009" * padding
            
            if task.completed:
                # Strikethrough for completed tasks
                lines.append(f"{status} `{task.name}{spaces}  {task.duration}m`{opt}\n")
            else:
                lines.append(f"{status} `{task.name}{spaces}  {task.duration}m`{opt}\n")
        
        # Footer with completion and streak
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
            'is_setup_complete': self.is_setup_complete
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
        return routine