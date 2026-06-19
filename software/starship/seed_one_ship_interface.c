// Seed One Ship Interface System - HCIos header file
#include <stdio.h>
#include <string.h>


#define PAUSE printf("\n\t\t\tpress <Enter> to Continue: ");
#define CONT while (getchar() != 10);
#define FF fflush(stdin);
#define NAME "SEED SHIP INTERFACE - Seed One - HCIos Pirate Brothers Software"
#define ADDRESS "Ships Systems - Diagnostic and Productiond"
#define PLACE "Main Production Facilities - Harvesting | Repair | New Production"
#define LIMIT 180
#define SPACE ' '
#define TITLE "SeedOne HCIos Software model"
#define CURRENCY printf("\n Please enter the conversion amount:____\b\b\b\b");
#define DOLLARS scanf("%f", &dollars);
#define MENU_CHOICE system("./white");	printf("\t\t\tPlease make a selection: ");
#define	MENU_SELECT scanf("%c", &choice);

//***********************************************************************	End Definitions
//***********************************************************************	Begin Functions/Class

void boarder(void);
void menu(void);
void clear(void);
void quit(void);
void n_char(char ch, int num);

int spaces;
char choice;
float exchange, dollars;

int main(void)
{
	clear();
	boarder();
	menu();
		return 0;

}
void n_char(char ch, int num)
{
//										Counts out the spaces
	int count;
	for (count = 1; count <= num; count++)
	putchar(ch);
}

void quit(void)
{
//										On Exit!
	system("./red");
	printf("\n\n\n\n\n\n\n\n\n\n");
	printf("\t\t\t\t\t\tEL F!N!\n");
}

void clear(void)
{
//										To clear the screen
	 system("clear");
	//			clear();
}


void boarder(void)
{
//	
	system("./white");		//							Boarder
	n_char('*', LIMIT);
	putchar('\n');
//			
	system("./red");
	spaces = (LIMIT - strlen(NAME)) / 2;	//						Top Boarder
	n_char(SPACE, spaces);
	printf("%s\n", NAME);
	
	system("./green");
	spaces = (LIMIT - strlen(ADDRESS)) / 2;
	n_char(SPACE, spaces);
	printf("%s\n", ADDRESS);

	spaces = (LIMIT - strlen(PLACE)) / 2;
	n_char(SPACE, spaces);
	printf("%s\n", PLACE);
//										Bottom Boarder
	system("./white");
	n_char('*', LIMIT);
	putchar('\n');
}


void menu(void)
{
//										Menu Selection
	putchar('\n');
	system("./green");
	spaces = (LIMIT - strlen(TITLE)) / 2;
	n_char(SPACE, spaces);
	printf("%s\n", TITLE);
	
	system("./white");
	n_char('*', LIMIT);
	putchar('\n');

	system("./blue");
	system("./reverse");	printf("\t\t\t1)\tNavigation & Propulstion 	a)\tPitch & Yaw		j)\tSolar Dome Engage	s)\tArtificial Lights	\n");
	system("./cyan");	printf("\t\t\t2)\tPower Plants & Engineering 	b)\tEngines Status	\tk)\tHyperDrive Engine	t)\tMain Dome Control	\n");
	system("./red");	printf("\t\t\t3)\tSecurity | Brig | Weapons    	c)\tWeapons Lock	\tl)\tSecurity Camera	\tu)\tSecurity Logs	\n");
	system("./yellow"); 	printf("\t\t\t4)\tSafty Officer S1 Airlocks  	d)\tDamage Reports	m)\tEmergency Stop	\tv)\tDuty Roster		\n");
	system("./green"); 	printf("\t\t\t5)\tLife Support & Aquaponics   	e)\tBio Labs | Seeds	n)\tNursury		\tw)\tMedical Bay | Labs	\n");
	system("./blue");	printf("\t\t\t6)\tMining & Mineral Collection	f)\tInventory Stores	o)\tManufacturing	\tx)\tDesign & Testing	\n");
	system("./white");	printf("\t\t\t7)\tProdction | Design | Robotics	g)\tOperational Systems	p)\tSystems Design	\ty)\tRobot Report Logs	\n");
	system("./red");	printf("\t\t\t8)\tDocking Bays and Launching	h)\tEscape Pods		q)\tDocking Schedule	z)\tCrew Manifest	\n");
	system("./cyan");	printf("\t\t\t9)\tAstrometrics | Resources	i)\tWeapons Systems	\tr)\tWeapons Status	\n");
	system("./reverse");	printf("\t\t\tQ)\tQuit Program\n");
						MENU_CHOICE
						MENU_SELECT
	 	while(choice != 'Q' || choice != 'q');
	{
		clear();
		boarder();
				if(choice == '1' || choice == '2' || choice == '3')
				{
					CURRENCY;
					DOLLARS;
					FF;
				}
				switch (choice)
				{
					case '1' : system("./beacon.update");
						break;
					case '2' : system("./nog.update");
						break;
					case '3' : system("./bkon.e");
						break;
					case 'q' : quit();
					case 'Q' : quit();
								printf("\n\tThank You!");
								break;
				}
			clear();
			boarder();
			menu();
	}
}

