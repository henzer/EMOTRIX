String index, val, sample, bin1, bin2;
char chr1, chr2;
long val1, val2;
int suma;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    // Esperamos a que se conecte el puerto serial
  }

  randomSeed(analogRead(0));
}

String decimal_to_bynary(int value) {
  int   i = 15;
  String binaryStr = "";

  while (i >= 0) {
    if ((value >> i) & 1)
      binaryStr += "1";
    else
      binaryStr += "0";
    i -= 1;
  }
  
  return binaryStr;
}

int potencia(int a, int b) {
  if (b == 0)
    return 1;

  int result = a;
  for (int i=1; i<b; i++)
    result *= a;

  return result;
}

int bynary_to_decimal(String bynary) {
  int result = 0;
  int pot = bynary.length() - 1;
  for (int i = 0; i<bynary.length(); i++){
    if (bynary.substring(i, i+1) == "1")
      result += potencia(2, pot);
    pot -= 1;
  }

  return result;
}

void loop() {
  // An example of poor signal could be one that oscillates between 0 and 1500.
  // 1500 = 0101 1101 1100
  sample = "{";
  suma = 0;

  for (int i=1; i <5 ; i++) {
    // First byte must be 0000 0101, ie 5.
    val1 = 5;
    // Max value for second byte must be 1101 1100, ie 220.
    val2 = random(0, 221);

    chr1 = (char)val1;
    chr2 = (char)val2;

    bin1 = decimal_to_bynary(val1);
    bin1 = bin1.substring(8, 16);
    bin2 = decimal_to_bynary(val2);
    bin2 = bin2.substring(8, 16);

    val = bin1 + bin2;    
    suma += bynary_to_decimal(val);

    index = "s";
    index += i;

    val = "";
    val.concat(chr1);
    val.concat(chr2);

    sample += index + ":" + val + ",";
  }

  val = decimal_to_bynary(suma);
  bin1 = val.substring(0, 8);
  bin2 = val.substring(8, 16);

  val1 = bynary_to_decimal(bin1);
  val2 = bynary_to_decimal(bin2);
  chr1 = (char)val1;
  chr2 = (char)val2;

  val = "";
  val.concat(chr1);
  val.concat(chr2);

  sample += "cs:" + val + "}";

  Serial.println(sample);
}
