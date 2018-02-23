int x, y;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  x = 0;
  y = 0;
  randomSeed(analogRead(0));
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(x);
  Serial.print(" ");
  Serial.print(y);
  Serial.print("\n");
  int ra = random(1, 41);
  if(x<5) {
    x = x + 1;
  }
  if(y<8) {
    y = y + 2;
  }

  if(ra <= 20) {
    Serial.print(x+1);
    Serial.print(" ");
    Serial.print(y-1);
    Serial.print(" ");
    Serial.print("Person");
    Serial.print("\n");
  }
  
  _delay_ms(500);
}
