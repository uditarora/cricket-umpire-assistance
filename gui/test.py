import subprocess

file1 = "/Users/udit/git/btp/object-detector/ballTracking.py"
path = "/Users/udit/Desktop/best/fast/VID_20160411_171619.mp4"
action = "0"

print "Switching to virtualenv"
# subprocess.call(["workon", "cv"])
python_bin = "/Users/udit/.virtualenvs/cv/bin/python"
# path to the script that must run under the virtualenv

print "Calling ballTracking.py"
subprocess.call([python_bin, file1, "-v", path, "-a", action])

file2 = "/Users/udit/git/btp/object-detector/3d.py"
print "Calling 3d.py"
subprocess.call(["python", file2])