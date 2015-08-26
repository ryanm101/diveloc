from lxml import html
import requests
import json
import sys
import re
import datetime

wrecklinks = [    
    'http://irishwrecksonline.net/details/Clemintine200.htm', 
    'http://irishwrecksonline.net/details/Thrush775.htm', 
    'http://irishwrecksonline.net/details/StateOfLouisiana700.htm', 
    'http://irishwrecksonline.net/details/Ailsa92.htm', 
    'http://irishwrecksonline.net/details/Berbice116a.htm', 
    'http://irishwrecksonline.net/details/BlackDiamond118.htm', 
    'http://irishwrecksonline.net/details/George495.htm', 
    'http://irishwrecksonline.net/details/Harrington515a.htm', 
    'http://irishwrecksonline.net/details/Peridot654.htm', 
    'http://irishwrecksonline.net/details/Teanua740.htm', 
    'http://irishwrecksonline.net/details/Alcedo98.htm', 
    'http://irishwrecksonline.net/details/Woods995.htm', 
    'http://irishwrecksonline.net/details/Inverurie543.htm', 
    'http://irishwrecksonline.net/details/Alastor93.htm', 
    'http://irishwrecksonline.net/details/Amber103.htm', 
    'http://irishwrecksonline.net/details/Upas980.htm', 
    'http://irishwrecksonline.net/details/Neotsfield640.htm', 
    'http://irishwrecksonline.net/details/LochSunart580.htm', 
    'http://irishwrecksonline.net/details/Beechgrove116aa.htm', 
    'http://irishwrecksonline.net/details/Kilbroney546.htm', 
    'http://irishwrecksonline.net/details/SaintBarchan680.htm', 
    'http://irishwrecksonline.net/details/Harold515.htm', 
    'http://irishwrecksonline.net/details/Connemara215.htm', 
    'http://irishwrecksonline.net/details/Retriever668.htm', 
    'http://irishwrecksonline.net/details/SaintBarchan680.htm', 
    'http://irishwrecksonline.net/details/Beechgrove116aa.htm', 
    'http://irishwrecksonline.net/details/GuideMeII514a.htm', 
    'http://irishwrecksonline.net/details/Leinster555.htm', 
    'http://irishwrecksonline.net/details/QueenVictoria663.htm', 
    'http://irishwrecksonline.net/details/Polewell657.htm', 
    'http://irishwrecksonline.net/details/Bolivar121.htm', 
    'http://irishwrecksonline.net/details/VanguardHMS997.htm', 
    'http://irishwrecksonline.net/details/AnnaToop104a.htm', 
    'http://irishwrecksonline.net/details/RoyalArthur672.htm', 
    'http://irishwrecksonline.net/details/Lennox557.htm', 
    'http://irishwrecksonline.net/details/ManchesterMarket619.htm', 
    'http://irishwrecksonline.net/details/Invercauld542a.htm', 
    'http://irishwrecksonline.net/details/Idaho541a.htm', 
    'http://irishwrecksonline.net/details/Bandon114b.htm', 
    'http://irishwrecksonline.net/details/Celtic134.htm', 
    'http://irishwrecksonline.net/details/Folia397.htm', 
    'http://irishwrecksonline.net/details/CityOfChicago160.htm', 
    'http://irishwrecksonline.net/details/CrescentCity235.htm', 
    'http://irishwrecksonline.net/details/Lusitania608.htm', 
    'http://irishwrecksonline.net/details/Norwegian647a.htm', 
    'http://irishwrecksonline.net/details/U260-948a.htm', 
    'http://irishwrecksonline.net/details/MignonetteHMS630.htm', 
    'http://irishwrecksonline.net/details/CardiffHall123.htm', 
    'http://irishwrecksonline.net/details/Queensmore662.htm', 
    'http://irishwrecksonline.net/details/Iberian541.htm', 
    'http://irishwrecksonline.net/details/Oswestry651.htm', 
    'http://irishwrecksonline.net/details/Limpatiente548a.htm', 
    'http://irishwrecksonline.net/details/Bohemian119.htm', 
    'http://irishwrecksonline.net/details/Memphis625.htm', 
    'http://irishwrecksonline.net/details/StephenWhitney704.htm', 
    'http://irishwrecksonline.net/details/Nestorian641.htm', 
    'http://irishwrecksonline.net/details/Illyrian542.htm',
    'http://irishwrecksonline.net/details/Mystique638.htm',
    'http://irishwrecksonline.net/details/Malmanger618a.htm', 
    'http://irishwrecksonline.net/details/Alondra101.htm', 
    'http://irishwrecksonline.net/details/KowloonBridge548.htm',
    'http://irishwrecksonline.net/details/Carnavonshire124.htm',
    'http://irishwrecksonline.net/details/Dido265.htm', 
    'http://irishwrecksonline.net/details/Asian113a.htm',
    'http://irishwrecksonline.net/details/LadyCharlotte548b.htm',
    'http://irishwrecksonline.net/details/Manaos618b.htm',
    'http://irishwrecksonline.net/details/Ribble664.htm', 
    'http://irishwrecksonline.net/details/BardiniReefer115a.htm', 
    'http://irishwrecksonline.net/details/ContessaViv220.htm',
    'http://irishwrecksonline.net/details/Crompton240.htm',
    'http://irishwrecksonline.net/details/PB4Y653b.htm',
    'http://irishwrecksonline.net/details/Barrister116.htm',
    'http://irishwrecksonline.net/details/AghiaEirini90.htm',
    'http://irishwrecksonline.net/details/CharlesSParnell145.htm',
    'http://irishwrecksonline.net/details/Ogano649.htm', 
    'http://irishwrecksonline.net/details/GirlMaureen509a.htm', 
    'http://irishwrecksonline.net/details/Laurentic551.htm',
    'http://irishwrecksonline.net/details/Florence395a.htm',
    'http://irishwrecksonline.net/details/KalliopiS545.htm',
    'http://irishwrecksonline.net/details/Gaelic470.htm', 
    'http://irishwrecksonline.net/details/WaspHMS991.htm',
    'http://irishwrecksonline.net/details/Laurentic550.htm',
    'http://irishwrecksonline.net/details/Towy800.htm',
    'http://irishwrecksonline.net/details/Nokomis645.htm', 
    'http://irishwrecksonline.net/details/Stipey710.htm', 
    'http://irishwrecksonline.net/details/Florence395.htm',
    'http://irishwrecksonline.net/details/ArgoDelos113.htm',
    'http://irishwrecksonline.net/details/EmpireHeritage358.htm', 
    'http://irishwrecksonline.net/details/Cumberland244a.htm',
    'http://irishwrecksonline.net/details/CastleEden127.htm',
    'http://irishwrecksonline.net/details/Assurance114.htm', 
    'http://irishwrecksonline.net/details/SaldahnaHMS682.htm',
    'http://irishwrecksonline.net/details/WilliamMannell993.htm', 
    'http://irishwrecksonline.net/details/CorientesHMT225.htm',
    'http://irishwrecksonline.net/details/Justicia544ayy.htm', 
    'http://irishwrecksonline.net/details/U1003-948b.htm', 
    'http://irishwrecksonline.net/details/Templemore750.htm', 
    'http://irishwrecksonline.net/details/Glentow514.htm', 
    'http://irishwrecksonline.net/details/SantaMaria684.htm', 
    'http://irishwrecksonline.net/details/CityOfBristol155.htm',
    'http://irishwrecksonline.net/details/Chirripo150.htm', 
    'http://irishwrecksonline.net/details/Fredanja400.htm', 
    'http://irishwrecksonline.net/details/Tiberia778.htm',
    'http://irishwrecksonline.net/details/Oregon650.htm',
    'http://irishwrecksonline.net/details/Ulrica900.htm', 
    'http://irishwrecksonline.net/details/Rose670.htm', 
    'http://irishwrecksonline.net/details/Lagan549.htm',
    'http://irishwrecksonline.net/details/Troutpool850.htm', 
    'http://irishwrecksonline.net/details/Karanan544a.htm', 
    'http://irishwrecksonline.net/details/Annagher105.htm', 
    'http://irishwrecksonline.net/details/NormanbyHall646.htm',
    'http://irishwrecksonline.net/details/Housatonic520.htm',
    'http://irishwrecksonline.net/details/Sumatra725.htm', 
    'http://irishwrecksonline.net/details/Maria620.htm', 
    'http://irishwrecksonline.net/details/Unknown1001.htm', 
    'http://irishwrecksonline.net/details/Unknown1002.htm', 
    'http://irishwrecksonline.net/details/Dalriada247.htm',
    'http://irishwrecksonline.net/details/Albia95.htm', 
    'http://irishwrecksonline.net/details/Norseman647.htm',
    'http://irishwrecksonline.net/details/Overton653.htm',
    'http://irishwrecksonline.net/details/Nimble643.htm', 
    'http://irishwrecksonline.net/details/EmpireTana360.htm', 
    'http://irishwrecksonline.net/details/Zarina1000.htm', 
    'http://irishwrecksonline.net/details/Tornamona790.htm',
    'http://irishwrecksonline.net/details/GeorgetownVictory500.htm', 
    'http://irishwrecksonline.net/details/Hunsdon540.htm',
    'http://irishwrecksonline.net/details/Helgoland516.htm', 
    'http://irishwrecksonline.net/details/ArantazuMendi110.htm', 
    'http://irishwrecksonline.net/details/Frieda405.htm', 
    'http://irishwrecksonline.net/details/ArchibaldFinnie112.htm',
    'http://irishwrecksonline.net/details/Bangor115.htm',
    'http://irishwrecksonline.net/details/Daybreak250.htm', 
    'http://irishwrecksonline.net/details/Strathtay715.htm',
    'http://irishwrecksonline.net/details/Shamrock689.htm',
    'http://irishwrecksonline.net/details/Tayleur745.htm', 
    'http://irishwrecksonline.net/details/Quebra660.htm', 
    'http://irishwrecksonline.net/details/TheThreeBrothers755.htm',
    'http://irishwrecksonline.net/details/CarraigUna125.htm',
    'http://irishwrecksonline.net/details/EvelynMarie375.htm',
    'http://irishwrecksonline.net/details/Skijford690.htm', 
    'http://irishwrecksonline.net/details/Eleftherios347.htm', 
    'http://irishwrecksonline.net/details/AndrewNugent104.htm',
    'http://irishwrecksonline.net/details/Tuscania860.htm',
    'http://irishwrecksonline.net/details/ErloHills370.htm',
    'http://irishwrecksonline.net/details/Gavina480.htm', 
    'http://irishwrecksonline.net/details/JamesStewart544.htm',
    'http://irishwrecksonline.net/details/HerMajesty517.htm',
    'http://irishwrecksonline.net/details/Cumberland244.htm', 
    'http://irishwrecksonline.net/details/Lindron565.htm', 
    'http://irishwrecksonline.net/details/BriskHMS122.htm',
    'http://irishwrecksonline.net/details/Bouncer120.htm', 
    'http://irishwrecksonline.net/details/KnightsGareth547.htm',
    'http://irishwrecksonline.net/details/Lugano605.htm', 
    'http://irishwrecksonline.net/details/Girvan512.htm',
    'http://irishwrecksonline.net/details/Pintail655.htm', 
    'http://irishwrecksonline.net/details/Hinde519.htm', 
    'http://irishwrecksonline.net/details/Shackleton688.htm', 
    'http://irishwrecksonline.net/details/Diamond260.htm', 
    'http://irishwrecksonline.net/details/BerryBretagne117.htm',
    'http://irishwrecksonline.net/details/Lochgarry600.htm',
    'http://irishwrecksonline.net/details/EllaHewitt350.htm',
    'http://irishwrecksonline.net/details/DrakeHMS300.htm',
    'http://irishwrecksonline.net/details/Andania103a.htm' ]
skiplinks = [
    "http://irishwrecksonline.net/details/Unknown1001.htm",
    "http://irishwrecksonline.net/details/Unknown1002.htm",
    "http://irishwrecksonline.net/details/Skijford690.htm"
    #"http://irishwrecksonline.net/details/CastleEden127.htm"  # Cant Parse Manual
    #"http://irishwrecksonline.net/details/Pintail655.htm" # Error
    ]  
    
# 
wrecklist = []
deadlinks = []
hshWrecks = {}
hshFWrecks = {}

for wrecklink in wrecklinks:
    if (wrecklink in skiplinks):
        continue
    r = requests.get(wrecklink)
    if (r.status_code == 404):
        deadlinks.append(wrecklink)
        continue
        
    tree = html.fromstring(r.text)
    WreckName = tree.xpath('/html/head/meta[@name="description"]/@content')[0].split(" - ")[1].strip()
    lu = tree.xpath('/html/body/table/tr/td/table[@width="100%"]/tr/td/div/p//text()')
    if (lu):
        resturl = "http://127.0.0.1:3000/wrecks/" + WreckName
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.get(resturl, headers=headers)
        wreck = r.json()
        wreck['irishwrecksonlineurl'] = wrecklink
        print()
        print(wrecklink + ": " + lu[1].strip())
        wreck['lastupdated'] = str(datetime.datetime.strptime(lu[1].replace("Sept","Sep").strip(), '%d-%b-%Y').date())
        print(json.dumps(wreck))
    else:
        hshFWrecks[WreckName] = lu
    
#print (hshWrecks)
#print ()
print (hshFWrecks)