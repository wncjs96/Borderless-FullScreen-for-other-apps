# Borderless-FullScreen-for-other-apps

adjusts the other apps screen to make it bordeless fullscreen (need to be on with the app)

## Prerequisites:
Tkinter: pip install tkinter  
pynput: python -m pip install --upgrade pynput  
pywin32: pip install pywin32
 
## USAGE:
1. Pick an application
2. Set x, y, width, height for the app (for X, the windows has a 7 pixel border, so might be better having -7. width and height have default value for your primary monitor already)
3. Check the checkbox if you want to stop borderless full screen when out of focus
4. without checkbox, you can manually put it on and off.

## Work

Borderless Fullscreen merely manipulates the depth and size of the app. The rest is handled by the windows.

## License
[MIT](https://choosealicense.com/licenses/mit/)
