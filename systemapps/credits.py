from badge import oled,btn
from time import sleep_ms

def app_start():
	banner = "Government\tTechnology\tAgency\tSingapore\nCyber\tSecurity\tGroup\t(CSG)\n Edmund Ang \tEditor\nC01N\t(C) 2023\nThank You\tFor Playing"
	for text in banner.split('\n'):
		lines = text.split('\t')
		lineh = 10
		blockh = lineh*len(lines)
		midy = int((64 - blockh) / 2)
		stopped = False
		for y in range(64,-blockh,-3):
			if y < midy and not stopped:
				stopped = True
				sleep_ms(3000)
			oled.fill(0)
			for dy,line in enumerate(lines): oled.hctext(line,y+dy*lineh,1)
			oled.show()
	return 0
