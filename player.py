from media import Media, Track, Movie
from linked_list import LinkedList
import json
class Player:
    """
    A media player class that manages a playlist of media.

    This class utilizes a doubly linked list (LinkedList) to store and manage media in a playlist.
    It provides methods for adding, removing, playing, and navigating through media.

    Attributes
    ----------
    playlist : LinkedList
        A doubly linked list that stores the media in the playlist.
    currentMediaNode : Node or None
        The current media being played, represented as a node in the linked list.
    """

    def __init__(self):
        """
        Initializes the Player with an empty playlist and None as currentMediaNode.
        """
        self.playlist = LinkedList()
        self.currentMediaNode = None

    def addMedia(self, media):
        """
        Adds a media to the end of the playlist.
        Set the currentMediaNode to the first node in the playlist,
        if currentMediaNode is None.

        Parameters
        ----------
        media : Media | Track | Movie
            The media to add to the playlist.
        """
        self.playlist.append(media)
        if self.currentMediaNode is None:
            self.currentMediaNode = self.playlist.dummyHead.next

    def removeMedia(self, index) -> bool:
        """
        Removes a media from the playlist based on its index.
        You can assume the only invalid input is invalid index.
        Set the currentMediaNode to its next, if currentMediaNode is removed,
        and remember using _isNodeUnbound(self.currentMediaNode) to check if a link is broken.

        Parameters
        ----------
        index : int
            The index of the media to remove.

        Returns
        -------
        bool
            True if the media was successfully removed, False otherwise.
        """
        if self.playlist.deleteAtIndex(index):
            if self.currentMediaNode is not None and self._isNodeUnbound(self.currentMediaNode):
                self.currentMediaNode = self.currentMediaNode.next
            return True
        return False

    def next(self) -> bool:
        """
        Moves currentMediaNode to the next media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the next media, False otherwise.
        """
        if self.currentMediaNode is not None and self.currentMediaNode.next != self.playlist.dummyTail:
            self.currentMediaNode = self.currentMediaNode.next
            return True
        return False

    def prev(self) -> bool:
        """
        Moves currentMediaNode to the previous media in the playlist.
        This method should not make self.currentMediaNode be self.playlist.dummyNode.

        Returns
        -------
        bool
            True if the player successfully moved to the previous media, False otherwise.
        """
        if self.currentMediaNode is not None and self.currentMediaNode.prev != self.playlist.dummyHead:
            self.currentMediaNode = self.currentMediaNode.prev
            return True
        return False

    def resetCurrentMediaNode(self) -> bool:
        """
        Resets the current media to the first media in the playlist,
        if the playlist contains at least one media. 

        Returns
        -------
        bool
            True if the current media was successfully reset, False otherwise.
        """
        if self.playlist.getSize() > 0:
            self.currentMediaNode = self.playlist.dummyHead.next
            return True
        return False

    def play(self):
        """
        Plays the current media in the playlist. 
        Call the play method of the media instance.
        Remeber currentMediaNode is a node not a media, but its data is the actual
        media. If the currentMediaNode is None or its data is None, 
        print "The current media is empty.". 
        """
        if self.currentMediaNode is not None and self.currentMediaNode.data is not None:
            self.currentMediaNode.data.play()
        else:
            print("The current media is empty.")

    def playForward(self):
        """
        Plays all the media in the playlist from front to the end,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print "Playlist is empty.". 
        """
        if self.playlist.getSize() == 0:
            print("Playlist is empty.")
            return
        curr = self.playlist.dummyHead.next
        while curr != self.playlist.dummyTail:
            if curr.data is not None:
                curr.data.play()
            curr = curr.next

    def playBackward(self):
        """
        Plays all the media in the playlist from the back to front,
        by iterating the linked list.  
        Remeber each media information should take one line. (follow the same
        format in linked list)
        If the playlist is empty, print this string "Playlist is empty.". 
        """
        if self.playlist.getSize() == 0:
            print("Playlist is empty.")
            return
        curr = self.playlist.dummyTail.prev
        while curr != self.playlist.dummyHead:
            if curr.data is not None:
                curr.data.play()
            curr = curr.prev

    def loadFromJson(self, fileName):
        """
        Loads media from a JSON file and adds them to the playlist.
        The order should be the same as the provided json file. 
        You could assume the filename is always valid
        Notice, for each given json object, 
        you should create instance of the correct instance type, (movie,track,media).
        You need to observe the provided json and figure how to do it.
        You could assume if a json object is not track or movie,
        it has to be a media.
        Pay attention the name of the key in each json object. 
        Set the currentMediaNode to the first media in the playlist, 
        if there is at least one media in the playlist.
        Remeber to use the dictionary get method. 

        Parameters
        ----------
        filename : str
            The name of the JSON file to load media from.
        """
        with open(fileName, 'r') as file:
            data = json.load(file)
            for item in data:
                if 'genre' in item:
                    media = Track(item['title'], item['artist'], item['releaseDate'], item['url'], item['album'], item['genre'], item['duration'])
                elif 'rating' in item:
                    media = Movie(item['title'], item['artist'], item['releaseDate'], item['url'], item['rating'], item['movieLength'])
                else:
                    media = Media(item['title'], item['artist'], item['releaseDate'], item['url'])
                self.addMedia(media)
            if self.playlist.getSize() > 0:
                self.currentMediaNode = self.playlist.dummyHead.next

    def _isNodeUnbound(self, node):
        return node.prev is None or node.next is None

if __name__ == "__main__":
    player = Player()
    player.loadFromJson("playlist.json")
    player.playForward()
