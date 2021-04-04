import matlab.engine

eng = matlab.engine.start_matlab()

print('my err msg' == True)

eng.addpath(eng.fullfile(eng.pwd(), 'Supporting Functions'))
print('hi')

mydict = {'test':[1, 2, 3], 'othertest':'OtherTestString'}

eng.workspace['mystruct'] = mydict

D = eng.workspace['mystruct']
D['test'] = [1]
eng.workspace['mystruct'] = D


print(eng.getfield(eng.workspace['mystruct'], 'test'))

eng.workspace['myPressurant'] = eng.Pressurant('oxidizer')
eng.eval('myPressurant.active = 1 ;',nargout=0)
print('did eval')
print(eng.getfield(eng.workspace['myPressurant'], 'active'))