"""Interactive Labeler

This module includes an InteractiveLabeler.
"""
#import matplotlib.pyplot as plt
#from six.moves import input

from libact.base.interfaces import Labeler
from libact.utils import inherit_docstring_from
from intlabeler.intlabeler import InteractiveLabeler
import intlabeler.const.task_types as const_ttype


class MyInteractiveLabeler(Labeler):

    """Interactive Labeler

    InteractiveLabeler is a Labeler object that shows the feature through image
    using matplotlib and lets human label each feature through command line
    interface.

    Parameters
    ----------
    label_name: list
        Let the label space be from 0 to len(label_name)-1, this list
        corresponds to each label's name.

    """

    def __init__(self, **kwargs):
        self.label_name = kwargs.pop('label_name', None)
        self.il = InteractiveLabeler()

    @inherit_docstring_from(Labeler)
    def label(self, feature):
        title = 'N - alt.atheism, Y - sci.space'
        label_name = ['Y', 'N']
        print(feature)
        lbl = self.il.make_query(feature, label_name, title, const_ttype.BINARY, None)
        return self.label_name.index(lbl)