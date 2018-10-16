goto comment

**** 这里是注释 ****

使用nosetests测试的时候总是import error，之前用try expect处理，现在将project根目录加到sys.path中，然后一律使用 import core.common这类方式处理
或者弄一个setup函数，在import之前执行下面这几句也可以
import os
import sys
sys.path.append(os.path.abspath('.'))

:comment

nosetests -v -s test/ --with-path=.