import subprocess, time
import signal
import os
def check_emergency():
	while True:
		#cmd = '/opt/ros/kinetic/bin/roslaunch eva_arm_controller eva_arm_controller.launch'
		#get_pid_cmd = 'pgrep rosmaster'
		cmd = 'sleep 20 '
		music_cmd = 'mpg123 /home/asimov/IRA_V2_ws/src/audio/emergency.mp3' #enter the command for playing music (release emeergency)
		emergency = subprocess.Popen(cmd,shell=True,stdin = subprocess.PIPE)
		time.sleep(15)
		res = emergency.poll()
		if res == None:
			print("emergency ok")
#			act = subprocess.Popen(get_pid_cmd.split(), stdout=subprocess.PIPE)
#			out, err = act.communicate()
#			out1 = out.rstrip()
#			int_out = int(out1)
			emergency.kill()
			time.sleep(2)
#			os.killpg(int_out, signal.SIGTERM)
			time.sleep(2)
			break
		else :
			music = subprocess.Popen(music_cmd,shell=True)
			music.wait()
			time.sleep(3)
def check_network():
	while True:
		cmd = 'ping -c 1 www.google.com'
		music_cmd = 'mpg123 /home/asimov/IRA_V2_ws/src/audio/internet.mp3'#enter the command for playing music (check internet)
		net = subprocess.call(cmd,shell=True)
		if net == 0:
			print("internet ok")
			break
		else :
			music = subprocess.Popen(music_cmd,shell=True)
			music.wait()
			time.sleep(3)

if __name__ == '__main__':
	#check_emergency()
	time.sleep(5)
#	check_network()





