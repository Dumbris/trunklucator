import numpy as np
from intlabeler.intlabeler import InteractiveLabeler
import intlabeler.const.task_types as const_ttype



def simple():
    X = np.array([[1,2],[3,4],[5,6]])
    y = np.array([0,1,0])
    label_name = ['Y', 'N']
    il = InteractiveLabeler()
    y_ = il.make_query(X,label_name, "Simple test", const_ttype.BINARY, y)
    print(y_)



if __name__ == '__main__':
    simple()