class AutoScaling(object):
    def __init__(self, minNodeCount, maxNodeCount):
        """
        AutoScaling class initializer.

        :param      minNodeCount": The minimum number of worker nodes that the managed node group can scale in.
                        Should be set together with 'maxNodeCount'.
                        Value for this attribute must be greater than equal to 1 and less than equal to maxNodeCount.
        :type       minNodeCount" : ``integer``

        :param      maxNodeCount: The maximum number of worker nodes that the managed node pool can scale-out.
                        Should be set together with 'minNodeCount'.
                        Value for this attribute must be greater than equal to 1 and minNodeCount.
        :type       maxNodeCount: ``integer``

        """
        self.minNodeCount = minNodeCount
        self.maxNodeCount = maxNodeCount

    def __repr__(self):
        return ('<AutoScaling: minNodeCount=%s, maxNodeCount=%s>'
                % (str(self.minNodeCount), str(self.maxNodeCount)))
