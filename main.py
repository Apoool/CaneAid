import RPi.GPIO as GPIO
import pygame
import time
import subprocess
import os
import shutil
import cv2

water_sensor_pin = 13
button = 18
TRIG = 16
ECHO = 15
path = "/home/caneaid/Desktop/Main/results"
path_file = "/home/caneaid/Desktop/Main/results/image.txt"
path_audio = "/home/caneaid/Desktop/Main/audio/"
model = "model_1" #default
path_model = "/home/caneaid/Desktop/Main/models_dir/selected_model.txt"

#Initiate pygame and opencv version
pygame.mixer.init()
print(cv2.__version__)

#for testing2
def readModel():
	with open(path_model, "r") as f:
		model = f.readlines()	
		print(model)

#initiate GPIO setup
def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(TRIG,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)
	GPIO.output(TRIG, False)
	GPIO.setup(water_sensor_pin, GPIO.IN)
	readModel()

def loop():
	#initiate water sensor variable so that it will detect once every restart of the system
	water_detect = 0
	
	#initiate greeting
	pygame.mixer.music.load(path_audio + "good_day.mp3")
	pygame.mixer.music.play()
	while pygame.mixer.music.get_busy() == True:
		continue
	while True:

		#read button state
		button_state = GPIO.input(button)
		
		#read ultrasonic reading
		GPIO.output(TRIG, True)
		time.sleep(1)
		GPIO.output(TRIG, False)
		while GPIO.input(ECHO)==0:
			pulse_start = time.time()
		while GPIO.input(ECHO)==1:
			pulse_end = time.time()
			
		#calculate the data into centimeters
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance+1.15)
		
		#Water sensor
		if water_detect == 0:
			if GPIO.input(water_sensor_pin):
				#print(water_sensor_pin)
				water_detect = 1
				pygame.mixer.music.load(path_audio+ "water_detected.mp3")
				pygame.mixer.music.play()
				while pygame.mixer.music.get_busy() == True:
					continue
				print("1")
			else:
				print("0")
				#print(water_sensor_pin)
		#else:
			#print("water")

		#Check if button state has been clicked
		#Button for image capture and processing
		if  button_state == False:
			print('Button Pressed...')
			print(distance)
			pygame.mixer.music.load(path_audio+"btn_prs.mp3")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
				continue
			
			#image capture
			subprocess.call(["raspistill", "-t", "500", "-o", "/home/caneaid/Desktop/Main/image.jpg"])
			#image object detection
			subprocess.call(["python", "/home/caneaid/Desktop/Main/core/image_detection.py", 
			f"--modeldir=/home/caneaid/Desktop/Main/models_dir/{model}", "--threshold=.6", "--save_results", "--image=/home/caneaid/Desktop/Main/image.jpg"])
			
			#If no objects detected, speech output will tell
			print(os.stat(path_file).st_size)
			if os.stat(path_file).st_size != 0:
				with open("/home/caneaid/Desktop/Main/results/image.txt", "r") as f:
					content = f.readlines()

				# Create a list to store the words
				words = []

				# Iterate over each line in the file
				for line in content:
					# Remove any whitespace or newline characters
					word = line.strip()
					# Add the word to the list
					words.append(word)
				print(words)
				print(len(words))
				
				for x in words:
					print(x)
					pygame.mixer.music.load(path_audio+ x + ".mp3")
					pygame.mixer.music.play()
					while pygame.mixer.music.get_busy() == True:
						continue
						
				#to reset the results path by deleting it
				if os.path.exists(path):
					# delete the directory
					shutil.rmtree(path)
					print("Folder deleted successfully")
				else:
					print("Folder does not exist")
				
				
			else:
				#unidentified object will play in speech output
				pygame.mixer.music.load(path_audio+ "no_obstacle.mp3")
				pygame.mixer.music.play()
				while pygame.mixer.music.get_busy() == True:
					continue
				print("EMPTY")
				
			#If button is still pressed this loop will run
			while GPIO.input(button) == False:
				print('?')
				time.sleep(0.2)

		#ultrasonic sensor detect
		#change to 150 cm (150cm = 1.5m) according to papers
		#20 cm for testing
		if distance <= 150:
			pygame.mixer.music.load(path_audio + "obstacle_close.mp3")
			pygame.mixer.music.play()
			while pygame.mixer.music.get_busy() == True:
				continue
			print("too close")
			
			#Image capture and object detection function if the button is still clicked after the ultrasonic speech output play
			#Button for image capture and processing
			if  button_state == False:
				print('Button Pressed...')
				print(distance)
				pygame.mixer.music.load(path_audio+"btn_prs.mp3")
				pygame.mixer.music.play()
				while pygame.mixer.music.get_busy() == True:
					continue
			
				#image capture
				subprocess.call(["raspistill", "-t", "500", "-o", "/home/caneaid/Desktop/Main/image.jpg"])
				#image object recognition
				subprocess.call(["python", "/home/caneaid/Desktop/Main/core/image_detection.py", 
				f"--modeldir=/home/caneaid/Desktop/Main/models_dir/{model}", "--threshold=.75", "--save_results", "--image=/home/caneaid/Desktop/Main/image.jpg"])
			
				
				print(os.stat(path_file).st_size)
				if os.stat(path_file).st_size != 0:
					with open("/home/caneaid/Desktop/Main/results/image.txt", "r") as f:
						content = f.readlines()

					# Create a list to store the words
					words = []

					# Iterate over each line in the file
					for line in content:
						# Remove any whitespace or newline characters
						word = line.strip()
						# Add the word to the list
						words.append(word)
					print(words)
					print(len(words))
				
					for x in words:
						print(x)
						pygame.mixer.music.load(path_audio+ x + ".mp3")
						#pygame.mixer.music.load("ako.mp3")
						pygame.mixer.music.play()
						while pygame.mixer.music.get_busy() == True:
							continue
						
					#to reset the results path by deleting it
					if os.path.exists(path):
						# delete the directory
						shutil.rmtree(path)
						print("Folder deleted successfully")
					else:
						print("Folder does not exist")
				
				
				else:
					pygame.mixer.music.load(path_audio+ "un_obstacle.mp3")
					pygame.mixer.music.play()
					while pygame.mixer.music.get_busy() == True:
						continue
					print("EMPTY")
				
				#If button is still pressed this loop will run
				while GPIO.input(button) == False:
					print('?')
					time.sleep(0.2)


			
def endprogram():
	GPIO.cleanup()


if __name__ == '__main__':
          
          setup()
          
          try:
                 loop()
          
          except KeyboardInterrupt:
                 print ('keyboard interrupt detected' )
                 endprogram()
