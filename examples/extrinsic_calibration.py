import o3d3xx
import sys
import time

if len(sys.argv) > 1:
    address = sys.argv[1]
else:
    address = '192.168.0.99'

# create device
device = o3d3xx.Device(address)

# open a session and create an application for editing
session = device.requestSession()
session.startEdit()
applicationIndex = session.edit.createApplication()
application = session.edit.editApplication(applicationIndex)

# configure the application to
# - double exposure
application.imagerConfig.changeType("under5m_moderate")
# - process interface trigger
application.setParameter("TriggerMode", "2")
# and perform an auto-exposure run to determine
# exposure times
application.imagerConfig.startCalculateExposureTime()
# wait until the auto-exposure process has finished
while application.imagerConfig.getProgressCalculateExposureTime() < 1.0:
    time.sleep(1)
# name and save the application and stop editing
application.setParameter("Name", "o3d3xx-python example extrinsic calibration")

application.save()
session.edit.stopEditingApplication()

# set extrinsic calibration parameters
session.edit.device.setParameter("ExtrinsicCalibTransX", 0.0)  # mm
session.edit.device.setParameter("ExtrinsicCalibTransY", 0.0)  # mm
session.edit.device.setParameter("ExtrinsicCalibTransZ", 2530.0)  # mm
session.edit.device.setParameter("ExtrinsicCalibRotX", 6.32)  # degree
session.edit.device.setParameter("ExtrinsicCalibRotY", 5.11)  # degree
session.edit.device.setParameter("ExtrinsicCalibRotZ", 25.75)  # degree

# set the new application as active and save the change
session.edit.device.setParameter("ActiveApplication", str(applicationIndex))
session.edit.device.save()

# finish the session
session.cancelSession()

# create image client for retrieving the unit vector matrix
device = o3d3xx.ImageClient(address=address, port=50010)

# trigger device
device.sendCommand(cmd="t")
# read frames
frames = device.readNextFrame()
# print unit vector matrix
unit_vector_matrix = frames["unitVectorMatrix"]
print(unit_vector_matrix)
