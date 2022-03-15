#include<Wire.h>
#include<Adafruit_PWMServoDriver.h>

#define MIN_PULSE_WIDTH 650
#define MAX_PULSE_WIDTH 2500
#define FREQUENCY 50


#define numOfValsRec 10
#define digitsPerValRec 3

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int valsRec[numOfValsRec];    //$0000000000
int stringLength = numOfValsRec * digitsPerValRec + 1;
int counter = 0;
bool counterStart = false;
String recievedString;

void setup()
{
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(FREQUENCY);

  for(int i=0;i<10;++i)
  {
    pwm.setPWM(i,0,toPulse(180));
    delay(500);
  }
 
}

void recieveData()
{
  while (Serial.available())
  {
    char c = Serial.read();
    
    if (c == '$')
    {
      counterStart = true;
    }
    if (counterStart)
    {
      if (counter < stringLength)
      {
        recievedString = String(recievedString + c);
        counter++;
      }
      if (counter >= stringLength)
      {
        //Serial.write("Recieved");
        for (int i = 0; i < numOfValsRec ; ++i)
        {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = recievedString.substring(num , num + digitsPerValRec).toInt();
          if(valsRec[i] > 180) valsRec[i] = 180;
          if(valsRec[i] < 0) valsRec[i] = 0;
         
        }
        
        recievedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}


int toPulse(int angle)
{
  int pulse_wide = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
  int pulse_width = int(float(pulse_wide) / 1000000 * FREQUENCY * 4096);
  return pulse_width;
}

void loop()
{
  recieveData();

  for(int i = 0;i<10;++i)
  {
    pwm.setPWM(i,0,toPulse(valsRec[i]));
  }
}
