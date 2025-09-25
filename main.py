import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , xKEys , base64 , datetime , re , socket , threading
from protobuf_decoder.protobuf_decoder import Parser
from black9 import *
from black9 import xSendTeamMsg
from black9 import Auth_Chat
from xHeaders import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

def AuTo_ResTartinG():
    time.sleep(6 * 60 * 60)
    print('\n - AuTo ResTartinG The BoT ... ! ')
    p = psutil.Process(os.getpid())
    for handler in p.open_files():
        try:
            os.close(handler.fd)
        except Exception as e:
            print(f" - Error CLose Files : {e}")
    for conn in p.net_connections():
        try:
            if hasattr(conn, 'fd'):
                os.close(conn.fd)
        except Exception as e:
            print(f" - Error CLose Connection : {e}")
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    python = sys.executable
    os.execl(python, python, *sys.argv)
       
def ResTarT_BoT():
    print('\n - ResTartinG The BoT ... ! ')
    p = psutil.Process(os.getpid())
    open_files = p.open_files()
    connections = p.net_connections()
    for handler in open_files:
        try:
            os.close(handler.fd)
        except Exception:
            pass           
    for conn in connections:
        try:
            conn.close()
        except Exception:
            pass
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])))
    python = sys.executable
    os.execl(python, python, *sys.argv)

def GeT_Time(timestamp):
    last_login = datetime.fromtimestamp(timestamp)
    now = datetime.now()
    diff = now - last_login   
    d = diff.days
    h , rem = divmod(diff.seconds, 3600)
    m , s = divmod(rem, 60)    
    return d, h, m, s

def Time_En_Ar(t): 
    return ' '.join(t.replace("Day","يوم").replace("Hour","ساعة").replace("Min","دقيقة").replace("Sec","ثانية").split(" - "))
    
Thread(target = AuTo_ResTartinG , daemon = True).start()
            
class FF_CLient():

    def __init__(self, id, password):
        self.id = id
        self.password = password
        self.Get_FiNal_ToKen_0115()     
            
    def Connect_SerVer_OnLine(self , Token , tok , host , port , key , iv , host2 , port2):
            global CliEnts2 , DaTa2 , AutH
            try:
                self.AutH_ToKen_0115 = tok    
                self.CliEnts2 = socket.create_connection((host2 , int(port2)))
                self.CliEnts2.send(bytes.fromhex(self.AutH_ToKen_0115))                  
            except:pass        
            while True:
                try:
                    self.DaTa2 = self.CliEnts2.recv(99999)
                    if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:	         	    	    
                            self.packet = json.loads(DeCode_PackEt(f'08{self.DaTa2.hex().split("08", 1)[1]}'))
                            self.AutH = self.packet['5']['data']['7']['data']
                    
                except:pass    	
                                                            
    def Connect_SerVer(self , Token , tok , host , port , key , iv , host2 , port2):
            global CliEnts       
            self.AutH_ToKen_0115 = tok    
            self.CliEnts = socket.create_connection((host , int(port)))
            self.CliEnts.send(bytes.fromhex(self.AutH_ToKen_0115))  
            self.DaTa = self.CliEnts.recv(1024)          	        
            threading.Thread(target=self.Connect_SerVer_OnLine, args=(Token , tok , host , port , key , iv , host2 , port2)).start()
            self.Exemple = xMsGFixinG('12345678')
            while True:      
                try:
                    self.DaTa = self.CliEnts.recv(1024)   
                    if len(self.DaTa) == 0 or len(self.DaTa2) == 0:	            		
                        try:            		    
                            self.CliEnts.close() ; self.CliEnts2.close() ; self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)                    		                    
                        except:
                            try:
                                self.CliEnts.close() ; self.CliEnts2.close() ; self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                            except:
                                self.CliEnts.close() ; self.CliEnts2.close() ; ResTarT_BoT()	            
                                      
                    if '1200' in self.DaTa.hex()[0:4] and 900 > len(self.DaTa.hex()) > 100:
                        if b"***" in self.DaTa:self.DaTa = self.DaTa.replace(b"***",b"106")         
                        try:
                           self.BesTo_data = json.loads(DeCode_PackEt(self.DaTa.hex()[10:]))	       
                           self.input_msg = 'besto_love' if '8' in self.BesTo_data["5"]["data"] else self.BesTo_data["5"]["data"]["4"]["data"]
                        except: self.input_msg = None	   	 
                        self.DeCode_CliEnt_Uid = self.BesTo_data["5"]["data"]["1"]["data"]
                        self.CliEnt_Uid = EnC_Uid(self.DeCode_CliEnt_Uid , Tp = 'Uid')
                               
                    if 'besto_love' in self.input_msg[:10]:
                        self.CliEnts.send(xSEndMsg(f'''[C][B][00f7f9]━━━━━━━━━━━━
[C][B][FFFFFF]instagram :
[C][B][0012ff]z9o_v
[c][b][0012ff]silver
[C][B][00f7f9]━━━━━━━━━━━━
[C][B][FFFFFF]لعرض الاوامر اكتب
[b][c][{ArA_CoLor()}]/[C][B]help''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(0.3)
                        self.CliEnts.close() ; self.CliEnts2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	                    	 	 
                                                               
                    if b'/start' in self.DaTa or b'/help' in self.DaTa or 'en' in self.input_msg[:2]:
                        self.result = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        if self.result:
                            self.Status , self.Expire = self.result
                            self.CliEnts.send(xSEndMsg(f'''[b][c][{ArA_CoLor()}]
فتح سكود لصديقك عبر ايدي :
[C][B][ffffff]/[C][B]3/[ id ]
/[C][B]5/[ id ]
/[C][B]6/[ id ][b][c][{ArA_CoLor()}]
تحويل الفريق إلى:
[C][B][ffffff]/[C][B]3  /[C][B]5  /[C][B]6  [b][c][{ArA_CoLor()}]
جلب لاعب إلى الفريق:
[C][B][ffffff]/[C][B]inv [ id ][b][c][{ArA_CoLor()}]
سبام طلبات انضمام:
[C][B][ffffff]/[C][B]x [ id ][b][c][{ArA_CoLor()}]
سبام رومات:
[C][B][ffffff]/[C][B]room [ id ][b][c][{ArA_CoLor()}]
معرفة حالة اللاعب:
[C][B][ffffff]/[C][B]status [ id ][b][c][{ArA_CoLor()}]
معرفة إذا كان اللاعب مبند:
[C][B][ffffff]/[C][B]check [ id ]
[b][c][{ArA_CoLor()}]
سبام طلبات صداقة:
[C][B][ffffff]/[C][B]spam [ id ][b][c][{ArA_CoLor()}]
زيادة عدد زوار الحساب:
[C][B][ffffff]/[C][B]visit  [ id ][b][c][{ArA_CoLor()}]
تزويد 100 لايك للحساب 
[C][B][ffffff]/[C][B]like  [ id ]
''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''[b][c][{ArA_CoLor()}]
مقبرة السكود  :
[C][B][ffffff]/[C][B]code [ Team Code  ]
سبام رسائل في الفريق
[C][B][ffffff]/msg/[team code] رسالة
[b][c][{ArA_CoLor()}]دخول شبح للسكواد
[C][B][ffffff]/cod[team code]
    \n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)		
                            self.CliEnts.send(xSEndMsg(f'''
    [b][c][FFD700]━━━━━━━━━━━━[ffffff]
    [b][c][{ArA_CoLor()}]id => [ffffff]{xMsGFixinG(self.DeCode_CliEnt_Uid)} 
    [b][c][{ArA_CoLor()}]  Status => [ffffff]{self.Status} 
    [b][c][{ArA_CoLor()}]  Expire In => [ffffff]{self.Expire}
    [b][c][{ArA_CoLor()}]  Version => v1
    [FFD700]━━━━━━━━━━━━[ffffff]\n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	   	       		
                        elif False == self.result:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)  
                            
                    elif '/who-is-the-best' in self.input_msg[:2]:
                        self.result = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        if self.result:
                            self.Status , self.Expire = self.result
                            self.CliEnts.send(xSEndMsg(f'''Black
    ''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''
Top''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)		
                            self.CliEnts.send(xSEndMsg(f'''1 in world''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	        
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''Black
    ''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''
Top''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)		
                            self.CliEnts.send(xSEndMsg(f'''1 in world''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	        
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''Black
    ''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''
Top''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)		
                            self.CliEnts.send(xSEndMsg(f'''1 in world''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	        
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''Black
    ''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)
                            self.CliEnts.send(xSEndMsg(f'''
Top''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.3)		
                            self.CliEnts.send(xSEndMsg(f'''1 in world''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	        
                            time.sleep(0.3)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	   	       		
                        elif False == self.result:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                     
                    elif '/code' in self.input_msg[:5]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        self.id , self.nm = (self.input_msg[6:].split(" ", 1) if " " in self.input_msg[6:] else [self.input_msg[6:], "Black</>CodeX"])  
                        self.Zx = ChEck_Commande(self.id)
                       
                        if self.ChEck_ReGister and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] JoinInG With Code {self.id}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            self.CliEnts2.send(GenJoinSquadsPacket(self.id, key, iv))
                            time.sleep(0.3)

                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                                sq = self.dT["5"]["data"]["31"]["data"]
                                idT = self.dT["5"]["data"]["1"]["data"]
                                print(idT)	            	            	            	            	            	            
                                self.CliEnts2.send(ExiT('000000' , key , iv))	            	            
                                self.CliEnts2.send(ghost_pakcet(idT, self.nm , sq , key , iv))  
                                for i in range(11111):
                                   self.CliEnts2.send(GenJoinSquadsPacket(self.id, key, iv))
                                   self.CliEnts2.send(ghost_pakcet(idT, self.nm , sq , key , iv))
                                   time.sleep(0.0001)
                                   self.CliEnts2.send(ExiT('000000' , key , iv))
                                   self.CliEnts2.send(ghost_pakcet(idT, self.nm , sq , key , iv))

                           

                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /cood <code>\n - Ex : /cood 517284\n', 9 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                    elif '/msg/' in self.input_msg[:5]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        self.id , self.nm = (self.input_msg[5:].split(" ", 1) if " " in self.input_msg[5:] else [self.input_msg[5:], ""])
                        self.Zx = ChEck_Commande(self.id)
                        if self.ChEck_ReGister and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Wait for sending message    : {self.id}\n', 9 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            
                            g = GenJoinSquadsPacket(self.id, key, iv)
                            self.CliEnts2.send(g)
                            print(g)
                            time.sleep(0.5)

                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                
                                self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                                
                                idT = self.dT["5"]["data"]["1"]["data"]
                                sq = self.dT["5"]["data"]["14"]["data"]
                                
                                 
                                self.CliEnts.send(Auth_Chat(idT, sq, key, iv))
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] succesfull snd message : {self.id}\n', 9 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                
                                self.CliEnts.send(xSendTeamMsg(f'\n[b][c][{ArA_CoLor()}] {self.nm}\n',idT , key , iv))
                                self.CliEnts2.send(ExiT('000000' , key , iv))
                                time.sleep(4)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)  
                                
                                
                                            	            	            
                                
                            

                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /cood <code>\n - Ex : /cood 517284\n', 9 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)

                    elif '/ban/' in self.input_msg[:5]:
                        self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                        self.id = self.input_msg[5:].split(" ", 1)[0]
                        self.Zx = ChEck_Commande(self.id)
                        if self.ChEck_ReGister and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'[b][c][{ArA_CoLor()}]تم تشجيل دخول by silver', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            
                            g = GenJoinSquadsPacket(self.id, key, iv)
                            self.CliEnts2.send(g)
                            print(g)
                            time.sleep(0.5)

                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                
                                self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                                
                                idT = self.dT["5"]["data"]["1"]["data"]
                                sq = self.dT["5"]["data"]["14"]["data"]
                                
                                 
                                self.CliEnts.send(Auth_Chat(idT, sq, key, iv))
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] BAN msg SS : {self.id}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                for i in range(10):
                                    self.CliEnts.send(xSendTeamMsg(f'[b][c][{ArA_CoLor()}]تم تشجيل دخول by Black',idT , key , iv))
                                    self.CliEnts2.send(ExiT('000000' , key , iv))
                                time.sleep(4)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)  
                                
                                
                                            	            	            
                                
                            

                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /cood <code>\n - Ex : /cood 517284\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        elif False == self.ChEck_ReGister:
                            DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                    elif '/like' in self.input_msg[:5]: 	
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)	            		    
                            self.res , self.time = ChEck_Limit(self.DeCode_CliEnt_Uid , 'like')
                            self.id = self.input_msg[6:]
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and self.res and True == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SendinG LiKes To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))   
                                a1 , a2 , a3 , a4 , a5 = Likes(self.id)   
                                if a3 == a4:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][ffffff] Please Try Likes After 24H.. !\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    time.sleep(0.3)
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)                	
                                else:
                                    self.CliEnts.send(xSEndMsg(f'''[b][c][90EE90]\n [SuccEssFuLLy] - UpGradE LiKes !
        [ffffff]	
          PLayer Name : {a1}
          PLayer Uid : {xMsGFixinG(self.id)}
          PLayer SerVer : {a2}
          LiKes BeFore : {xMsGFixinG(a3)}
          LiKes AFter : {xMsGFixinG(a4)}
          LiKes GiVen : {a5}
          RemaininG : {self.res}
         
           [90EE90]Dev : LWESS_ANTIBAN\n''', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    time.sleep(0.3)
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	 
                                      
                            elif False == self.res and True == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][ffffff] U Reched Max Limit To SEnd LiKes\n Try AfTer : {xMsGFixinG(self.time)} !\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))  
                                      
                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /like <id>\n - Ex : /like {self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	      
                                                     
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                                                       
                    elif '/spam' in self.input_msg[:5]: 	
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[6:]
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and True == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SendinG Spam To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))   
                                self.Req = Requests_SPam(self.id)	     
                                if True == self.Req:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]SuccEssFuLLy SendinG SPam\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    time.sleep(0.3)
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	
                                             
                                elif False == self.Req:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][FFD700]FaiLEd SendinG SPam\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    
                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /spam <id>\n - Ex : /spam {self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                    
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)      
                                                               
                    elif '++' in self.input_msg[:2]:   
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[3:]
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and True == self.Zx:			    
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] GeTinG InFo FoR {xMsGFixinG(self.id)}\n' , 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.3)
                                self.CliEnts.send(xSEndMsg(GeT_PLayer_InFo(self.id , Token) , 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                
                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use ++ <id>\n - Ex : ++ {self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                                    
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)          	               	    	
                    elif '/5' in self.input_msg[:2]:    
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            if self.ChEck_ReGister:         	  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] GeneRaTinG 5 In Squid\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(5 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(3)		      
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)	
                                                                    
                    elif '/6' in self.input_msg[:2]:
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            if self.ChEck_ReGister:         	  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] GeneRaTinG 6 In Squid\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(6 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)

                    elif '/3' in self.input_msg[:2]:
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            if self.ChEck_ReGister:         	  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] GeneRaTinG 3 In Squid\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(3 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                                    
                    elif '/5/' in self.input_msg[:4]:
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[4:]
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and True == self.Zx:         	  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] 5 In Squid To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(5 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.id , key , iv))
                                time.sleep(3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)

                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /c5/<id>\n - Ex : /c5/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                                
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)  
                                                    
                    elif '/6/' in self.input_msg[:4]:
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[4:]	    	    
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and True == self.Zx:  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] 6 In Squid To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(6 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.id , key , iv))
                                time.sleep(3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)

                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /c6/<id>\n - Ex : /c6/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                                
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                                
                    elif '/3/' in self.input_msg[:4]:
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[4:]	    	    
                            self.Zx = ChEck_Commande(self.id)
                            if self.ChEck_ReGister and True == self.Zx:  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] 3 In Squid To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(3 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.id , key , iv))
                                time.sleep(3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)

                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /c3/<id>\n - Ex : /c3/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                                
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)
                                                            
                    elif '/inv' in self.input_msg[:5]:
                            self.ChEck_ReGister = ChEck_The_Uid(self.DeCode_CliEnt_Uid)
                            self.id = self.input_msg[5:]
                            self.Zx = ChEck_Commande(self.id)    
                            if self.ChEck_ReGister and True == self.Zx:  
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] GeTinG PLayer {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                self.CliEnts2.send(OpEnSq(key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(cHSq(5 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(0.5)			         
                                self.CliEnts2.send(SEnd_InV(1 , self.id , key , iv))
                                time.sleep(0.5)
                                self.CliEnts2.send(SEnd_InV(1 , self.DeCode_CliEnt_Uid , key , iv))
                                time.sleep(3)
                                self.CliEnts.close() ; self.CliEnts2.close()
                                self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2) 

                            elif False == self.Zx:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /inv<id>\n - Ex : /inv{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                                     
                            elif False == self.ChEck_ReGister:
                                DeLet_Uid(self.DeCode_CliEnt_Uid , Token)    		             

                    if '/pp/' in self.input_msg[:4]:
                        self.id = self.input_msg[4:]	 
                        self.Zx = ChEck_Commande(self.id)
                        if True == self.Zx:	            		     
                            for i in range(20):
                                threading.Thread(target=lambda: self.CliEnts2.send(SPamSq(self.id , key , iv))).start()
                            time.sleep(0.1)    			         
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SuccEss Spam To {xMsGFixinG(self.id)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	            		      	
                        elif False == self.Zx: 
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /pp/<id>\n - Ex : /pp/{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	            		

                    elif '/room' in self.input_msg[:4]:
                        self.res , self.time = ChEck_Limit(self.DeCode_CliEnt_Uid , 'Spam_Room')
                        self.id , self.nm = (self.input_msg[4:].split(" ", 1) if " " in self.input_msg[4:] else [self.input_msg[4:], "Black"])
                        self.Zx = ChEck_Commande(self.id)	
                        if self.res and True == self.Zx:
                            try:	      		    
                                self.CliEnts2.send(GeT_Status(self.id , key , iv))
                                time.sleep(0.3)
                            except:pass    	            	
                            if '0f00' in self.DaTa2.hex()[:4]:
                                try:	            		
                                    packet = self.DaTa2.hex()[10:]
                                    self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                    self.room_uid = self.BesTo_data['5']['data']['1']['data']['15']['data']
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] SuccEss SpamRoom To {xMsGFixinG(self.room_uid)}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    for i in range(999):
                                        threading.Thread(target=lambda: self.CliEnts2.send(SPam_Room(self.id , self.room_uid , self.nm , key , iv))).start()
                                    time.sleep(0.1)
                                    self.CliEnts.close() ; self.CliEnts2.close()
                                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	    		       
                                except:pass
                                
                        elif False == self.res and True == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][ffffff] U Reched Max Limit To SEnd SPam\n Try AfTer : {xMsGFixinG(self.time)} !\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                            
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /room<id> <name>\n - Ex : /room{self.Exemple} Black Team\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                            time.sleep(0.1)
                            self.CliEnts.close() ; self.CliEnts2.close()
                            self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)	
                    elif '/ou/' in self.input_msg[:4]:
                        self.id_part = self.input_msg[4:]
                        parts = self.id_part.split(" ", 1)
                        self.id = parts[0] 
                        self.ghost_name = parts[1] if len(parts) > 1 else "Blackf-t"
                        self.Zx = ChEck_Commande(self.id)
                        if True == self.Zx:
                            try:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري إرسال طلب انضمام إلى سكواد اللاعب {xMsGFixinG(self.id)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                self.CliEnts2.send(SPamSq(self.id, key, iv))
                                time.sleep(2)
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] في انتظار قبول الطلب...\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                self.CliEnts2.send(AccEpT(self.id, self.AutH, key, iv))
                                time.sleep(2)
                                start_time = time.time()
                                while time.time() - start_time < 10:  
                                    if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                        packet = self.DaTa2.hex()[10:]
                                        self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                        self.sq_code = self.BesTo_data["5"]["data"]["31"]["data"]
                                        self.sq_leader = self.BesTo_data["5"]["data"]["1"]["data"]
                                        self.CliEnts2.send(ExiT('000000', key, iv))
                                        time.sleep(1)
                                        self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] جاري إرسال الشبح "{self.ghost_name}" إلى السكواد {xMsGFixinG(self.sq_code)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                        self.CliEnts2.send(ghost_pakcet(self.sq_leader, self.ghost_name, self.sq_code, key, iv))
                                        time.sleep(0.01)
                                        self.CliEnts2.send(ExiT('000000', key, iv))
                                        time.sleep(0.01)
                                        self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]تم إرسال الشبح "{self.ghost_name}" بنجاح!\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                                        break
                                    time.sleep(0.1)
                                else:
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]لم يتم قبول الطلب خلال الوقت المحدد\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))                                
                            except Exception as e:
                                self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]حدث خطأ: {str(e)}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.3)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                            
                        elif False == self.Zx:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - الصيغة الصحيحة: /9t/<آيدي>\n - مثال: /9t/{self.Exemple}\n', 2, self.DeCode_CliEnt_Uid, self.DeCode_CliEnt_Uid, key, iv))
                            time.sleep(0.1)
                            self.CliEnts.close(); self.CliEnts2.close()
                            self.Connect_SerVer(Token, tok, host, port, key, iv, host2, port2)
                    elif '/status' in self.input_msg[:4]:
                        self.id = self.input_msg[4:]
                        self.Zx = ChEck_Commande(self.id)
                        if True == self.Zx:	            		     
                            try:
                                  self.CliEnts2.send(GeT_Status(self.id , key , iv))
                                  time.sleep(0.3)
                            except:pass   
                            if '0f00' in self.DaTa2.hex()[:4]:
                                packet = self.DaTa2.hex()[10:]
                                try:
                                    self.BesTo_data = json.loads(DeCode_PackEt(packet))
                                    self.target_id = self.BesTo_data["5"]["data"]["1"]["data"]["1"]["data"]
                                    self.h = self.BesTo_data["5"]["data"]["1"]["data"]["3"]["data"]
                                except:pass						
                                try:status_data = self.BesTo_data["5"]["data"]["1"]["data"]["3"]["data"]
                                except:pass
                                try:		
                                    if self.h == 1:
                                        try:
                                            self.last = self.BesTo_data["5"]["data"]["1"]["data"]["4"]["data"]	                
                                        except:
                                            self.last = 'No DaTa !'
                                        self.name = GeT_Name(self.target_id , Token)
                                        self.name = str(self.name)
                                        self.CliEnts.send(xSEndMsg(f"[b][c]\n Status InFo Of The PLayer : \n\n[{ArA_CoLor()}]PLayer Uid : {xMsGFixinG(self.target_id)}\nPLayer Status : SoLo\nPLayer s'Name : {self.name}\nLast Login : {xMsGFixinG(datetime.fromtimestamp(self.last).strftime('%I:%M %p %d/%m/%y'))}\n\n[ffffff] Dev : Black\n", 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)					
                                    elif self.h == 2:
                                        self.leader = xMsGFixinG(self.BesTo_data["5"]["data"]["1"]["data"]["8"]["data"])
                                        self.group_count = self.BesTo_data["5"]["data"]["1"]["data"]["9"]["data"]
                                        self.group_count2 = self.BesTo_data["5"]["data"]["1"]["data"]["10"]["data"]
                                        self.leader_id = self.BesTo_data["5"]["data"]["1"]["data"]["8"]["data"]
                                        self.name = GeT_Name(self.leader_id , Token)
                                        self.name = str(self.name)
                                        self.time = self.BesTo_data["5"]["data"]["1"]["data"]["4"]["data"]
                                        self.CliEnts.send(xSEndMsg(f"[b][c]\n Status InFo Of The PLayer : \n\n[{ArA_CoLor()}]PLayer Uid : {xMsGFixinG(self.target_id)}\nPLayer Status : His In Squid\nSquid s'Leader : {self.leader}\nLeader s'Name : {self.name}\nSquid Count : {self.group_count}/{self.group_count2 + 1}\nLast Login : {xMsGFixinG(datetime.fromtimestamp(self.time).strftime('%I:%M %p %d/%m/%y'))}\n\n[ffffff] Dev : Black\n", 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    elif self.h in [3 , 5]:
                                        self.CliEnts.send(xSEndMsg(f"[b][c]\n Status InFo Of The PLayer : \n\nPLayer Uid : {xMsGFixinG(self.target_id)}\nPLayer Status : In Game\nLast Login : {xMsGFixinG(datetime.fromtimestamp(self.time).strftime('%I:%M %p %d/%m/%y'))}\n\n[ffffff]  Dev : blackf-t\n", 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    else:
                                        self.CliEnts.send(xSEndMsg(f'\n[b][c][FFD700]FaiLEd GeTinG STaTus InFo\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                        time.sleep(0.3)
                                        self.CliEnts.close() ; self.CliEnts2.close()
                                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                except:pass
                        if False == self.Zx: self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] - PLease Use /status<id>\n - Ex : /status{self.Exemple}\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))	
                                                          
                        
                                                           
                    elif '/ayj' in self.input_msg[:3]:  
                        self.CliEnts.send(xSEndMsg(f'hhhh', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv)) 
                        time.sleep(0.3)   
                        self.CliEnts2.send(SPamSq(self.DeCode_CliEnt_Uid , key , iv))
                        time.sleep(1)
                        self.CliEnts2.send(AccEpT(self.DeCode_CliEnt_Uid , self.AutH , key , iv))

                    elif '/psps/' in self.input_msg[:6]:
                        self.id , self.nm = (self.input_msg[6:].split(" ", 1) if " " in self.input_msg[6:] else [self.input_msg[6:], "sponge japoni"])  
                        
                        
                        self.CliEnts.send(xSEndMsg(f'\n[b][c][{ArA_CoLor()}] Preparing ghost for {xMsGFixinG(self.id)}...\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        
                        
                        self.CliEnts2.send(OpEnSq(key , iv))
                        time.sleep(1)  
                        
                        
                        self.CliEnts2.send(cHSq(5 , self.id , key , iv))
                        time.sleep(1)  
                        
                        
                        start_time = time.time()
                        while time.time() - start_time < 5: 
                            if '0500' in self.DaTa2.hex()[0:4] and len(self.DaTa2.hex()) > 30:
                                self.dT = json.loads(DeCode_PackEt(self.DaTa2.hex()[10:]))
                                if "5" in self.dT and "data" in self.dT["5"] and "31" in self.dT["5"]["data"]:
                                    sq = self.dT["5"]["data"]["31"]["data"]
                                    print(f"Successfully got squad code: {sq}")
                                    
                                    
                                    self.CliEnts2.send(SEnd_InV(1 , self.id , key , iv))
                                    time.sleep(3)
                                    
                                    
                                    self.CliEnts2.send(ExiT('000000' , key , iv))
                                    time.sleep(1)
                                    
                                    
                                    for i in range(10):  
                                        self.CliEnts2.send(ghost_pakcet(self.id , self.nm , sq , key , iv))
                                        time.sleep(0.5)
                                    
                                    self.CliEnts.send(xSEndMsg(f'\n[b][c][90EE90]Ghost sent successfully!\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                                    break
                            time.sleep(0.1)
                        else:
                            self.CliEnts.send(xSEndMsg(f'\n[b][c][FF0000]Failed to get squad info!\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))
                        
                        self.CliEnts.close(); self.CliEnts2.close()
                        self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)

                    elif 'ss' in self.input_msg[:2]:#1750289322058798839_51s3raxooz
                            for i in range(100): 
                                self.CliEnts2.send(ghost_pakcet(self.DeCode_CliEnt_Uid ,'8679231987', '1750287629500765351_vfhkisb7hv' , key , iv))
                                time.sleep(0.1)     	    
                            self.CliEnts.send(xSEndMsg(f'\n[b][c]DONE  !\n', 2 , self.DeCode_CliEnt_Uid , self.DeCode_CliEnt_Uid , key , iv))           		      	            			      	
                except Exception as e:
                    self.CliEnts.close() ; self.CliEnts2.close()
                    self.Connect_SerVer(Token , tok , host , port , key , iv , host2 , port2)
                                    
    def GeT_Key_Iv(self , serialized_data):
        my_message = xKEys.MyMessage()
        my_message.ParseFromString(serialized_data)
        timestamp , key , iv = my_message.field21 , my_message.field22 , my_message.field23
        timestamp_obj = Timestamp()
        timestamp_obj.FromNanoseconds(timestamp)
        timestamp_seconds = timestamp_obj.seconds
        timestamp_nanos = timestamp_obj.nanos
        combined_timestamp = timestamp_seconds * 1_000_000_000 + timestamp_nanos
        return combined_timestamp , key , iv    

    def Guest_GeneRaTe(self , uid , password):
        self.url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        self.headers = {"Host": "100067.connect.garena.com","User-Agent": "GarenaMSDK/4.0.19P4(G011A ;Android 9;en;US;)","Content-Type": "application/x-www-form-urlencoded","Accept-Encoding": "gzip, deflate, br","Connection": "close",}
        self.dataa = {"uid": f"{uid}","password": f"{password}","response_type": "token","client_type": "2","client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3","client_id": "100067",}
        try:
            self.response = requests.post(self.url, headers=self.headers, data=self.dataa).json()
            self.Access_ToKen , self.Access_Uid = self.response['access_token'] , self.response['open_id']
            time.sleep(0.2)
            print(' - Starting Black Freind BoT !')
            print(f' - Uid : {uid}\n - Password : {password}')
            print(f' - Access Token : {self.Access_ToKen}\n - Access Id : {self.Access_Uid}')
            return self.ToKen_GeneRaTe(self.Access_ToKen , self.Access_Uid)
        except Exception: ResTarT_BoT()    
                                        
    def GeT_LoGin_PorTs(self , JwT_ToKen , PayLoad):
        self.UrL = 'https://clientbp.common.ggbluefox.com/GetLoginData'
        self.HeadErs = {
            'Expect': '100-continue',
            'Authorization': f'Bearer {JwT_ToKen}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB50',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)',
            'Host': 'clientbp.common.ggbluefox.com',
            'Connection': 'close',
            'Accept-Encoding': 'gzip, deflate, br',}       
        try:
                self.Res = requests.post(self.UrL , headers=self.HeadErs , data=PayLoad , verify=False)
                self.BesTo_data = json.loads(DeCode_PackEt(self.Res.content.hex()))  
                address , address2 = self.BesTo_data['32']['data'] , self.BesTo_data['14']['data'] 
                ip , ip2 = address[:len(address) - 6] , address2[:len(address) - 6]
                port , port2 = address[len(address) - 5:] , address2[len(address2) - 5:]             
                return ip , port , ip2 , port2          
        except requests.RequestException as e:
                print(f" - Bad Requests !")
        print(" - Failed To GeT PorTs !")
        return None, None   
        
    def ToKen_GeneRaTe(self , Access_ToKen , Access_Uid):
        self.UrL = "https://loginbp.common.ggbluefox.com/MajorLogin"
        self.HeadErs = {
            'X-Unity-Version': '2018.4.11f1',
            'ReleaseVersion': 'OB50',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-GA': 'v1 1',
            'Content-Length': '928',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
            'Host': 'loginbp.common.ggbluefox.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'}   
        self.dT = bytes.fromhex('1a13323032352d30372d33302031343a31313a3230220966726565206669726528013a07322e3131342e324234416e64726f6964204f53203133202f204150492d33332028545031412e3232303632342e3031342f3235303531355631393737294a0848616e6468656c6452094f72616e676520544e5a0457494649609c1368b80872033438307a1d41524d3634204650204153494d4420414553207c2032303030207c20388001973c8a010c4d616c692d473532204d433292013e4f70656e474c20455320332e322076312e72333270312d3031656163302e32613839336330346361303032366332653638303264626537643761663563359a012b476f6f676c657c61326365613833342d353732362d346235622d383666322d373130356364386666353530a2010e3139362e3138372e3132382e3334aa0102656eb201203965373166616266343364383863303662373966353438313034633766636237ba010134c2010848616e6468656c64ca0115494e46494e495820496e66696e6978205836383336ea014063363231663264363231343330646163316137383261306461623634653663383061393734613662633732386366326536623132323464313836633962376166f00101ca02094f72616e676520544ed2020457494649ca03203161633462383065636630343738613434323033626638666163363132306635e003dc810ee803daa106f003ef068004e7a5068804dc810e9004e7a5069804dc810ec80403d2045b2f646174612f6170702f7e7e73444e524632526357313830465a4d66624d5a636b773d3d2f636f6d2e6474732e66726565666972656d61782d4a534d4f476d33464e59454271535376587767495a413d3d2f6c69622f61726d3634e00402ea047b61393862306265333734326162303061313966393737633637633031633266617c2f646174612f6170702f7e7e73444e524632526357313830465a4d66624d5a636b773d3d2f636f6d2e6474732e66726565666972656d61782d4a534d4f476d33464e59454271535376587767495a413d3d2f626173652e61706bf00402f804028a050236349a050a32303139313135363537a80503b205094f70656e474c455333b805ff7fc00504d20506526164c3a873da05023133e005b9f601ea050b616e64726f69645f6d6178f2055c4b71734854346230414a3777466c617231594d4b693653517a6732726b3665764f38334f306f59306763635a626457467a785633483564454f586a47704e3967476956774b7533547a312b716a36326546673074627537664350553d8206147b226375725f72617465223a5b36302c39305d7d8806019006019a060134a2060134b20600')
        self.dT = self.dT.replace(b'2025-07-30 14:11:20' , str(datetime.now())[:-7].encode())        
        self.dT = self.dT.replace(b'c621f2d621430dac1a782a0dab64e6c80a974a6bc728cf2e6b1224d186c9b7af' , Access_ToKen.encode())
        self.dT = self.dT.replace(b'9e71fabf43d88c06b79f548104c7fcb7' , Access_Uid.encode())
        self.PaYload = bytes.fromhex(EnC_AEs(self.dT.hex()))  
        self.ResPonse = requests.post(self.UrL, headers = self.HeadErs ,  data = self.PaYload , verify=False)        
        if self.ResPonse.status_code == 200 and len(self.ResPonse.text) > 10:
            self.BesTo_data = json.loads(DeCode_PackEt(self.ResPonse.content.hex()))
            self.JwT_ToKen = self.BesTo_data['8']['data']           
            self.combined_timestamp , self.key , self.iv = self.GeT_Key_Iv(self.ResPonse.content)
            ip , port , ip2 , port2 = self.GeT_LoGin_PorTs(self.JwT_ToKen , self.PaYload)            
            return self.JwT_ToKen , self.key , self.iv, self.combined_timestamp , ip , port , ip2 , port2
        else:
            sys.exit()
      
    def Get_FiNal_ToKen_0115(self):
        token , key , iv , Timestamp , ip , port , ip2 , port2 = self.Guest_GeneRaTe(self.id , self.password)
        self.JwT_ToKen = token        
        try:
            self.AfTer_DeC_JwT = jwt.decode(token, options={"verify_signature": False})
            self.AccounT_Uid = self.AfTer_DeC_JwT.get('account_id')
            self.EncoDed_AccounT = hex(self.AccounT_Uid)[2:]
            self.HeX_VaLue = DecodE_HeX(Timestamp)
            self.TimE_HEx = self.HeX_VaLue
            self.JwT_ToKen_ = token.encode().hex()
            print(f' - ProxCed Uid : {self.AccounT_Uid}')
        except Exception as e:
            print(f" - Error In ToKen : {e}")
            return
        try:
            self.Header = hex(len(EnC_PacKeT(self.JwT_ToKen_, key, iv)) // 2)[2:]
            length = len(self.EncoDed_AccounT)
            self.__ = '00000000'
            if length == 9: self.__ = '0000000'
            elif length == 8: self.__ = '00000000  '
            elif length == 10: self.__ = '000000'
            elif length == 7: self.__ = '000000000'
            else:
                print('Unexpected length encountered')                
            self.Header = f'0115{self.__}{self.EncoDed_AccounT}{self.TimE_HEx}00000{self.Header}'
            self.FiNal_ToKen_0115 = self.Header + EnC_PacKeT(self.JwT_ToKen_ , key , iv)
        except Exception as e:
            print(f" - Erorr In Final Token : {e}")
        self.AutH_ToKen = self.FiNal_ToKen_0115
        self.Connect_SerVer(self.JwT_ToKen , self.AutH_ToKen , ip , port , key , iv , ip2 , port2)        
        return self.AutH_ToKen , key , iv
def StarT_SerVer():

    FF_CLient('هنا حط uid بوتك','هنا حط password بوتك')
  
StarT_SerVer() 