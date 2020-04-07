import telnetlib, socket, ftplib, time, datetime

import logging
import numpy as np
np.set_printoptions(threshold=np.inf)


log = logging.getLogger('root')

ftp = ftplib.FTP('169.254.13.237')
ftp.login()

print(ftp.getwelcome())
temp = ftp.sendcmd('.image.state.live.set true\n')
print(temp)
ftp.quit()
