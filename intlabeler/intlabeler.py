"""Interactive Labeler

This module includes an InteractiveLabeler.
"""


class MyInteractiveLabeler:

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

    @inherit_docstring_from(Labeler)
    def label(self, feature):
        plt.imshow(feature, cmap=plt.cm.gray_r, interpolation='nearest')
        plt.draw()
