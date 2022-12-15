from time import process_time
import sys
import os
import datetime
from timeit import timeit
class Message:
    def __init__(self,data) -> None:
        # self.name = name
        self.data = data
        self.time = datetime.datetime.now()
        # frameinfo = getframeinfo(currentframe())
        self.file_name,self.file_line = None,None
        # self.file_name,self.file_line = frameinfo.filename, sys._getframe().f_lineno

    def get_message(self):
        print('this is a pure message, data:', self.data)

    # def update_message(self,**kwgars):
    #     for key, value in kwgars.items():
    #         setattr(self, key, value)

    def get_data(self):return self.data
    def set_data(self, data):self.data = data
    def get_file_line(self):return self.file_line

    def get_file_name(self):return self.file_name
    def __str__(self) -> str:
        return \
f'{self.file_name}\n\
{self.data}\n\
this data is in line number: {self.file_line}\n\
{self.time}\n'


    def start(self):...

    def end(self):...

    def update(self):...

    def refresh(self):...

    def get_compound_data(self):
        return {'file_name':self.file_name, 'code_line':self.file_line, 'data':self.data}

class STR_Message(Message):
    def __init__(self, data, description='this is a message') -> None:
        super().__init__(data)
        self.description = description
    def __str__(self)->str:
        return f'{self.description}\n' + super().__str__()
    def get_compound_data(self):
        m=super().get_compound_data()
        m['message']= self.description


class TIM_Message(STR_Message):
    def __init__(self, data, description='this is a timer message') -> None:
        super().__init__(data, description) if description else super().__init__(data)
        self.create_at = process_time()
        self.accumulate = 0
        self.counter = 0
    def start(self):
        self.counter +=1
        self._start = process_time()
    def end(self, ignore_warning = False):
        """
        this is a funciton called when timer end, 
        :param bool ignore_warning: a indicator of ignorance of the warning
        :param list[int] left_bc: left boundary condition
        :param list[int] right_bc: left boundary condition
        """
        self.counter -=1
        c = self.counter
        if ignore_warning == False and c != 0:
            if c < 0:
                raise MissCall('missed_call! \n \
                                    you have called end twice, they have to show in pair \n \
                                        there is risk that timer become unprecise if this happend\
                                        if you don\'t want to see this warning, set ignore warning to True').with_traceback()
            else:
                raise MissCall('missed_call! \n \
                                    you have called end twice, they have to show in pair \n \
                                        there is risk that timer become unprecise if this happend\
                                        if you don\'t want to see this warning, set ignore warning to True').with_traceback()
        self._end = process_time()
        self.accumulate += self._end - self._start
    def update(self):
        raise NotImplementedError(message ='this method has no use in time function')
    def refresh(self):
        self.accumulate =0
    def get_compound_data(self):
        m = super().get_compound_data()
        m['time'] =self.accumulate
    def __str__(self):
        return f'time_accumulate: {self.accumulate}\n' +super().__str__()

class CTR_Message(STR_Message):
    def __init__(self, data, test_string=None) -> None:
        
        super().__init__(data, test_string) if test_string else super().__init__(data)
        self.create_at = process_time()
        self.counter = 0
        self.pause = True
    def start(self):self.pause= False
    def end(self):self.pause= True
    def update(self):self.counter +=1 if self.pause == False else ...
    def refresh(self):self.counter =0
    def get_compound_data(self):
        m= super().get_compound_data()
        m['counter'] = self.counter
    def __str__(self) -> str:
        return f'count: {self.counter}\n' + super().__str__()

class MissCall(Exception):
    def __init__(self, message = 'missed called'):
        self.message = message
        super().__init__(self.message)
class NoSuchMessageError(Exception):
    def __init__(self,name, message = 'no such Message named: '):
        self.message = message + str(name)
        super().__init__(self.message)


class MessagePool():
    pool = []
    def new_message(self,name,data,index,description = ''):
        """_summary_

        Args:
            name (string): name of the message
            data (not known): could be any type, data printed
            description (str, optional): description of this test message. Defaults to ''.
            index (str, optional): type of message to create. Defaults to 's'or't'or'c'.

        Raises:
            NoSuchMessageError: _description_
        """
        if hasattr(self, name):
            getattr(self, name).data = data
        else: 
            if index == 's':
                setattr(self, name, STR_Message(data, description))
            elif index == 't':
                setattr(self, name, TIM_Message(data, description))
            elif index == 'c':
                setattr(self, name, CTR_Message(data, description))
            else:
                raise NoSuchMessageError(name = index, message='no such message based on index: ')
            self.pool.append(name)
            # print(getattr(self, name))

    def print_message(self, name):
        message = getattr(self, name)
        print(message)
    
    def set_printing_method(self,name,function):
        #TODO not yet implemented
        self.print_function = function
    def print_data(self, name):
        """print only data

        Args:
            name (string): name of the message

        Raises:
            NoSuchMessageError: name of the message is not correct
        """        
        if hasattr(self, name):
            m:Message = getattr(self, name)
            data = m.get_data()
            if self.print_function:
                self.print_function(data)
            else:
                print(data)
        else:
            raise NoSuchMessageError(name = name)
            
    def get_message(self, name):
        """get message with name given

        Args:
            name (string): name of the message

        Returns:
            Message: message type
        """        
        return getattr(self, name)
    def get_all_message_name(self):
        return [message for message in getattr(self)]
    def timer(e):
        pass

class Tester:   
    mp = MessagePool()
if __name__ =="__main__":
    t=Tester()
    m = t.mp.new_message('x',3,'s','test message')
    m = t.mp.new_message('x',1,'s','test message')
    print(timeit(\
        """Tester.mp.new_message('x',3,'s','test message');Tester.mp.new_message('x',1,'s','test message')"""\
            ,setup='from __main__ import Tester', number =10000000)) 
    print(type(m))