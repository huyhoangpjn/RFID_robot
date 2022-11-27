#include <AFMotor.h>
#include <SoftwareSerial.h>
#include <Servo.h>
#include <NewPing.h>
//This code is used for digital sensors (Which use emittor to emit infrared waves
//and if there is a surface in front of the sensor, the waves will reflect to the collector
//Vout = LOW
//Otherwise, if there is no wave back (all of them are absorted by black line or there is no surface to reflect to collector)
//The digital value is HIGH (detect black line or there is not wave back)

//Digital sensors work as the same way to analog but output resuls are LOW or HIGH

// initialize motors, ultra sonic sensor and servo, bluetooth (demo) in further step, we probably send message through Raspberry

AF_DCMotor motor1(1);
AF_DCMotor motor2(3);
Servo servo;

#define TRIGGER_PIN A2
#define ECHO_PIN A3
#define max_distance 80
NewPing ultrasonic(TRIGGER_PIN, ECHO_PIN, max_distance);

//initialize sensors
const int right_sensor = 2;
const int left_sensor = 3;
const int led_stop = 7;

//initialize some params
//Obstacle distance
const int threshold_obj = 15;

//Speed
const int speed_forward = 93;
//if normal power: 113
const int speed_turn = 153;
//if normal power: 163

//Angle for servo
const int init_angle = 74;
const int angle_left = init_angle + 18;
const int angle_right = init_angle - 18;
const int time_to_rotate = 2;
const int time_to_rotate_forward = 35;


int left_consecutive = 0;
int right_consecutive = 0;
//0.7 ms for 1 loop -> 10
int forward_consecutive = 0;

//long start = micros();
//long duration;
//Algorithm
//We design the robot so that the black line is between two sensor (left & right)
//If the right sensor activates, the robot turns right
//In contrast, it turns leftz
//Otherwise, it goes straight ahead

void setup() 
{
  Serial.begin(9600);
  //Stop motor
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  //Initialize pins of sensor and led on arduino 
  pinMode(left_sensor,INPUT);
  pinMode(right_sensor,INPUT);
  pinMode(led_stop, OUTPUT);
  digitalWrite(led_stop, LOW);
  servo.attach(10);
  servo.write(init_angle);
  // Activate bluetooth communication
  while(true){
    if (Serial.available() > 0){
      if (Serial.read() == '1'){
        Serial.println("Bluetooth connected!");
        delay(1000);
        break;
      }
    }
  }
}

void loop() 
{
  if((digitalRead(right_sensor) == HIGH) && (digitalRead(left_sensor) == HIGH))
  {
    Stop();
  }
  //Right sensor detects black line -> turn right
  //Servo turn left or right if the robot turns (2 consecutive left --> servo turn left)
  else if(digitalRead(right_sensor) == HIGH)
  {
    if (right_consecutive > time_to_rotate){
      servo.write(angle_right);
    }
    DetectObj();
    right();
    right_consecutive++;
    left_consecutive = 0;
    forward_consecutive = 0;
    delay(50);
  }
  //Turn left
  else if(digitalRead(left_sensor) == HIGH)
  {
    if (left_consecutive > time_to_rotate){
      servo.write(angle_left);
    }
    DetectObj();
    left();
    left_consecutive++;
    right_consecutive = 0;
    forward_consecutive = 0;
    delay(50);
  }
  //Go forward
  else
  {
    if (forward_consecutive > time_to_rotate_forward){
      servo.write(init_angle);
    }
    forward_consecutive++;
    right_consecutive = 0;
    left_consecutive = 0;
    DetectObj();
    forward();
//    Functional test
//    duration = micros() - start;
//    Serial.println(duration);
  }

//For testing:
//  Serial.print("Left sensor:");
//  Serial.println(analogRead(left_sensor));
//  Serial.print("Right sensor:");
//  Serial.println(analogRead(right_sensor));
}

void DetectObj(){
  int distance;
  boolean detected_obj;
  distance = getDistance();
  //Serial.println(distance); //(functional test)
  
  if (distance > threshold_obj){
    detected_obj = false;
    digitalWrite(led_stop, LOW);
  }
  else{
    detected_obj = true;
  }
  if (detected_obj == true)
  {
    Stop();
    //Send message
    Serial.println("WARNING: There is something blocking the line!");
    digitalWrite(led_stop, HIGH);
    delay(700);
    digitalWrite(led_stop, LOW);
    delay(700);
    DetectObj();
  }
}

int getDistance(){
  int cm;
  cm = ultrasonic.ping_cm();
  if (cm == 0){
    cm = 100; //Out of range (max_distance) -> dis = 0
  }
  return cm;
}


//Note: the speed of motors is not the same, therefore, 
//we determine a different value of these motors with an expectation that it would be more stable

void forward(){
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor1.setSpeed(speed_forward);
  motor2.setSpeed(speed_forward+2);
}


void back(){
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor1.setSpeed(speed_forward);
  motor2.setSpeed(speed_forward);
}

void left(){
  motor1.run(RELEASE);
  motor2.run(FORWARD);
  motor2.setSpeed(speed_turn);
}

void right(){
  motor1.run(FORWARD);
  motor2.run(RELEASE);
  motor1.setSpeed(speed_turn);
}

void Stop(){
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}
