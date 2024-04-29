import random
random.seed(17)
from collections import defaultdict, deque

class BaconNumberCalculator:
    """
    A class to calculate the Kevin Bacon number in a network of actors.

    Parameters
    ----------
    fileName : str
        The name of the file containing the movie data.

    Attributes
    ----------
    adjList : dict of dict/dict of list/ dict of tuple/etc...

    Methods
    -------
    generateAdjList(fileName)
        Constructs the adjacency list from the given file.
    
    calcBaconNumber(startActor, endActor)
        Calculates the Bacon number between two actors.
    
    calcAvgNumber(startActor, threshold)
        Calculates the average Bacon number for a given actor.
    """

    def __init__(self, fileName):
        """
        Constructs all the necessary attributes for the BaconNumberCalculator object.

        Parameters
        ----------
        fileName : str
            The name of the file containing the movie data.
        """
        self.adjList = {}
        self.generateAdjList(fileName)

    def generateAdjList(self, fileName):
        """
        Reads a file and builds an adjacency list representing actor connections.

        Parameters
        ----------
        fileName : str
            The name of the file to read the movie data from.
            You need to think about which encoding you should use,
	        To load the file.

        
        Attributes
        ----------
        adjList : dict of dict/dict of list/ dict of tuple/etc...
        The key of the adjList should be the original(unmodified) actor name
        in the inputted file. You should not and do not need to modify it.
        For example:
        Bacon, Kevin
        Kidman, Nicole


        Note
        ----------
        Adjacency list representing the actor connections.
        For example: 
        adjList = {actor1 : {actor2: movie1} ,{actor3: movie1}}
        or 
        adjList = {actor1 : [[actor2,movie1],[actor3, movie1]]}
        or
        ...

        Hint
        ------
        Do we need all of the movie information/name in which two 
        actors performed together stored in the adjList? 
        Or just one pair is sufficient? 
        ie  {actor1 : {actor2: movie1} }
        not  {actor1 : {actor2: [movie1,movie2]} }
        Think about how many paths we need to find between the inputted actor,
        just one or many. 

        Returns
        -------
        None
        """
        try:
            with open(fileName, 'r', encoding='ISO-8859-1') as file:
                movieDict = defaultdict(set)
                for line in file:
                # Strip leading/trailing whitespace and split by the '/' delimiter
                    parts = [part.strip() for part in line.split('/')]
                    movie, actors = parts[0], parts[1:]
                    for actor in actors:
                        movieDict[movie].add(actor.strip())
            # with open(fileName, 'r', encoding='ISO-8859-1') as file:
            #     movieDict = defaultdict(set)
            #     for line in file:
            #     # Strip leading/trailing whitespace and split by the '/' delimiter
            #         parts = [part.strip() for part in line.split('/')]
            #         movie, actors = parts[0], parts[1:]
            #         for actor in actors:
            #             movieDict[movie].add(actor.strip())

            # # Now use movieDict to create the adjacency list
            #     for movie, actors in movieDict.items():
            #         for actor in actors:
            #             if actor not in self.adjList:
            #                 self.adjList[actor] = set()
            #         # Add each co-actor along with their shared movie to this actor's set
            #             for co_actor in actors:
            #                 if co_actor != actor:  # Don't add the actor to their own list
            #                     self.adjList[actor].add((movie, co_actor))

        except IOError as e:
            print(f"An error occurred while reading the file: {e}")

        # try:
        # # Method implementation...
        #     with open(fileName, 'r', encoding='iso-8859-1') as f:
        #         data = f.read()
        #     for line in data.split('\n'):
        #         parts = line.split('/')
        #         movie = parts[0]
        #         actors = parts[1:]
        #         for i in range(len(actors)):
        #             for j in range(i + 1, len(actors)):
        #                 actor1, actor2 = actors[i], actors[j]

        #                 if actor1 not in self.adjList:
        #                     self.adjList[actor1] = {}
        #                 if actor2 not in self.adjList[actor1]:
        #                     self.adjList[actor1][actor2] = movie

        #                 if actor2 not in self.adjList:
        #                     self.adjList[actor2] = {}
        #                 if actor1 not in self.adjList[actor2]:
        #                     self.adjList[actor2][actor1] = movie

        # except I0Error as e:
        #     print(f"An error occurred: {e}")

    def calcBaconNumber(self, startActor, endActor):
        """
        Calculates the Bacon number (shortest path) between two actors.

        Parameters
        ----------
        startActor : str
            The name of the starting actor.
        endActor : str
            The name of the ending actor.

        Returns
        -------
        List[int, List[str]]
            A List containing the Bacon number and the path of connections.
            The second List should be in the following form.
            [startActor, movie1, actor1, movie2,actor1, movie3,endActor]

        Note
        -------
        1.A local variable visited:set() is needed, which avoid visiting the same
        actor more than once. 

        2.List should not be used to simulate the behavior of a queue.
        related reading:https://docs.python.org/3/tutorial/datastructures.html
        solution to is question is in the next line of the reason in the website

        3. It should return [-1, []], if one of the inputted actor is not
        in our graph.

        4.It should return [0, [start actor]], if the start actor is the end actor

        Hint
        -------
        What information you should store in the queue?
        Should it be the whole current path, or a single actor, or a tuple with 
        length of two?

        If the whole path, think about how many new list object you might create
        during the process. Notice, create a new list is not very time efficient.

        If a single actor, think about how to reconstruct the path from startActor
        to endActor. Will you need a dictionary to do so? 

        If a tuple, think about what information need to be in the tuple, and 
        how to reconstruct the path. Will you need a dictionary to do so? 

        BFS is a search algorithm that extends step by step, so if a point is traversed, 
        there is one and only one path to the point due to the visited set. 
        Each time, you enqueue an actor, 
        record the actor and movie before it in a dictionary.

        """
        prev_actor_movie = {startActor: (None, None)}
        visited = set(startActor)
        queue = deque([(startActor, None)])  # (actor, path)

        if startActor not in self.adjList or endActor not in self.adjList:
            return [-1, []]
        while queue:
            actor, _ = queue.popleft()
            if startActor == endActor:
                path = []
                path.append(actor)
                while actor != startActor:
                    actor, movie = prev_actor_movie[actor]
                    path.append(movie)
                    path.append(actor)
                path.reverse()
                return [(len(path) - 1) // 2, path]
            for neighbour, movie in self.adjList.get(actor, {}).items():
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append((neighbour, movie))
                    prev_actor_movie[neighbour] = (actor, movie)
        return [-1, []]
        
        # for movie in self.adjList.get(actor, []):
        #     for co_actor in self.adjList.get(movie, []):
        #         if co_actor not in visited:
        #                 queue.append((co_actor, path + [actor, movie]))
        # return [-1, []]

            # return [0, [startActor]]
        # parent = {startActor: None}
        # while queue:
        #     actor, path = queue.popleft()
        #     if actor == endActor:
        #         return [len(path) - 1, path + [endActor]]
        #     visited.add(actor)
        #     for movie in self.adjList.get(actor, []):
        #         for co_actor in self.adjList.get(movie, []):
        #             if co_actor not in visited:
        #                 queue.append((co_actor, path + [actor, movie]))
        # return [-1, []]

    def calcAvgNumber(self, startActor, threshold):
        """
        Calculates the average Bacon number for a given actor until convergence.

        The method iteratively selects a random actor and computes the Bacon number 
        from the startActor to this random actor. It updates and calculates the 
        average Bacon number. This process continues until the difference between 
        successive averages is less than the specified threshold, indicating convergence.

        pseudocode 
        ----------
        Initialize previousAvg to 0, curDiff to a large number (acting as infinity)
        Create a list of all possible actors from the adjacency list.
        Enter a while loop that continues as long as curDiff is greater than the threshold.
        a. Increment round count.
        b. Choose a random actor from the list of possible actors.
        c. Calculate the Bacon number (bNum) from startActor to the chosen actor.
        d. If bNum is valid (not -1 and not 0):
            adjust totalBNum and calculate the difference (curDiff) between the current and previous averages.
            Update previousAvg to the current average.
        e. If bNum is invalid, exclude it and adjust round count, undo the effect of this unsuccessful round.
        Return the previousAvg once the loop exits.

        Parameters
        ----------
        startActor : str
            The actor for whom the average Bacon number is to be calculated.
        threshold : float
            The convergence threshold for the average calculation.

        Returns
        -------
        float
            The converged average Bacon number for the startActor.
        """
        if startActor not in self.adjList:
            return float('inf')
        # Method implementation...
        previousAvg = 0
        curDiff = float('inf')
        totalBNum = 0
        round_count = 0

        all_actors = list(self.adjList.keys())

        while curDiff > threshold:
            round_count += 1
            chosen_actor = random.choice(all_actors)
            bNum, _ = self.calcBaconNumber(startActor, chosen_actor)
            if bNum != -1 and bNum != 0:
                totalBNum += bNum
                curAvg = totalBNum / round_count
                curDiff = abs(curAvg - previousAvg)
                previousAvg = curAvg
            else:
                round_count -= 1

        return previousAvg

def main():
    """function for baconnumbercalculator class"""
    file_names = "BaconCast_00_06.txt"
    calculator = BaconNumberCalculator(file_names)
    start = "Bacon, Kevin"
    end = "Kidman, Nicole"
    print("Average Bacon Number:", calculator.calcAvgNumber(start, 0.01))

    baconNumber, path = calculator.calcBaconNumber(start, end)
    if baconNumber == -1:
        print(f'{start} and {end} are not connected')
    else:
        print(f'The Bacon number between {start} and {end} is {baconNumber}')
        print(f'The path is: {path}')
if __name__ == "__main__":
    # file_names = ["ActionCast.txt", "Bacon_06.txt", "BaconCast_00_06.txt", "PopularCast.txt", "BaconCastFull.txt"]
    # for file_name in file_names:
        # calculator = BaconNumberCalculator(file_name)
        # calculator = BaconNumberCalculator("Bacon_06.txt")
        # start = "Bacon, Kevin"
        # end = "Kidman, Nicole"
        # print("Bacon Number:", calculator.calcBaconNumber(start, end))
        # print("Average Bacon Number:", calculator.calcAvgNumber(start, 0.01))