class MaintenanceWindow(object):
    def __init__(self, dayOfTheWeek, time):
        """
        MaintenanceWindow class initializer.

        :param      dayOfTheWeek: The day of the week for a maintenance window.
        :type       dayOfTheWeek: ``str`` ["Monday",
                                            "Tuesday",
                                            "Wednesday",
                                            "Thursday",
                                            "Friday",
                                            "Saturday",
                                            "Sunday"]

        :param      time: The time to use for a maintenance window. Accepted formats are: HH:mm:ss; HH:mm:ss"Z";
                        HH:mm:ssZ. This time may varies by 15 minutes.
        :type       time: ``string``

        """
        self.dayOfTheWeek = dayOfTheWeek
        self.time = time

    def __repr__(self):
        return ('<MaintenanceWindow: dayOfTheWeek=%s, time=%s>'
                % (self.dayOfTheWeek, self.time))
