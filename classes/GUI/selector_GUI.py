import tkinter
import tkinter.messagebox
import customtkinter
import time

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

from data.schedule import schedule

# from data.data import STUDENT_COURSES

class App(customtkinter.CTk):
    def __init__(self): #student_list
        super().__init__()

        # self.student_convert_dict = self.__init_student_convert_dict(student_list)

        self.student_convert_dict = {52311353: 'Yanick Abbing', 76903244: 'Roelof Adam', 6709529: 'Willibrordus Agema', 70015932: 'Servaas Anker', 82066165: 'Wissal Ankone', 1886996: 'Herman Apeldoorn', 13534377: 'Evi Appel', 54395877: 'Wilmer Appelhof', 53512831: 'Benjamin Arendse', 56348773: 'Diny Aslan', 13218321: 'Chesney Autar', 13284244: 'Martin Avci', 36748818: 'Gidon Baetsen', 50184318: 'Rhona Bakkum', 64296965: 'Wafa Bart', 42778953: 'Sharan Baselmans', 82689818: 'Edin Bastings', 81385263: 'Mattijs Baudoin', 51741554: 'Ravi Bauer', 63939720: 'Wiert Becht', 70844780: 'Kyllian Bekkema', 97135019: 'Marrie Bekker', 78136904: 'Angle Berentsen', 8522855: 'Emil Bergmans', 27064249: 'Tian Berkers', 82872148: 'Annique Berrevoets', 93023961: 'Theadora Besemer', 22871048: 'Abdallah Beulen', 96554914: 'Eltjo Beunen', 41585485: 'Saba Bhaggoe', 46052388: 'Ella Bischoff', 34691309: 'Perry Blijleven', 54074680: 'Thyrza Blik', 81200278: 'Jarik Blikman', 18266644: 'Monika Blikman', 1075391: 'Marco Bloemert', 44151631: 'Anjana Bloemsma', 69459473: 'Guilliano Blomsma', 40791377: 'Lenne Boateng', 5368702: 'Amadou Boekema', 88737765: 'Armin Bol', 27916487: 'Rayn Bolding', 20239127: 'Jeremey Bontenbal', 28943658: 'Tariq Bood', 70939718: 'Hiba Boogert', 73893840: 'Kely Borg', 51415617: 'Ken Borsboom', 19540225: 'Narin Boshuis', 93361408: 'Rudolph Bosman', 59220392: 'Jael Boutkan', 82233873: 'Resi Braamhaar', 36785409: 'Hanne Brans', 77831658: 'Cyrina Brasser', 45556081: 'Femia Brink', 5615125: 'Renze Brink', 44940353: 'Nyncke Brinks', 49922855: 'Wulfert Brinksma', 56815156: 'Ilyass Broeks', 14671406: 'Ethan Broer', 62872965: 'Tarah Broerse', 23257088: 'Devlin Bronsema', 91196968: 'Sayfeddine Bruijnes', 5517869: 'Virginie Brunsveld', 62736669: 'Angus Brusse', 87602030: 'Allan Budel', 86988337: 'Wytske Buining', 77636749: 'Rika Buizer', 86807027: 'Vivianne Buter', 29718115: 'Abdel Buth', 54569540: 'Donna Buurma', 12077419: 'Lucienne Caris', 22826928: 'Samyra Çetin', 60661905: 'Liana Charita', 96054456: 'Yde Christiaens', 13718298: 'Hailey Claassen', 52304977: 'Seyit Cleven', 7957843: 'Jorike Coenen', 33760909: 'Laurentia Cooijmans', 15911353: 'Mitzi Corten', 24891081: 'Jildou Corvers', 5590289: 'Abdelouahid Cramer', 27582862: 'Hananja Cramer', 65003379: 'Jonas Crombach', 27370083: 'Goven Curfs', 17496687: 'Everhard Curvers', 15249775: 'Amelie Daams', 66701209: 'Gradus Dams', 41644639: 'Goos Dane', 46701583: 'Manuel de Boon', 58565406: 'Albertien de Hoogh', 19214659: 'Kathryn de Jongste', 96082155: 'Anes de Kanter', 33946407: 'Krijna de Kreij', 63573738: 'Farhad de Kuijer', 66433883: 'Janniek de Leest', 90743504: 'Wieke de Leest', 3727435: 'Yana de Looff', 16011419: 'Alexandre de Olde', 3678531: 'Merel de Olde', 82968410: 'Ziggy de Smit', 51673172: 'Mayla de Snoo', 64393888: 'Marije de Vreeze', 39919665: 'Linne de Zoete', 93566383: 'Quido Deniz', 50143947: 'Brigitta Diallo', 670011: 'Boy Dibbets', 65978354: 'Marjory Dielen', 76487754: 'Pietro Dieperink', 57467488: 'Andre Dieters', 47932106: 'Kelly Doedens', 37419523: 'Winfried Doeve', 19958553: 'Oumaima Donselaar', 53267490: 'Maruschka Doppenberg', 40911986: 'Siri Droge', 3168419: 'Sola Droog', 26260141: 'Ko Droste', 68315599: 'Doede Duiveman', 78822885: 'Rintje Dumoulin', 75599734: 'Brecht Eeltink', 4529208: 'Wissal Eggens', 31103066: 'Catharinus Eggermont', 59075181: 'Mattie Eisinga', 59544049: 'Ludovicus Eissens', 59397895: 'Pearl Elberse', 33930505: 'Raven Elissen', 79033175: 'Bauke Elschot', 31633723: 'Geerten Elschot', 7492204: 'Dinah Ensink', 1181560: 'Hande Essink', 54772132: 'Jaro Essink', 74131924: 'Herwin Ester', 27298319: 'Jurrian Fekkes', 66621166: 'Nurcan Fennis', 65852230: 'Antonius Fleming', 14941752: 'Belle Florijn', 85335143: 'Diemer Fokkens', 37830626: 'Ynze Freriks', 45414528: 'Nordin Geboers', 93041523: 'Bahattin Geelen', 87758823: 'Sohrab Geers', 67073567: 'Patric Geluk', 18477924: 'Eddy Gerritse', 11915563: 'Deacon Gielissen', 14637758: 'Richenel Giesen', 48308205: 'Abdelkader Gijbels', 49219163: 'Marco Gilsing', 78243495: 'Maritte Gok', 19337738: 'Rivelino Goor', 70113753: 'Umar Grift', 4546613: 'Rijkje Groote', 7106649: 'Bert Grooteman', 72895450: 'Yalda Grootenboer', 13132925: 'Faruk Haalboom', 53139134: 'Jetty Haanstra', 77264363: 'Gabe Haarman', 58332004: 'Eylem Haas', 51593625: 'Virgill Hamelink', 14383795: 'Judi Hamers', 51472074: 'Olle Hamhuis', 71839156: 'Sahar Hamstra', 20095994: 'Ervin Hartevelt', 14398123: 'Berdina Heijman', 6939933: 'Guus Heijnen', 1048485: 'Rosali Heikoop', 99453514: 'Mahmud Heller', 38179241: 'Sergio Hijdra', 36508571: 'Bo Hilhorst', 49683101: 'Dana Hoeksema', 58480929: 'Sverre Hoenderdos', 49908313: 'Anne-Jet Hofman', 535689: 'Johanne Holstein', 5526560: 'Nesrin Holt', 34900967: 'Florus Holtkamp', 43460038: 'Christal Hoogerbrugge', 62356458: 'Esmee Hooijmaijers', 87314964: 'Michal Hooiveld', 10149535: 'Catherine Hoornstra', 2317551: 'Tea Horstink', 31416266: 'Wichard Hospers', 41790793: 'Kyra Huibers', 5298748: 'Paulette Hunting', 87210640: 'Ytje Hup', 77376714: 'Frederic IJkema', 88597745: 'Marnik Imthorn', 45660925: 'Geartsje Jackson', 91139627: 'Rino Jacob', 73823548: 'Faya Jagersma', 54540997: 'Paulo Jak', 28359697: 'Owen Jama', 84524083: 'Le Janga', 66122625: 'Kyan Jankie', 21192048: 'Nikolas Jansema', 94467156: 'Tamar Jongbloed', 15902055: 'Jenske Jongejan', 92496780: 'Aradhna Jonkergouw', 75585647: 'Gerritjan Joris', 80709893: 'Marssae Joseph', 10702778: 'Miko Kalpoe', 38499176: 'Chrystel Kalshoven', 6249823: 'Yaro Kamp', 92778619: 'Riana Kampers', 75005528: 'Juliette Kant', 3685034: 'Esme Karim', 69634191: 'Devon Keijser', 58083680: 'Enya Kemps', 33776961: 'Ceciel Kentie', 11459236: 'Thys Kersten', 34773179: 'Kimmy Kesteloo', 1766560: 'Lysbeth Keuken', 99272880: 'Rahim Kienhuis', 59887191: 'Sezen Kivits', 62701040: 'Ylse Klarenbeek', 58040377: 'Adil Klop', 16097870: 'Danique Knibbe', 43689934: 'George Knuiman', 10792879: 'Evelyn Koelemij', 43680781: 'Djura Kol', 48601268: 'Matz Koning', 75997788: 'Nuriye Kooijmans', 88855695: 'Thijn Kooyman', 81155296: 'Yee Koppers', 47260040: 'Eveline Kops', 86291592: 'Titia Korbee', 27241113: 'Djuri Korpershoek', 13798030: 'Gineke Korte', 51542218: 'Sharen Kortlever', 87900893: 'Remon Kost', 96118484: 'Cherissa Koudijs', 21677389: 'Fynn Krabbe', 34588570: 'Nikie Kreijkes', 1695839: 'Do?ukan Krikke', 247918: 'Corry Kroonen', 38329455: 'Ngoc Kropman', 22699561: 'Vincent Kros', 54026378: 'Resul Kuijpers', 97417002: 'Machteld Kwantes', 79366078: 'Esperanza Kwee', 78735049: 'Nadeem Lagendijk', 14303208: 'Christianus Laman', 31897288: 'Mathyn Lamme', 23547619: 'Buck Lantinga', 11068043: 'Hanan Lathouwers', 29526540: 'Mouna Lathouwers', 79937969: 'Yvan Lau', 62613937: 'Seyed Laurijssen', 47477884: 'Mellisa Leemburg', 36527838: 'Rein Leidelmeijer', 3233378: 'Bjorn Leijen', 25994016: 'Jory Leijenaar', 44868097: 'Haroun Lemaire', 77960666: 'Nadia Lems', 40434933: 'Sanne Lentz', 13911001: 'Federico Levels', 88596522: 'Chi Liebregts', 74361881: 'Maurice Lima', 1696500: 'Hetty Lindhout', 16912993: 'Dingenus Loeffen', 76802764: 'Wannes Lohuis', 56872729: 'Malcolm Looij', 21095566: 'Fredrika Lopez', 77306636: 'Sherwin Lugthart', 63634350: 'Yi Luten', 97838175: 'Mathe Luth', 51186803: 'Pim Machielsen', 58522654: 'Valery Majoor', 42115591: 'Dorenda Malestein', 55480737: 'Noelle Melis', 44391517: 'Noud Menke', 24613625: 'Bodie Metselaar', 86000192: 'Miquel Metzelaar', 68409833: 'Roan Meulmeester', 72683344: 'Myron Middel', 99283252: 'Maron Miedema', 4783858: 'Marcellus Mijnheer', 75623387: 'Eyup Milder', 27925117: 'Oliver Milder', 56749879: 'Jo-Anne Modderkolk', 72577292: 'Jorren Modderkolk', 53585410: 'Lisse Moes', 26857113: 'Antonetta Moeskops', 84110134: 'Lamia Mok', 44671041: 'Sonny Mol', 54310617: 'Shannon Mullenders', 10872825: 'Doetje Munsters', 64418623: 'Callista Mutsaers', 63096281: 'Claudine Nagel', 70336464: 'Fauve Neve', 4697362: 'Randell Nieman', 1137946: 'Jurrit Nieuwenhuizen', 67817269: 'Inas Niezen', 51650744: 'Vesna Nijs', 72586808: 'Harry Noordhuis', 46570285: 'Juliet Noordzij', 88519892: 'Henricus Noot', 13092455: 'Inger Notermans', 61060652: 'Geurt Nuiten', 40141996: 'Lee Numan', 30658799: 'Rieke Odijk', 90067329: 'Seb Okkerse', 86180471: 'Steijn Ooijen', 13116738: 'Rins Oosterbeek', 13210212: 'Lilly Oosterbroek', 22731474: 'Romaisa Oostvogels', 17575088: 'Casimir Overbeeke', 30195935: 'Shakir Paauwe', 75664412: 'Redouane Paijmans', 79888156: 'Loulou Panman', 3407554: 'Farah Pastoor', 34765676: 'Vincentius Pater', 1665980: 'Solane Paulissen', 96104167: 'Xander Peijs', 75680261: 'Heba Pelders', 23798155: 'Luca Pereira', 58866007: 'Ilana Philippi', 20883994: 'Kaoutar Philips', 5976174: 'Romy Piek', 85284256: 'Wijntje Plaizier', 47605891: 'Giedo Planken', 2416751: 'Nathanael Plasman', 77240949: 'Matthijs Pleiter', 31247305: 'Zahir Poepjes', 58253841: 'Gustaaf Poldervaart', 72665524: 'Rafaela Polfliet', 34872117: 'Stephano Popma', 36903574: 'Timo Postuma', 64947290: 'Desiree Potgieter', 27950803: 'Aart Pothuizen', 85236626: 'Mink Pothuizen', 123355: 'Genesis Potman', 27805666: 'Hendrik-Jan Prevoo', 3883025: 'Annigje Prinssen', 82412626: 'Javier Pruijmboom', 37110913: 'Andre Putters', 61611295: 'Luciana Putters', 32044893: 'Semiha Quik', 38296757: 'Haiko Raaijmakers', 25077484: 'Erdal Ramcharan', 20618153: 'Adisa Reek', 4353500: 'Jarik Regeling', 29474737: 'Romello Reintjes', 25557516: 'Nadir Remijn', 23215240: 'Taeke Renes', 3474870: 'Cheyenna Reuvekamp', 58699305: 'Leonie Richardson', 37279234: 'Abdeslam Ridderhof', 62105897: 'Kimm Rienks', 27123462: 'Lorraine Rijkens', 41527759: 'Karam Rinkel', 7308727: 'Fatime Rodenburg', 18144425: 'Yarah Roest', 22168693: 'Tori Roeterdink', 60352393: 'Shan Rokx', 65408517: 'Krijntje Rombout', 76123484: 'Karolina Roodbeen', 43902015: 'Ziya Rooijmans', 72547110: 'Jennie Roozendaal', 72526473: 'Jake Rosenbrand', 88176729: 'Roma Rotgans', 40343779: 'Tevfik Rothuizen', 17222374: 'Sivar Rottier', 92665222: 'Eleanora Rovers', 19662602: 'Jannette Rust', 76393508: 'Tea Rutte', 52552718: 'Angelica Sarikaya', 48357272: 'Imran Scheffers', 80188025: 'Albertine Schellevis', 73302736: 'Minoesch Scheltema', 94955328: 'Jackson Scherpenzeel', 33252501: 'Xiao Schijvenaars', 12091019: 'Elbertha Schoneveld', 72652638: 'Jaiden Schoonderwoerd', 90296821: 'Nassira Schoutens', 14179347: 'Arif Schrader', 44901052: 'Emrah Schrama', 4709948: 'Silvy Schrauwen', 64246605: 'Thom Schuiling', 58469172: 'Levien Selten', 34173695: 'Marianka Selten', 83443653: 'Michel Sieben', 35330349: 'Enes Siemonsma', 73236988: 'Patricia Sier', 68601184: 'Christiana Siero', 40633534: 'Servet Sijmons', 14072826: 'Saif Sikking', 64228258: 'Jimi Sips', 92977271: 'Noa Slangen', 80998260: 'Xanne Slob', 9287708: 'Rachell Smallegange', 19858730: 'Shaya Snelder', 57419039: 'Dolf Snippe', 77392404: 'Marck Soekhai', 91527663: 'Logan Sonnemans', 76924297: 'Marrit Speelman', 42297781: 'Kenan Spronck', 37804282: 'Ya Steeman', 26207525: 'Sharief Stegink', 79167252: 'Olaf Sterenberg', 55412918: 'Wichard Stienen', 74182182: 'Tom Stokkel', 64554442: 'Franke Stoppels', 17823206: 'Kamil Streefland', 39905995: 'Gonca Stroo', 56121590: 'Franklin Stuurman', 4921119: 'Chaimae Swiers', 83415514: "Christoffel 't Jong", 47982619: "Jorg 't Lam", 89985072: 'Nermin Talhaoui', 39659121: 'Elbertus Tamis', 88263855: 'Olof Tap', 95631564: 'Sanja Tas', 49631542: 'Skye Tas', 83266686: 'Nanette te Braak', 37399898: 'Xiao Teekens', 20331158: 'Maan ten Pas', 94686490: 'Tjalle ten Pas', 4568018: 'Pleun ter Heide', 82854435: 'Aboubakr Terpstra', 64053722: 'Arianna Tettero', 53202517: 'Jonah Teuben', 34262212: 'Rochelle Thielen', 57595888: 'Silvie Thoma', 21964491: 'Ard Tielemans', 36213792: 'Raja Tijhof', 19058315: 'Bilal Tip', 14591033: 'Sarena Tjeerdsma', 66034145: 'Hedwich Toetenel', 24875739: 'Samentha Toren', 83869542: 'Liza Traa', 9067939: 'Tom Truijen', 82390428: 'Jacey Tun', 78544592: 'Annamaria Twigt', 57701414: 'Arina Ubbink', 42171678: 'Emme Udo', 43027916: 'Felien Uitslag', 14816774: 'Keely Ursem', 14309255: 'Nygel Vaatstra', 20830477: 'Dineke Valster', 24167153: 'Shairon van Aaken', 63408522: 'Said van Aalderen', 97019450: 'Cherilyn van Amelsvoort', 73196865: 'Leo van Amerongen', 65318664: 'Peter-Jan van Amersfoort', 28055464: 'Jacky van Apeldoorn', 87830198: 'Nika van Baaren', 90474003: 'Cemil van Barneveld', 81022997: 'Johannus van Bavel', 21070547: 'Lody van Bentem', 99975346: 'Ynte van Berkom', 28357474: 'Liedeke van Bezooijen', 75759231: 'Emircan van de Bunt', 70193386: 'Robbie van de Geijn', 63111000: 'Patryk van de Kraats', 81116418: 'Kamila van de Kruijs', 27187154: 'Rayen van de Kruijs', 32183908: 'Roswitha van de Kuilen', 31306819: 'Rudy van de Pavert', 42196732: 'Shawny van de Pol', 6913074: 'Leida van de Ridder', 66120270: 'Jurre van de Sanden', 61518436: 'Paulette van de Wardt', 67625383: 'Nanke van den Berg', 97371272: 'Btissam van den Boer', 32204977: 'Enrique van den Born', 81218347: 'Cyrano van den Eijnde', 8464817: 'Ceren van den Engel', 51791169: 'Cyrille van den Ham', 55530367: 'Leon van den Hoogen', 79858178: 'Amos van den Oord', 57086672: 'Chelly van der Doelen', 55103073: 'Tamar van der Drift', 15187217: 'Lakshmi van der Gaag', 51566595: 'Deejay van der Geer', 41489515: 'Ferhan van der Gulik', 77896638: 'Daisy van der Klei', 59111489: 'Pearl van der Leek', 51509565: 'Aynel van der Marel', 23983476: 'Agelo van der Meer', 64600457: 'Abdul van der Meeren', 60312776: 'Geerte van der Meij', 41578612: 'Maritha van der Niet', 22288615: 'Johannes van der Plaats', 32705005: 'Graciella van der Plas', 23391676: 'Darian van der Steege', 23628642: 'Tos van der Ster', 94687383: 'Scotty van der Stoel', 8557857: 'Yun van der Vleuten', 48678993: 'Josef van der Wiel', 6723948: 'Jos van der Zwet', 5739011: 'George van Dieten', 11593163: 'Ilayda van Dinther', 55474917: 'Naciye van Eert', 13996448: 'Jayme van Eeuwijk', 42406214: 'Juan van Eijndhoven', 82688900: 'Wytse van Geest', 76661016: 'Carmela van Gerwen', 5595824: 'Joshi van Groeningen', 37744525: 'Ouidad van Hall', 69086548: 'Walther van Halteren', 88627897: 'Tamimount van Herten', 63955238: 'Shauny van Hezik', 76648468: 'Nalinie van Ierland', 3707829: 'Berit van Ingen', 80135353: 'Aidan van Iwaarden', 25330192: 'Ciske van Kalsbeek', 45915482: 'Ycel van Kasteel', 75446434: 'Romany van Kessel', 79617364: 'Demelza van Kommer', 68286356: 'Seval van Leussen', 28618400: 'Ruveyda van Lingen', 68360259: 'Touraya van Lingen', 26406342: 'Harwin van Loon', 39459642: 'Lammigje van Loveren', 56544130: 'Fae van Luttikhuizen', 78821918: 'Micha van Maarseveen', 34243356: 'Meta van Marle', 88752563: 'Leon van Maurik', 89180944: 'Abram van Mierlo', 59753700: 'Ans van Montfort', 33877725: 'Yuri van Mourik', 90103047: 'Yang van Munster', 12170832: 'Miguel van Oss', 2550487: 'Nanet van Osta', 11741347: 'Sien van Plateringen', 21029457: 'Fedoua van Poorten', 70878567: 'Jetty van Putten', 20374340: 'Jersey van Ravesteijn', 58592894: 'Jodi van Riel', 79879876: 'Cleo van Rietschoten', 7386961: 'Caressa van Roemburg', 26172512: 'El van Rosmalen', 58736785: 'Georgia van Rossem', 34110913: 'Dragana van Ruitenbeek', 37498675: 'Borre van Ruler', 16333449: 'Marilene van Santen', 9332762: 'Sanne van Sleeuwen', 10698627: 'Dalila van Sommeren', 11996292: 'Elske van Suijlekom', 47462856: "Samah van 't Oever", 96453361: 'Julot van Teeffelen', 46989508: 'Enrico van Triest', 83210352: 'Tarik van Vloten', 29640619: 'Priscillia van Voorden', 56191333: 'Anne-Jan van Waardenburg', 37701751: 'Maggy van Walsum', 65675896: 'Maran van Wanrooij', 89338938: 'Renco van Weel', 35315956: 'Hazel van Wensen', 32595335: 'Sanna van Wiggen', 14138904: 'Hui van Zeijl', 41153310: 'Jorian van Zijderveld', 64768422: 'Anthonius van Zoelen', 66570705: 'Christiaan van Zon', 48198668: 'Neele Veeke', 61443567: 'Bobby Veldhuis', 17092717: 'Vinod Velt', 91250534: 'Nadja Vendel', 88636924: 'Solomon Verhorst', 5085194: 'Yuki Verkuijl', 23565001: 'Chloe Vermanen', 97136582: 'Talha Vermeeren', 70072978: 'Maureen Versantvoort', 22323043: 'Kavish Versteeg', 12430748: 'Sherman Vervaart', 98105190: 'Karim Vingerhoets', 73980360: 'Jiri Vinke', 73350019: 'Kamiel Vinken', 95007221: 'Arnela Visch', 13658563: 'Tjesse Voesten', 62363761: 'Edwinus Voigt', 31194811: 'Nadien Volman', 5892092: 'Annemarie Vooijs', 78443067: 'Dax Voskuilen', 9731271: 'Jort Vries', 34806836: 'Rhona Vromans', 53775014: 'Zhen Vullings', 44828429: 'Laurent Wallenburg', 15051051: 'Vasco Waninge', 65960683: 'Reduan Warsame', 37770881: 'Matisse Weij', 25106480: 'Jos Welling', 56988998: 'Evelina Wensing', 28957789: 'Djamilla Wesselink', 58074656: 'Eyup Wesselman', 53107172: 'Harke Wester', 2079771: 'Yunus Westera', 61520025: 'Keshia Westgeest', 12782624: 'Mies Westra', 84449005: 'Maryam Wiegmans', 19717077: 'Maris Wielenga', 72796858: 'Filipe Wiersema', 39429093: 'Vigo Wijers', 48503689: 'Heiltje Wijnands', 24277163: 'Marck Wijngaarden', 72456780: 'Alexandra Wijnsma', 51052738: 'Ihsane Wind', 23652927: 'Yuna Winkelaar', 30050930: 'Jacko Wobbes', 75521763: 'Aya Woertman', 28358060: 'Sayfeddine Wolswijk', 33672995: 'Frederikus Wullink', 52715680: 'Gabriella Yazici', 10609762: 'Vanita Yusuf', 94930277: 'Juno Zaaijer', 39230359: 'Fransiscus Zagers', 23658570: 'Mellanie Zhang', 14847953: 'Malte Zondag', 98780382: 'Marise Zonneveld', 59289233: 'Chico Zwarts', 21311067: 'Stein Zweekhorst'}

        self.schedule = schedule



        self.represent_schedule()

        # configure window
        self.title("Scheduly")
        self.geometry(f"{1340}x{790}")

        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Run initializing methods
        self.create_sidebar()
        self.create_frames()


    """ Init """

    def __init_student_convert_dict(student_list) -> dict:
        student_convert_dict = {}
        for student in student_list:
            student_convert_dict[student.id] = student.name
        return student_convert_dict


    def represent_schedule(self):

        self.student_dict = self.__init_student_schedule(schedule)
        self.course_dict = self.__init_course_schedule(schedule)
        self.room_dict = self.__init_room_schedule(schedule)


    def __init_student_schedule(self, schedule) -> dict:

        student_dict = {}

        for course in schedule:

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                for student_id in schedule[course][_class]['students']:

                    student_name = self.get_student_name(student_id)

                    if student_name not in student_dict:
                        student_dict[student_name] = {}
                    if course not in student_dict[student_name]:
                        student_dict[student_name][course] = []

                    class_data = (_class, timeslot['day'], timeslot['timeslot'], timeslot['room'])

                    student_dict[student_name][course].append(class_data)

        return student_dict

    def __init_course_schedule(self, schedule) -> dict:

        course_dict = {}

        for course in schedule :
            if course == "No course":
                continue

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                if course not in course_dict:
                    course_dict[course] = {}

                course_dict[course][_class] = []

                class_data = (timeslot['day'], timeslot['timeslot'], timeslot['room'])

                course_dict[course][_class].append(class_data)

        return course_dict

    def __init_room_schedule(self, schedule) -> dict:

        room_dict = {}

        for course in schedule:

            for _class in schedule[course]:

                timeslot = schedule[course][_class]

                if timeslot['room'] not in room_dict:
                    room_dict[timeslot['room']] = []

                class_data = (course, _class, timeslot['day'], timeslot['timeslot'])

                room_dict[timeslot['room']].append(class_data)

        return room_dict

    def create_sidebar(self):

        # Frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # Text
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Schedule Selector", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        # Buttons
        self.student_button = customtkinter.CTkButton(self.sidebar_frame, text="Student", command=self.show_student_frame)
        self.student_button.grid(row=1, column=0, padx=20, pady=20)
        self.course_button = customtkinter.CTkButton(self.sidebar_frame, text="Course", command=self.show_course_frame)
        self.course_button.grid(row=2, column=0, padx=20, pady=20)
        self.room_button = customtkinter.CTkButton(self.sidebar_frame, text="Room", command=self.show_room_frame)
        self.room_button.grid(row=3, column=0, padx=20, pady=20)

        # Export
        self.export_button= customtkinter.CTkButton(self.sidebar_frame, text="Export", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export)
        self.export_button.grid(row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Export All
        self.export_all_button= customtkinter.CTkButton(self.sidebar_frame, text="Export All", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.export)
        self.export_all_button.grid(row=8, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def create_frames(self):

        # Create student frame
        self.student_frame = customtkinter.CTkFrame(self, width=200, corner_radius=10)
        self.student_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.student_frame.grid_columnconfigure(0, weight=1)
        self.student_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        self.frame_student_content()


        # Create course frame
        self.course_frame = customtkinter.CTkFrame(self, width=200, height=200, corner_radius=10)
        self.course_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.course_frame.grid_columnconfigure(0, weight=1)
        self.course_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        self.frame_course_content()

        # Create room frame
        self.room_frame = customtkinter.CTkFrame(self, width=200, height=200, corner_radius=10)
        self.room_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        self.room_frame.grid_columnconfigure(0, weight=1)
        self.room_frame.grid_rowconfigure((1,2,3,4,5,6), weight=1)

        self.frame_room_content()


    def frame_student_content(self):

        # Search Frame
        self.student_search_frame = customtkinter.CTkFrame(self.student_frame, corner_radius=10)
        self.student_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.student_search_frame.grid_rowconfigure((0), weight=1)
        self.student_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Student option
        self.student_option = customtkinter.CTkOptionMenu(self.student_search_frame,
                                                values=[student for student in self.student_dict])
        self.student_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.student_option.set('Student')

        # Student Add Button
        self.student_add_button = customtkinter.CTkButton(self.student_search_frame, text="Search", command=self.student_button_click)
        self.student_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Student Roster
        self.student_schedule = customtkinter.CTkFrame(self.student_frame, corner_radius=10)
        self.student_schedule.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.student_schedule.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.student_schedule.grid_rowconfigure((0,1,2,3,4), weight=1)

    def frame_course_content(self):

        # Search Frame
        self.course_search_frame = customtkinter.CTkFrame(self.course_frame, corner_radius=10)
        self.course_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.course_search_frame.grid_rowconfigure(0, weight=1)
        self.course_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Course option
        self.course_option = customtkinter.CTkOptionMenu(self.course_search_frame,
                                                values=[course for course in self.course_dict])
        self.course_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.course_option.set('Course')

        # Course Add Button
        self.course_add_button = customtkinter.CTkButton(self.course_search_frame, text="Search", command=self.course_button_click)
        self.course_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Course Roster
        self.course_schedule = customtkinter.CTkFrame(self.course_frame, corner_radius=10)
        self.course_schedule.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.course_schedule.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.course_schedule.grid_rowconfigure((0,1,2,3,4), weight=1)

    def frame_room_content(self):

        # Search Frame
        self.room_search_frame = customtkinter.CTkFrame(self.room_frame, corner_radius=10)
        self.room_search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.room_search_frame.grid_rowconfigure(0, weight=1)
        self.room_search_frame.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)

        # Room option
        self.room_option = customtkinter.CTkOptionMenu(self.room_search_frame,
                                                values=[room for room in self.room_dict])
        self.room_option.grid(row=0, column=0, columnspan=7, padx=20, pady=20, sticky="ew")
        self.room_option.set('Room')

        # Room Add Button
        self.room_add_button = customtkinter.CTkButton(self.room_search_frame, text="Search", command=self.room_button_click)
        self.room_add_button.grid(row=0, column=7, columnspan=2, padx=20, pady=20, sticky="ew")

        # Room Roster
        self.room_schedule = customtkinter.CTkFrame(self.room_frame, corner_radius=10)
        self.room_schedule.grid(row=1, column=0, rowspan=6, padx=20, pady=20, sticky="nsew")
        self.room_schedule.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.room_schedule.grid_rowconfigure((0,1,2,3,4), weight=1)

    """ Get """

    def get_student_name(self, id):
        return self.student_convert_dict.get(id)

    """ Methods """

    def show_student_frame(self):
        self.student_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.student_schedule.winfo_children():
            widget.destroy()

        self.student_option.set('Student')

    def show_course_frame(self):
        self.course_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.course_schedule.winfo_children():
            widget.destroy()

        self.course_option.set('Course')

    def show_room_frame(self):
        self.room_frame.tkraise()

        # Destroy any prior schedule
        for widget in self.room_schedule.winfo_children():
            widget.destroy()

        self.room_option.set('Room')


    def student_button_click(self):

        student = None
        while student == None:
            student = self.student_option.get()

        frame = self.student_schedule
        print(student)
        self.fill_grid(frame, 'student', student)

    def course_button_click(self):

        course = None
        while course == None:
            course = self.course_option.get()

        frame = self.course_schedule

        self.fill_grid(frame, 'course', course)

    def room_button_click(self):

        room = None
        while room == None:
            room = self.room_option.get()

        frame = self.room_schedule

        self.fill_grid(frame, 'room', room)


    def create_grid(self, frame):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        timeslots = ["9-11", "11-13", "13-15", "15-17", "17-19"]
        timeslot_to_num = {9:0, 11:1, 13:2, 15:3, 17:4}

        for i, day in enumerate(days):
            self.day_label = customtkinter.CTkLabel(master=frame, text=day, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.day_label.grid(row=0, column=i+1, padx=5, pady=10, sticky='nsew')

        for i, timeslot in enumerate(timeslots):
            self.time_label = customtkinter.CTkLabel(master=frame, text=timeslot, font=customtkinter.CTkFont(size=15, weight="bold"))
            self.time_label.grid(row=i+1, column=0, padx=10, pady=5, sticky='nsew')

        return days, timeslot_to_num

    def fill_grid(self, frame, search_type, key):

        days, timeslot_to_num = self.create_grid(frame)

        if search_type == 'student':
            schedule_dict = self.student_dict
        elif search_type == 'course':
            schedule_dict = self.course_dict
        elif search_type == 'room':
            schedule_dict = self.room_dict

        for schedule_object in schedule_dict[key]:
            if type(schedule_object) == tuple:
                course, _class, day, timeslot = schedule_object
            else:
                for class_data in schedule_dict[key][schedule_object]:
                    if len(class_data) == 4:
                        course = schedule_object
                        _class, day, timeslot, room = class_data
                    elif len(class_data) == 3:
                        _class = schedule_object
                        day, timeslot, room = class_data

            row = timeslot_to_num[timeslot]
            col = days.index(day)

            if search_type == 'student':
                self._class = customtkinter.CTkLabel(master=frame, text=f"{course}\n{_class}\n{room}")
            elif search_type == 'course':
                self._class = customtkinter.CTkLabel(master=frame, text=f"{_class}\n{room}")
            else:
                self._class = customtkinter.CTkLabel(master=frame, text=f"{course}\n{_class}")

            self._class.grid(row=row+1, column=col+1, sticky='nsew')



    def run(self) -> None:
        self.mainloop()

    def export(self):
        pass

if __name__ == "__main__":
    app = App()
    app.mainloop()