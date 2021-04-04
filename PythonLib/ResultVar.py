'''
    ResultVar:

    Class defining an output variable from a simulation. 

    Has:
    - name : the name of the variable in that MATLAB workspace and the SimPage.ans object
    - unit : base unit and unit of data
'''

class ResultVar(str):
    def __new__(cls, name, unit, description = ''):
        obj = str.__new__(cls, name)
        obj.unit = unit
        obj.description = description
        return obj