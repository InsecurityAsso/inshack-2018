#include<stdio.h>
#include<string.h>
#include <unistd.h>
#include<stdlib.h>

char encryptkey[17];
char * masterkey;

void xread(char * buffer, int length)
{
    read(0, buffer, length);
    int i;
    for(i=0; buffer[i]!=0 && buffer[i]!=10; i++);
    buffer[i]=0;
    return;
}

char scti(char c)
{
    switch(c)
    {
        case '7': return 5;
        case 'd': return 7;
        case '2': return 6;
        case '3': return 2;
        case '4': return 1;
        case '8': return 3;
        case 'f': return 8;
        case '6': return 10;
        case 'b': return 12;
        case 'c': return 15;
        case 'a': return 0;
        case '1': return 9;
        case '5': return 4;
        case '0': return 14;
        case 'e': return 11;
        case '9': return 13;
        default: return 16;
    }
}

char itcs(char i)
{
    switch(i)
    {
        case 5: return '7';
        case 7: return 'd';
        case 6: return '2';
        case 2: return '3';
        case 1: return '4';
        case 3: return '8';
        case 8: return 'f';
        case 10: return '6';
        case 12: return 'b';
        case 15: return 'c';
        case 0: return 'a';
        case 9: return '1';
        case 4: return '5';
        case 14: return '0';
        case 11: return 'e';
        case 13: return '9';
        default: return 'x';
    }
}

char oath(char * name)
{
    printf("Now raise your right hand and repeat after me :\n");
    char oathstr[512];
    strcpy(oathstr, "I, ");
    strcat(oathstr, name);
    strcat(oathstr, ", do solemnly swear");
    printf("%s\n", oathstr);
    char input[512];
    xread(input, 511);
    //printf("Debug : |%s|%s|\n",oathstr,input);
    if(!strcmp(input, "yeah sure whatever"))
    {
        return 0;
    }
    if(strcmp(input, oathstr))
    {
        return 1;
    }
    
    strcpy(oathstr, "That I will faithfully execute");
    printf("%s\n", oathstr);
    xread(input, 511);
    if(strcmp(input, oathstr))
    {
        return 1;
    }

    strcpy(oathstr, "The Office of President of the United States");
    printf("%s\n", oathstr);
    xread(input, 511);
    if(strcmp(input, oathstr))
    {
        return 1;
    }
    
    strcpy(oathstr, "And will to the best of my Ability");
    printf("%s\n", oathstr);
    xread(input, 511);
    if(strcmp(input, oathstr))
    {
        return 1;
    }

    strcpy(oathstr, "Preserve, protect and defend");
    printf("%s\n", oathstr);
    xread(input, 511);
    if(strcmp(input, oathstr))
    {
        return 1;
    }

    strcpy(oathstr, "The constitution of the United States");
    printf("%s\n", oathstr);
    xread(input, 511);
    if(strcmp(input, oathstr))
    {
        return 1;
    }
    return 0;
}

char checkExistingPresidents(char * name)
{
    //return 0; //Override president check
    char * presidents [] = {"George Washington", "John Adams", "Thomas Jefferson", "James Madison", "James Monroe", "John Quincy Adams", "Andrew Jackson", "Martin Van Buren", "William H. Harrison", "John Tyler", "James K. Polk", "Zachary Taylor", "Millard Fillmore", "Franklin Pierce", "James Buchanan", "Abraham Lincoln", "Andrew Johnson", "Ulysses S. Grant", "Rutherford B. Hayes", "James A. Garfield", "Chester A. Arthur", "Grover Cleveland", "Benjamin Harrison", "Grover Cleveland", "William McKinley", "Theodore Roosevelt", "William H. Taft", "Woodrow Wilson", "Warren G. Harding", "Calvin Coolidge", "Herbert Hoover", "Franklin D. Roosevelt", "Harry S. Truman", "Dwight D. Eisenhower", "John F. Kennedy", "Lyndon B. Johnson", "Richard M. Nixon", "Gerald R. Ford", "Jimmy Carter", "Ronald Reagan", "George H. W. Bush", "Bill Clinton", "George W. Bush", "Barack Hussein Obama", "Donald J. Trump"};
    int len = sizeof(presidents)/sizeof(presidents[0]);
    int i;
    for(i=0; i<len; i++)
    {
        if(!strcmp(name, presidents[i]))
        {
            return 1;
        }
    }
    return 0;
}

void pkcs7pad(char * data)
{
    int datalen = strlen(data);
    char pad = (65536-datalen)%16;
    int i;
    for(i=0; i<pad; i++)
    {
        data[datalen+i]=pad;
    }
    data[datalen+i]=0;
}

char xbox[16][8] = {
{240, 197, 57, 95, 181, 41, 222, 154},
{74, 47, 111, 215, 184, 234, 191, 137},
{75, 14, 158, 218, 195, 186, 119, 146},
{93, 213, 180, 243, 141, 166, 215, 70},
{19, 178, 92, 197, 16, 131, 233, 104},
{112, 221, 47, 138, 250, 236, 52, 208},
{7, 25, 182, 10, 119, 198, 213, 164},
{70, 174, 134, 229, 218, 240, 30, 59},
{208, 47, 206, 255, 27, 155, 121, 8},
{97, 82, 18, 39, 186, 102, 104, 55},
{231, 115, 66, 54, 248, 10, 47, 26},
{2, 181, 4, 41, 225, 146, 5, 154},
{172, 107, 247, 229, 47, 114, 117, 64},
{90, 199, 32, 87, 175, 42, 220, 186},
{17, 152, 191, 25, 23, 45, 3, 232},
{244, 10, 173, 31, 115, 66, 170, 148}
};

char xbox2[256] = {95, 253, 211, 232, 172, 222, 198, 42, 85, 105, 93, 252, 139, 142, 214, 89, 173, 137, 110, 151, 246, 194, 8, 18, 207, 103, 167, 161, 1, 220, 67, 210, 249, 44, 255, 126, 197, 91, 2, 66, 82, 159, 88, 7, 187, 108, 33, 128, 122, 123, 34, 149, 236, 170, 226, 164, 71, 206, 191, 188, 120, 157, 205, 254, 233, 228, 190, 115, 20, 118, 6, 61, 186, 215, 248, 60, 114, 216, 13, 58, 86, 102, 174, 176, 64, 113, 112, 219, 63, 96, 111, 171, 79, 54, 250, 189, 203, 200, 180, 184, 25, 104, 227, 132, 72, 158, 152, 154, 39, 117, 179, 155, 235, 106, 9, 230, 65, 92, 27, 68, 119, 182, 195, 224, 37, 38, 134, 223, 116, 145, 178, 185, 31, 83, 163, 76, 150, 231, 90, 234, 125, 141, 77, 238, 81, 87, 56, 19, 181, 30, 201, 213, 48, 55, 22, 36, 243, 146, 101, 127, 16, 218, 138, 109, 50, 183, 131, 80, 239, 49, 23, 3, 4, 62, 196, 204, 97, 14, 12, 135, 11, 144, 51, 45, 241, 99, 121, 168, 70, 148, 208, 221, 225, 73, 217, 26, 162, 212, 52, 140, 43, 5, 10, 107, 153, 78, 32, 74, 160, 35, 40, 94, 136, 175, 53, 124, 199, 242, 240, 166, 129, 75, 0, 41, 247, 130, 15, 21, 229, 98, 29, 47, 133, 17, 46, 24, 57, 202, 169, 192, 251, 193, 59, 100, 147, 156, 177, 209, 84, 143, 28, 237, 69, 244, 165, 245};

char pbox[16][8] = {
{7, 4, 3, 0, 5, 2, 6, 1},
{2, 3, 4, 1, 0, 7, 5, 6},
{7, 4, 6, 2, 5, 3, 0, 1},
{4, 1, 6, 5, 0, 7, 3, 2},
{2, 1, 6, 5, 4, 0, 7, 3},
{4, 3, 6, 5, 0, 7, 1, 2},
{0, 6, 2, 7, 1, 4, 3, 5},
{4, 1, 7, 2, 6, 5, 0, 3},
{6, 0, 4, 2, 3, 1, 7, 5},
{0, 6, 2, 1, 7, 4, 3, 5},
{5, 2, 1, 6, 3, 7, 0, 4},
{7, 1, 6, 0, 4, 5, 3, 2},
{7, 2, 0, 4, 3, 6, 1, 5},
{5, 1, 0, 3, 4, 6, 2, 7},
{4, 2, 6, 1, 3, 5, 7, 0},
{0, 1, 5, 2, 7, 3, 6, 4}
};

void printlr(char * l, char * r)
{
    printf("Left  :");
    int i;
    for(i=0; i<8; i++)
    {
        printf(" %02x",(unsigned char)l[i]);
    }
    printf("\nRight :");
    for(i=0; i<8; i++)
    {
        printf(" %02x",(unsigned char)r[i]);
    }
    printf("\n");
}

void encrypt(char * data)
{
    char * left = malloc(8);
    char * right = malloc(8);
    int i;
    for(i=0; i<8; i++)
    {
        left[i]=data[i];
        right[i]=data[i+8];
    }
    
    int round;
    for(round=0; round<16; round++)
    {
        //printlr(left,right);
        char xindex = (encryptkey[round] >> 4)&0xf;
        char pindex = encryptkey[round] & 0xf;
        //printf("Running round %d with xkey %d and pkey %d\n",round,xindex,pindex);
        char f;
        for(i=0; i<8; i++)
        {
            f=right[pbox[pindex][i]]^xbox2[right[(i-1)%8]];
            f^=xbox[xindex][i];
            left[i]^=f;
        }
        char * tmp = right;
        right=left;
        left=tmp;
    }
    for(i=0; i<8; i++)
    {
        data[i]=left[i];
        data[i+8]=right[i];
    }
    //printlr(left,right);
}

void decrypt(char * data)
{
    char * left = malloc(8);
    char * right = malloc(8);
    int i;
    for(i=0; i<8; i++)
    {
        left[i]=data[i+8];
        right[i]=data[i];
    }
    
    int round;
    for(round=15; round>=0; round--)
    {
        //printlr(left,right);
        char xindex = (encryptkey[round] >> 4)&0xf;
        char pindex = encryptkey[round] & 0xf;
        char f;
        //printf("Running round %d with xkey %d and pkey %d\n",round,xindex,pindex);
        for(i=0; i<8; i++)
        {
            f=right[pbox[pindex][i]]^xbox2[right[(i-1)%8]];
            f^=xbox[xindex][i];
            left[i]^=f;
        }
        char * tmp = right;
        right=left;
        left=tmp;
    }
    for(i=0; i<8; i++)
    {
        data[i+8]=left[i];
        data[i]=right[i];
    }
    //printlr(left,right);
}

char * generateNuclearCode(char * president)
{
    unsigned long long state = 12128142353075455455ULL;
    unsigned long long poly = 11791203767310758923ULL;
    int i=0;
    while(president[i])
    {
        int j;
        for(j=0;j<8;j++)
        {
            char bit = (president[i]>>j)&1;
            if(bit^((state>>31)&1))
            {
                state = (state<<1)^poly;
            }
            else
            {
                state = state<<1;
            }
        }
        i++;
    }
    char * result = malloc(25);
    sprintf(result,"INSA{%llx}",state);
    return result;
}

char * generateToken(char * username)
{
    char * toEncrypt = malloc(256+32);
    toEncrypt[0]=1;
    strcpy(toEncrypt+1, username);
    pkcs7pad(toEncrypt);
    
    int datalen = strlen(toEncrypt);
    toEncrypt[0]=datalen/16;
    int block;
    for(block=0; block<datalen; block+=16)
    {
        if(block)
        {
            int i;
            for(i=0; i<16; i++)
            {
                toEncrypt[block+i]^=toEncrypt[block+i-16];
            }
        }
        encrypt(toEncrypt+block);
    }
    //printf("Debug : encrypted raw is %s\n",toEncrypt); 
    char * hextoken = malloc(datalen*2+1);
    int i;
    for(i=0;i<datalen;i++)
    {
        hextoken[2*i]=itcs(toEncrypt[i]&0xf);
        hextoken[2*i+1]=itcs((toEncrypt[i]>>4)&0xf);
        //printf("DEBUG : %c|(%d %c)|(%d %c)",toEncrypt[i], toEncrypt[i]&0xf,itcs(toEncrypt[i]&0xf),toEncrypt[i]>>4,itcs(toEncrypt[i]>>4));
    }
    return hextoken;
}

void registerPresident()
{
    printf("Please enter your name : ");
    fflush(stdout);
    char president[256];
    xread(president, 255);

    if(!strcmp(president,"administrator"))
    {
        printf("Error : Cannot register as administrator.\n");
        return;
    }

    char res;
    res = checkExistingPresidents(president);
    if(res)
    {
        printf("Error : President %s is already registered.\n", president);
        return;
    }
    
    res = oath(president);
    if(!res)
    {
        printf("Welcome aboard, President %s !\n", president);
        printf("Your nuclear codes are %s\n",generateNuclearCode(president));
        printf("In case you ever forget your nuclear codes, here is your token to generate them again :\n");
        printf("%s\n\n", generateToken(president));
    }
    else
    {
        printf("Please try that again.\n");
        return;
    }
}

void forgotCodes()
{
    printf("Please enter your token : ");
    fflush(stdout);
    char token[600];
    char data[512] = {0};
    xread(token,512);
    int tokenlen = strlen(token);
    if(tokenlen%32)
    {
        printf("Invalid token length.\n");
        return;
    }
    int i;
    for(i=0; i<tokenlen; i++)
    {
        char val = scti(token[i]);
        if(val==16)
        {
            printf("Invalid hex value %c\n", token[i]);
            return;
        }
        if(i%2)
        {
            data[i/2]+=val*16;
        }
        else
        {
            data[i/2]+=val;
        }
    }
    //printf("Debug : Data loaded %s\n",data);
    int datalen = strlen(data);
    char orig[512];
    strcpy(orig, data);
    int block;
    for(block=0; block<datalen; block+=16)
    {
        //printf("Decrypting block %d\n",block);
        decrypt(data+block);
        if(block)
        {
            //printf("done. Now CBC\n");
            for(i=0;i<16;i++)
            {
                data[block+i]^=orig[block+i-16];
            }
        }
    }
    //printf("%s\n", data);
    if(data[0]!=datalen/16) //Number of blocks was altered
    {
        printf("Invalid token. Data0 is %d and datalen is %d\n",data[0],datalen);
        return;
    }
    char pad = data[datalen-1];
    for(i=0;i<pad;i++)
    {
        if(data[datalen-1-i]!=pad)
        {
            printf("Invalid token. Pad is %d, invalid encountered at idx %d\n", pad, i);
            return;
        }
    }
    
    data[datalen-pad]=0;

    char president[256];
    strcpy(president,data+1);
    if(!strcmp(president,"administrator"))
    {
        printf("Welcome administrator ! The override key is %s\n", masterkey);
    }
    else
    {
        printf("Nuclear codes for president %s are %s\n", president, generateNuclearCode(president));
    }
}

void main(int argc, char ** argv)
{
    if(argc != 3)
    {
        printf("Usage : %s [master nuclear code] [encryption key, 16 hex bytes]\n", *argv);
        return;
    }

    if(strlen(argv[2])!=32)
    {
        printf("Bad key length (need 32 hex chars, got %d\n", (int)strlen(argv[2]));
        return;
    }

    int i;
    for(i=0; i<16; i++)
    {
        encryptkey[i]=0;
    }

    for(i=0; i<32; i++)
    {
        char val = scti(argv[2][i]);
        if(val==16)
        {
            printf("Invalid hex value %c\n", argv[2][i]);
            return;
        }
        if(i%2)
        {
            encryptkey[i/2]+=val*16;
        }
        else
        {
            encryptkey[i/2]+=val;
        }
    }
    masterkey = argv[1];

    printf("                    _ _.-'`-._ _\n");
    printf("                   ;.'________'.;\n");
    printf("        _________n.[____________].n_________\n");
    printf("       |''_''_''_''||==||==||==||''_''_''_''|\n");
    printf("       |'''''''''''||..||..||..||'''''''''''|\n");
    printf("       |LI LI LI LI||LI||LI||LI||LI LI LI LI|\n");
    printf("       |.. .. .. ..||..||..||..||.. .. .. ..|\n");
    printf("       |LI LI LI LI||LI||LI||LI||LI LI LI LI|\n");
    printf("    ,,;;,;;;,;;;,;;;,;;;,;;;,;;;,;;,;;;,;;;,;;,,\n");
    printf("   ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;\n\n");

    printf("        WHITE HOUSE AUTHENTICATION SERVICE\n\n");

    while(1)
    {
        printf("What do you want to do ?\n");
        printf("1. Register a new president\n");
        printf("2. Generate nuclear bomb codes\n");
        printf("3. Exit\n");
        printf("Your choice : ");
        fflush(stdout);

        char choice[2];
        xread(choice, 1);
        char c;
        while((c = getchar()) != '\n' && c != EOF);
    
        if(choice[0] == '1')
        {
            registerPresident();
        }
        else if(choice[0] == '2')
        {
            forgotCodes();
        }
        else
        {
            return;
        }
    }
}
