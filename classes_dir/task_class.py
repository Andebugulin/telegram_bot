import datetime
import pytz
import math


class Task:

    def __init__(self, name: str, duration: int) -> None:
        """container

        Args:
            name (str): name of the task; <example> str("Neural Network")
            duration (int): duration of the task in minutes; <example> int(10)
        """
        self.name = name 
        self.remaining_time = duration
        self.going = False
        self.last_time_hit_start_stop = datetime.datetime.now()
        
        # TODO: man you gotta use native datetime over aware datetime.
        timezone = pytz.timezone('UTC')        
        # Convert the naive datetime to an aware datetime
        self.last_time_hit_start_stop = timezone.localize(self.last_time_hit_start_stop)

    def __str__(self)  -> str:
        """
        Returns:
            str : formatted task within a string type; <example> str("<code> Hello everyone in my bot </code>")
        """
        # * only formatting, not important part
        # * start FORMATTING
        space1, space2, space3, space4 = (0, 0, 0, 0)
        printing_remaining_time = ''
        
        if len(self.name) > 18:
                space1 = 0
                space2 = 0
        else:
            space1 = (18 - len(self.name)) / 2
            if space1 % 1 == 0:
                space1 = int(space1)
                space2 = space1
            else:
                space1 = int(math.ceil(space1))
                space2 = space1 - 1


        if self.remaining_time > 0:

            hours, minutes = self.remaining_time // 60, self.remaining_time % 60
            if self.remaining_time > 599 and self.remaining_time % 60 < 10 and self.remaining_time % 60 > 0:
                printing_remaining_time =  f'0{hours}:0{minutes} h:m'  
            elif self.remaining_time > 120 and self.remaining_time % 60 < 10 and self.remaining_time % 60 >= 0:
                printing_remaining_time =  f'0{hours}:0{minutes} h:m'
            elif self.remaining_time > 120 and self.remaining_time % 60 >= 0:
                printing_remaining_time =  f'0{hours}:{minutes} h:m'
            elif self.remaining_time > 60 and self.remaining_time % 60 < 10 and self.remaining_time % 60 >= 0:
                printing_remaining_time =  f'0{hours}:0{minutes} h:m' 
            elif self.remaining_time > 60 and self.remaining_time % 60 != 0:
                printing_remaining_time =  f'0{hours}:{minutes} h:m'
            elif self.remaining_time == 60:
                printing_remaining_time =  f'0{hours}:00 h:m'
            elif self.remaining_time < 60 and self.remaining_time > 9:
                printing_remaining_time =  f'{minutes} min'
            elif self.remaining_time < 60 and self.remaining_time < 10:
                printing_remaining_time =  f' {minutes} min'
            

            if len(printing_remaining_time) > 11:
                space3 = 0
                space4 = 0
            else:
                space3 = 1
                space4 = (11 - len(printing_remaining_time) - space3)
        else:
            if len('*') > 20:
                space3 = 0
                space4 = 0
            else:
                space3 = (20 - len('*') ) / 2
                if space3 % 1 == 0:
                    space3 = int(space3)
                    space4 = space3
                else:
                    space3 = int(math.floor(space3))
                    space4 = space3 + 1 
        # * stop FORMATTING 
        
        
        if self.remaining_time > 0:
            if self.going:
                return f" <b>|<code><b>{' ' * space1}{self.name}{' ' * space2}</b> </code> | <code>{'<code> </code>' * space3}{printing_remaining_time}{'<code> </code>' * space4}</code> |</b>"
            else:
                return f"~<i><code>{' ' * space1}{self.name}{' ' * space2}</code></i>  ~<i><code>{'<code> </code>' * space3}{printing_remaining_time}{'<code> </code>' * space4}</code></i>~"
        else:    
            return f" * <code>{' ' * space1}{self.name}{' ' * space2}</code> *"

    def __dict__(self) -> dict:
        """Returns:
            dict : {
                [str]: [object]
            }
        """
        return {
                'name': str(self.name), #string
                'remaining_time': int(self.remaining_time), #int
                'going' : bool(self.going), #boolean
                'last_time_hit_start_stop': self.last_time_hit_start_stop.strftime("%Y-%m-%d %H:%M:%S") # should be datetime, but I do not wanna write specific json decoder of datetime, so, i just use convertion to string.
                }
    
    def start_stop_timer(self, date_time: datetime)  -> None: # type: ignore
        """function to start or stop a timer

        Args:
            date_time (datetime): _description_
        """
        if self.remaining_time > 0:
            if not self.going:
                # TODO: man you gotta use native datetime over aware datetime. 
                self.last_time_hit_start_stop = datetime.datetime.now()
                timezone = pytz.timezone('UTC')        
                # Convert the naive datetime to an aware datetime
                self.last_time_hit_start_stop = timezone.localize(self.last_time_hit_start_stop)
                self.going = True
            else:
                # Later, when you want to calculate the difference:
                current_time = date_time
                time_difference = current_time - self.last_time_hit_start_stop # type: ignore

                # Extract minutes and hours from the timedelta
                minutes, secods = divmod(time_difference.seconds, 60)
                self.remaining_time -= minutes
                self.going = False 
        
    def check(self, date_time: datetime) -> None: # type: ignore
        if self.remaining_time > 0:
            if not self.going:
                # TODO: man you gotta use native datetime over aware datetime.
                self.last_time_hit_start_stop = datetime.datetime.now()
                timezone = pytz.timezone('UTC')        
                self.last_time_hit_start_stop = timezone.localize(self.last_time_hit_start_stop)
            else:
                timezone = pytz.timezone('UTC')   
                # TODO: man you gotta use native datetime over aware datetime.
                current_time = timezone.localize(date_time) # type: ignore
                time_difference = current_time - self.last_time_hit_start_stop

                # Extract minutes and hours from the timedelta
                minutes, secods = divmod(time_difference.seconds, 60)
                self.remaining_time -= minutes
                if minutes != 0:
                    self.last_time_hit_start_stop = datetime.datetime.now()
                    timezone = pytz.timezone('UTC')        
                    # TODO: man you gotta use native datetime over aware datetime.
                    self.last_time_hit_start_stop = timezone.localize(self.last_time_hit_start_stop)

                if self.remaining_time <= 0:
                    self.going = False
