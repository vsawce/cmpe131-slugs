// scrolltext demo for Adafruit RGBmatrixPanel library.
// Demonstrates double-buffered animation on our 16x32 RGB LED matrix:
// http://www.adafruit.com/products/420
// DOUBLE-BUFFERED ANIMATION DOES NOT WORK WITH ARDUINO UNO or METRO 328.

// Written by Limor Fried/Ladyada & Phil Burgess/PaintYourDragon
// for Adafruit Industries.
// BSD license, all text above must be included in any redistribution.

#include <RGBmatrixPanel.h>
//#include <SoftwareSerial.h>

// Most of the signal pins are configurable, but the CLK pin has some
// special constraints.  On 8-bit AVR boards it must be on PORTB...
// Pin 11 works on the Arduino Mega.  On 32-bit SAMD boards it must be
// on the same PORT as the RGB data pins (D2-D7)...
// Pin 8 works on the Adafruit Metro M0 or Arduino Zero,
// Pin A4 works on the Adafruit Metro M4 (if using the Adafruit RGB
// Matrix Shield, cut trace between CLK pads and run a wire to A4).

#define CLK  8   // USE THIS ON ADAFRUIT METRO M0, etc.
//#define CLK A4 // USE THIS ON METRO M4 (not M0)
//#define CLK 11 // USE THIS ON ARDUINO MEGA
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2
#define BUFFER_SIZE 64

// Last parameter = 'true' enables double-buffering, for flicker-free,
// buttery smooth animation.  Note that NOTHING WILL SHOW ON THE DISPLAY
// until the first call to swapBuffers().  This is normal.
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);
//SoftwareSerial mySerial(12, 13); //RX TX

// Similar to F(), but for PROGMEM string pointers rather than literals
#define F2(progmem_ptr) (const __FlashStringHelper *)progmem_ptr

//const char str[] = "51.76F|Rain|72:5m|17:18m|C.Katsu|N:99%|S:38%|SW:45%";
//int16_t    textX         = matrix.width(),
//          textMin       = (int16_t)sizeof(str) * -12,
//          hue           = 0;

int16_t    textX, textMin, hue;
char buf[BUFFER_SIZE];

int8_t ball[3][4] = {
  {  3,  0,  1,  1 }, // Initial X,Y pos & velocity for 3 bouncy balls
  { 17, 15,  1, -1 },
  { 27,  4, -1,  1 }
};
static const uint16_t PROGMEM ballcolor[3] = {
  0x0080, // Green=1
  0x0002, // Blue=1
  0x1000  // Red=1
};

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600); //Arduino Hardware RX/TX
  //char str[] = "51.76F|Rain|72:5m|17:18m|C.Katsu|N:99%|S:38%|SW:45%";
  
  digitalWrite(LED_BUILTIN, LOW);

  delay(10000); //Allow for garbage serial to pass

  bool breakLoop = false;
  while (!breakLoop) {
    while (Serial.available()) {
      String temp_str = Serial.readString();
      temp_str.toCharArray(buf, BUFFER_SIZE);
      if (temp_str.length() > 15) { //If greater than 15 characters (filter out garbage serial further)
        digitalWrite(LED_BUILTIN, HIGH);
        breakLoop = true;
        break;
      }
    }
  }
  
  textX         = matrix.width();
  textMin       = (int16_t)sizeof(buf) * -12;
  hue           = 0;
  matrix.begin();
  matrix.setTextWrap(false); // Allow text to run off right edge
  matrix.setTextSize(2);
}

void loop() {
  //char str1[] = "51.76F|Rain|72:5m|17:18m|C.Katsu|N:99%|S:38%|SW:45%";

  byte i;

  //const char str[] PROGMEM = "51.76F|Rain|72:5m|17:18m|C.Katsu|N:99%|S:38%|SW:45%";
  //int16_t    textX         = matrix.width(),
  //        textMin       = (int16_t)sizeof(str) * -12,
  //        hue           = 0;

  // Clear background
  matrix.fillScreen(0);

  // Bounce three balls around
  /*
  for(i=0; i<3; i++) {
    // Draw 'ball'
    matrix.fillCircle(ball[i][0], ball[i][1], 5, pgm_read_word(&ballcolor[i]));
    // Update X, Y position
    ball[i][0] += ball[i][2];
    ball[i][1] += ball[i][3];
    // Bounce off edges
    if((ball[i][0] == 0) || (ball[i][0] == (matrix.width() - 1)))
      ball[i][2] *= -1;
    if((ball[i][1] == 0) || (ball[i][1] == (matrix.height() - 1)))
      ball[i][3] *= -1;
  }
  */
  
  // Draw big scrolly text on top
  matrix.setTextColor(matrix.ColorHSV(hue, 255, 255, true));
  matrix.setCursor(textX, 1);
  //matrix.print(F2(str));
  matrix.print(buf);

  // Move text left (w/wrap), increase hue
  if((--textX) < textMin) textX = matrix.width();
  hue += 7;
  if(hue >= 1536) hue -= 1536;

#if !defined(__AVR__)
  // On non-AVR boards, delay slightly so screen updates aren't too quick.
  delay(20);
#endif

  delay(40);

  // Update display
  matrix.swapBuffers(false);
}
