# discord-music-bot

Will do automatic search on youtube and play that song for you 

Added recommendation and loop features 

!play {song-name} (alias - !p {song-name})- to join the channel you are in and play your given song 
!pause - to pause the current song 
!resume / !res - to resume the song 
!skip - to skip the current song 
!skipall - to remove all songs from the queue
!recommend / !r n{no of songs to recommend} - to recommend next n songs based on current song 
!loop - put loop on the current song 
!unloop - to unloop the current song 
!leave / !lv - to leave the channel and remove all songs from the queue 




### For running 24/7 , Make a account on azure or your preferred choice and make a virtual machine and do the following steps on the vm (virtual machine).

## Installation 

Run -
```pip3 install -m requirements.txt``` 

```sudo apt install ffmpeg``` (necessary as discord client supports that only)

Now run , ```python3 final3.py``` to run the discord music bot.

Now sit back and enjoy the music ...
