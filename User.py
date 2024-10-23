# =============================================================================
# Class to create a user with his planning.
# =============================================================================

class User :
    def __init__(self, name) :
        self.name = name
        self.planning = ["''" for i in range(24)]
        
    
    def addInPlanning(self, start, end, status) :
        """
        Add a status in the planning.
        
        Parameters
        ----------
        start : INTEGER
            Start hour.
        end : INTEGER
            End hour.
        status : STRING
            Associated status.

        Returns
        -------
        None.

        """
        for i in range(start, end) :
            self.planning[i] = status
    
    def getPlanning(self) :
        """
        Print the planning.

        Returns
        -------
        None.

        """
        for i in range(0, len(self.planning)) :
            print(i, " - ", i+1, " : ", self.planning[i])
        
    def predefinedPlanning(self) :
        """
        Generate a predefined planning.

        Returns
        -------
        None.

        """
        self.addInPlanning(14,15,"REUNION")
        self.addInPlanning(15,16,"TRAVAIL")

        