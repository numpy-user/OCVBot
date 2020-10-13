- https://www.jetbrains.com/help/pycharm/run-debug-configuration.html
- https://realpython.com/python-testing/
- https://realpython.com/python-refactoring/
- https://towardsdatascience.com/ultimate-setup-for-your-next-python-project-179bda8a7c2c
- https://realpython.com/python-application-layouts/
- https://docs.python-guide.org/writing/structure/
- http://www.patricksoftwareblog.com/python-documentation-using-sphinx/
- https://coverage.readthedocs.io/en/coverage-5.1/
- https://www.jetbrains.com/pycharm/whatsnew/
- https://www.jetbrains.com/help/pycharm/activity-monitor.html
- https://www.jetbrains.com/help/pycharm/guided-tour-around-the-user-interface.html
- multi-template matching with opencv: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
- more template matching with opencv https://docs.opencv.org/3.4/de/da9/tutorial_template_matching.html
- run pyautogui.mouseinfo to get image and mouse info
- versioning: https://stackoverflow.com/questions/37814286/how-to-manage-the-version-number-in-git
- git workflow: https://nvie.com/posts/a-successful-git-branching-model/, https://nvie.com/files/Git-branching-model.pdf
- simpler git workflow: https://guides.github.com/introduction/flow/
- use azure as VPS for bot
- fix filepaths in python for cross-compatibility: https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
- path runtime info for pyinstaller: https://pyinstaller.readthedocs.io/en/stable/runtime-information.html
  - more info on settings correct working dir for file: https://stackoverflow.com/questions/2632199/how-do-i-get-the-path-of-the-current-executed-file-in-python/18489147#18489147
- determine filepath when running python as exe: http://www.py2exe.org/index.cgi/WhereAmI
- import image in numpy array
- create GIF from video for README: https://askubuntu.com/questions/648603/how-to-create-an-animated-gif-from-mp4-video-via-command-line
- reading for devolpers: https://blog.codinghorror.com/recommended-reading-for-developers/
- code smells: https://blog.codinghorror.com/code-smells/
- https://www.smartspate.com/how-to-write-a-bot-in-python-for-online-games/ 
- https://github.com/PyUserInput/PyUserInput 
- https://www.reddit.com/r/programming/comments/7wivfv/reverse_engineering_a_mmorpg_bot_to_find/ 
```python
import cv2

im = cv2.imread('kolala.jpeg')
img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)   # BGR -> RGB
cv2.imwrite('opncv_kolala.png', img)
print (type(img))
```
- pyautogui screenshot to numpy array
```python
image = pyautogui.screenshot()
image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
cv2.imwrite("in_memory_to_disk.png", image)
```
- move all vision constants out of __init__.py and into vision.py, outside of the class. also move everything from init_vision() outside of its function. this will allow us to access Vision objects without needing to run init_vision().
- switch from pyautogui to mss for screenshots https://python-mss.readthedocs.io/examples.html
- use pysimplegui instead of tkinter for GUI https://pysimplegui.readthedocs.io/en/latest/cookbook/
- using opencv for GTAV https://pythonprogramming.net/game-frames-open-cv-python-plays-gta-v/
- managing timers: https://stackoverflow.com/questions/7370801/measure-time-elapsed-in-python?rq=1
- pytest testing for expected exceptions https://docs.pytest.org/en/latest/assert.html
- travis-ci GUI testing https://docs.travis-ci.com/user/gui-and-headless-browsers/
- code profiling: https://docs.python.org/3.8/library/profile.html#module-cProfile
  - view code profiling result in GUI: http://www.vrplumber.com/programming/runsnakerun/
- opencv performance measuring: https://docs.opencv.org/master/dc/d71/tutorial_py_optimization.html
  - opencv template matching with confidence interval: https://www.geeksforgeeks.org/template-matching-using-opencv-in-python/
  - opencv grab mouse events to replace feh for testing: https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/, https://stackoverflow.com/questions/28327020/opencv-detect-mouse-position-clicking-over-a-picture/49338267
- python performance tips: https://wiki.python.org/moin/PythonSpeed/PerformanceTips
- opencv resize image: https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
