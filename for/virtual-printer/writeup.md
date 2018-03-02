# Writeup Virtual Printer

## Analysis

You can upload PNG files. You receive a A4 paper in return which could be a real page but this is a Virtual Printer.

You should try to submit a black PNG and zoom in on the page which is returned, you'll see dots.

These dots constitute a dot matrix here its 8 rows by 64 columns. 
8 should remind you of a byte. Yes that's it 64 bytes vertically coded.

The first dot matrix starts at 50 from the top and 50 from the left side. 
Dots are present every 20 pixels both in rows and columns.

Using GIMP you can extract the color of the dot: `rgb(255, 255, 204)`

There are two ways of interpreting columns of 8 bits: MSB at the top or MSB at the bottom. 
Test both. MSB at the top is the one which makes sense.

You've got the following data: `"ip:\xHH\xHH\xHH\xHH\nat:\xHH\xHH\xHH\xHH\xHH\xHH\xHH\nS/N:\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\xHH\n\xff\xff\xff\xff\xff\xff\xff\xff"`
In fact it's `ip:<your_ip>\nat:<day_month_year_hour_min_sec>\nS/N:<serial_number>\n\xff\xff\xff\xff\xff\xff\xff\xff`

So you extract `<serial_number>` and encode it using base64 encoding.

You send it back to the server and it's too late... Have fun automating the process.

## Exploitation

See exploit/exploit for complete automation of the previous process.

