# missilecmd
Trying to re-create the Atari Missile Command of my youth. Trying to learn pygame.


# Assets
All assets with the exception of assets/launcher belong to their respective owners.
I downloaded fonts from https://www.1001freefonts.com/
Other images and sounds were downloaded from https://opengameart.org/

# Install
These are the steps I recommend installing this game. I'm using python's virtualenv to make it easy to uninstall (you just remove the directory and your system is back to what it was before.)

Download the zip file to your machine.

    cd /tmp
    mv ~/Downloads/missilecmd-main.zip .
    unzip missilecmd-main.zip
    cd missilecmd-main
    virutalenv -p python3 venv
    source ./venv/bin/activate
    pip install -r requirements.txt
    ./main.py

# Uninstall

    rm -rf /tmp/missilecmd-main.py
    
# Rules
Keys 1,2 and 3 select the launcher.  
Mouse click to set the missile target.  
No limits on number of missiles.  
No way to die.  
Press ESC to quit.  
Enjoy!  

