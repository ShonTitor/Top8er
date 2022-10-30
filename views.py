from .forms import makeform
from .utils import graphic_from_request, hestia, response_from_json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class salu2(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            img = graphic_from_request(request, request.POST['game'], hasextra=False, icon_sizes=(64, 32), default_bg="bg")
            return Response({
                "base64_img": img
                })
        except Exception as e:
            return Response({"jaja": "salu2", "error": str(e)})

def index(request) :
    FormClass = makeform()
    c_guide = "https://www.ssbwiki.com/Alternate_costume_(SSBU)"
    return hestia(request, "ssbu", FormClass, color_guide=c_guide)

def roa(request) :
    c = ["Random", "Absa", "Clairen", "Elliana", "Etalus",
         "Forsburn", "Hodan", "Kragg", "Maypul", "Mollo", "Olympia", "Orcane",
         "Ori and Sein", "Pomme", "Ranno", "Shovel Knight",
         "Sylvanos", "Wrastor", "Zetterburn"]
    ec = ["Random", "Absa", "Clairen", "Elliana", "Etalus",
         "Forsburn", "Kragg", "Maypul", "Orcane",
         "Ori and Sein", "Ranno", "Shovel Knight",
         "Sylvanos", "Wrastor", "Zetterburn"]
    FormClass = makeform(chars=c, numerito=21, numerito_extra=1, echars=c,
                        color1="#B4A5E6", color2="#261C50")
    return hestia(request, "roa", FormClass)

def sg(request) :
    c = ['Annie', 'Beowulf', 'Big Band', 'Cerebella', 'Double', 'Eliza',
         'Filia', 'Fukua', 'Ms Fortune', 'Painwheel', 'Parasoul',
         'Peacock', 'Robo Fortune', 'Squigly', 'Valentine']
    FormClass = makeform(chars=c, numerito=30, numerito_extra=1,
                         color1="#FF544A", color2="#E6DEBB")
    c_guide = "https://wiki.gbl.gg/w/Skullgirls"
    return hestia(request, "sg", FormClass, color_guide=c_guide)

def rr(request) :
    c = ["Afi and Galu", "Ashani", "Ezzie", "Kidd",
         "Raymer", "Seth", "Urdah", "Velora", "Weishan", "Zhurong"]
    FormClass = makeform(chars=c, numerito=1, numerito_extra=1,
                         color1="#384BCB", color2="#40EB8F")
    return hestia(request, "rr", FormClass, icon_sizes=(80,50))

def melee(request) :
    c = ['Random', 'Bowser', 'Captain Falcon', 'Donkey Kong', 'Dr Mario', 'Falco',
         'Fox', 'Ganondorf', 'Ice Climbers', 'Jigglypuff', 'Kirby', 'Link',
         'Luigi', 'Mario', 'Marth', 'Mewtwo', 'Mr Game & Watch', 'Ness',
         'Peach', 'Pichu', 'Pikachu', 'Roy', 'Samus', 'Sheik', 'Yoshi',
         'Young Link', 'Zelda']
    FormClass = makeform(chars=c, numerito=6)
    c_guide = "https://www.ssbwiki.com/Alternate_costume_(SSBM)"
    return hestia(request, "melee", FormClass, icon_sizes=(48,24))

def ggxx(request) :
    c = ['A.B.A', 'Anji Mito', 'Axl Low', 'Baiken', 'Bridget', 'Chipp Zanuff',
         'Dizzy', 'Eddie', 'Faust', 'I-No', 'Jam Kuradoberi', 'Johnny',
         'Justice', 'Kliff Undersn', 'Ky Kiske', 'May', 'Millia Rage',
         'Order-Sol', 'Potemkin', 'Robo-Ky', 'Slayer', 'Sol Badguy',
         'Testament', 'Venom', 'Zappa']
    FormClass = makeform(chars=c, numerito=22, hasextra=False,
                         color1="#EF0020", color2="#16E7DE")
    c_guide = "https://www.dustloop.com/wiki/index.php?title=Guilty_Gear_XX_Accent_Core_Plus_R"
    return hestia(request, "ggxx", FormClass, color_guide=c_guide, hasextra=False)

def ggxrd(request) :
    c = ['Answer', 'Axl', 'Baiken', 'Bedman', 'Chipp', 'Dizzy', 'Elphelt', 'Faust', 'I-No', 
        'Jack-O', 'Jam', 'Johnny', 'Kum Haehyun', 'Ky', 'Leo', 'May', 'Millia', 'Potemkim', 
        'Ramlethal', 'Raven', 'Sin', 'Slayer', 'Sol', 'Venom', 'Zato'] 
    FormClass = makeform(chars=c, numerito=2, hasextra=False,
                         color1="#3a6446", color2="#09ed7a")
    return hestia(request, "ggxrd", FormClass, hasextra=False)

def ggst(request) :
    c = ['Anji', 'Axl', 'Baiken', 'Bridget', 'Chipp', 'Faust', 'Giovanna', 'Goldlewis', 'Happy Chaos',
         'I-No', 'Jack-O\'', 'Ky', 'Leo', 'May', 'Millia',
         'Nagoriyuki', 'Potemkim', 'Ramlethal', 'Sol', 'Testament', 'Zato'] 
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#5e0a00", color2="#000000")
    return hestia(request, "ggst", FormClass, hasextra=False)

def uni(request) :
    c = ['Akatsuki', 'Byakuya', 'Carmine', 'Chaos', 'Eltnum', 'Enkidu',
         'Gordeau', 'Hilda', 'Hyde', 'Linne', 'Londrekia', 'Merkava',
         'Mika', 'Nanase', 'Orie', 'Phonon', 'Seth', 'Vatista', 'Wagner',
         'Waldstein', 'Yuzuriha']
    FormClass = makeform(chars=c, numerito=42, numerito_extra=1,
                         color1="#32145a", color2="#c814ff")
    c_guide = "https://wiki.gbl.gg/w/Under_Night_In-Birth/UNICLR"
    return hestia(request, "uni", FormClass, color_guide=c_guide)

def efz(request) :
    c = ['Akane', 'Akiko', 'Ayu', 'Doppel', 'Ikumi', 'Kanna', 'Kano',
         'Kaori', 'Mai', 'Makoto', 'Mayu', 'Minagi', 'Mio', 'Misaki',
         'Mishio', 'Misuzu', 'Mizuka', 'Nayuki (asleep)', 'Nayuki (awake)',
         'Rumi', 'Sayuri', 'Shiori', 'UNKNOWN']
    FormClass = makeform(chars=c, numerito=8, hasextra=False,
                         color1="#24358a", color2="#9dcae9",
                          efz=True)
    c_guide = "https://wiki.gbl.gg/w/Eternal_Fighter_Zero"
    return hestia(request, "efz", FormClass, color_guide=c_guide,
                  hasextra=False)

def mbaacc(request) :
    c = ['Akiha', 'Aoko', 'Arcueid', 'Ciel', 'Hime', 'Hisui',
         'Koha-Mech', 'Kohaku', 'Kouma', 'Len', 'Maids', 'Mech-Hisui',
         'Miyako', 'NAC', 'Nanaya', 'Neco-Arc', 'Neco-Mech', 'Nero',
         'Powerd Ciel', 'Red Arcueid', 'Riesbyfe', 'Roa', 'Ryougi',
         'Satsuki', 'Seifuku', 'Sion', 'Tohno', 'V.Akiha', 'V.Sion',
         'Warachia', 'White Len']
    ec = ["Crescent", "Full", "Half"]
    FormClass = makeform(chars=c, echars=ec, mb=True,
                         numerito=37, numerito_extra=1,
                         color1="#171a45", color2="#440206")
    c_guide = "https://wiki.gbl.gg/w/Melty_Blood/MBAACC"
    return hestia(request, "mbaacc", FormClass,
                  color_guide=c_guide, hasextra=True)

def soku(request) :
    c = ['alice', 'aya', 'cirno', 'iku', 'komachi', 'marisa', 'meiling',
         'patchouli', 'reimu', 'reisen', 'remilia', 'sakuya', 'sanae',
         'suika', 'suwako', 'tenshi', 'utsuho', 'youmu', 'yukari', 'yuyuko']
    FormClass = makeform(chars=c, numerito=1, color1='#28516a', color2='#51a3d5')
    return hestia(request, "soku", FormClass)

def slapcity(request) :
    c = ['Asha', 'Business Casual Man', 'Frallan', 'Goddess of Explosions', 'Ittle Dew',
         'Jenny Fox', 'Masked Ruby', 'Princess Remedy', 'Ultra Fishbunjin 3000']
    FormClass = makeform(chars=c, numerito=24, hasextra=False,
                         color1="#ff7100", color2='#25d0fb')
    c_guide = "https://slapwiki.com/SlapWiki/"
    return hestia(request, "slapcity", FormClass, color_guide=c_guide, hasextra=False)

def dfci(request) :
    c = ['Akira Yuki', 'Ako Tamaki', 'Asuna', 'Emi Yusa', 'Kirino Kousaka',
         'Kirito', 'Kuroko Shirai', 'Kuroyukihime', 'Mikoto Misaka',
         'Miyuki Shiba', 'Qwenthur Barbotage', 'Rentaro Satomi',
         'Selvaria Bles', 'Shana', 'Shizuo Heiwajima', 'Taiga Aisaka',
         'Tatsuya Shiba', 'Tomoka Minato', 'Yukina Himeragi', 'Yuuki Konno']
    ec = ['Accelerator', 'Alicia', 'Boogiepop', 'Celty', 'Dokuro', 'Enju',
             'Erio', 'Froleytia', 'Haruyuki', 'Holo', 'Innocent Charm',
             'Iriya', 'Izaya', 'Kino', 'Kojou', 'Kouko', 'Kuroneko',
             'Leafa', 'LLENN', 'Mashiro', 'Miyuki', 'Pai', 'Rusian',
             'Ryuuji', 'Sadao', 'Tatsuya', 'Tomo', 'Touma', 'Uiharu',
             'Wilhelmina', 'Zero']
    FormClass = makeform(chars=c, echars=ec, mb=True,
                         numerito=25, numerito_extra=1,
                         color1="#1919c8", color2="#c81919")
    c_guide = "https://wiki.gbl.gg/w/Dengeki_Bunko:_Fighting_Climax/DFCI"
    return hestia(request, "dfci", FormClass,
                  color_guide=c_guide, hasextra=True)

def tla(request) :
    c = ['Beef', 'Garlic', 'Noodle', 'Onion', 'Pork', 'Rice']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#753c7c", color2='#ea79f8')
    return hestia(request, "tla", FormClass, hasextra=False)

def svs(request) :
    c = ['Earth', 'Erile', 'Hiro', 'Hiro2', 'Jadou', 'Jadou2',
         'Krayce', 'Mayura', 'Orochimaru', 'Roze', 'Ryuken', 'Welles']
    FormClass = makeform(chars=c, numerito=6, hasextra=False,
                         color1="#233f91", color2='#e4c149')
    return hestia(request, "svs", FormClass, hasextra=False)

def sf3s(request) :
    c = ['Akuma', 'Alex', 'Chun-Li', 'Dudley', 'Elena', 'Hugo',
         'Ibuki', 'Ken', 'Makoto', 'Necro', 'Oro', 'Q', 'Remy', 'Ryu',
         'Sean', 'Twelve', 'Urien', 'Yang', 'Yun']
    FormClass = makeform(chars=c, numerito=14, hasextra=False,
                         color1="#c83c14", color2='#ef8f17')
    c_guide = "https://www.zytor.com/~johannax/jigsaw/sf/3s.html"
    return hestia(request, "3s", FormClass, hasextra=False,
                  color_guide=c_guide)

def sfst(request) :
    c = ['Blanka', 'Boxer', 'Cammy', 'Chun Li', 'Claw', 'Dee Jay',
         'Dhalsim', 'Dictator', 'E.Honda', 'Fei Long', 'Guile', 'Ken',
         'Ryu', 'Sagat', 'T.Hawk', 'Zangief']
    FormClass = makeform(chars=c, numerito=9, hasextra=False,
                         color1="#d214a0", color2="#d8d819")
    return hestia(request, "sfst", FormClass, hasextra=False)

def AsuraBuster(request) :
    c = ['Alice', 'Alice!', 'Chen-Mao', 'Goat', 'Leon', 'Nanami', 'Rokurouta', 
         'Rose Mary', 'Sittara', 'Taros', 'Yashaou', 'Zam-B', 'Zinsuke']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#ba2315", color2="#1f0141")
    return hestia(request, "AsuraBuster", FormClass, hasextra=False)

def kf2(request) :
    c = ['Archer', 'Artist', 'Bandana Dee', 'Beam', 'Beetle', 'Bell', 'Bomb', 
         'Cutter', 'Fighter', 'Gooey', 'Hammer', 'King Dedede', 'Magolor', 'Meta Knight', 
         'Ninja', 'Parasol', 'Staff', 'Sword', 'Water', 'Whip', 'Wrestler', 'Yo-yo']
    FormClass = makeform(chars=c, numerito=3, hasextra=True,
                         color1="#1f0141", color2="#ffff11")
    return hestia(request, "kf2", FormClass, hasextra=True)

def pplus(request) :
    c = ['Bowser', 'Captain Falcon', 'Charizard', 'Dedede', 'Diddy Kong', 'Donkey Kong', 
    'Falco', 'Fox', 'Ganondorf', 'Ice Climbers', 'Ike', 'Ivysaur', 'Jigglypuff', 'Kirby', 'Knuckles',
    'Link', 'Lucario', 'Lucas', 'Luigi', 'Mario', 'Marth', 'Meta Knight', 'Mewtwo', 
    'Mr. Game and Watch', 'Ness', 'Olimar', 'Peach', 'Pikachu', 'Pit', 'ROB', 'Roy', 'Samus', 
    'Sheik', 'Snake', 'Sonic', 'Squirtle', 'Toon Link', 'Wario', 'Wolf', 'Yoshi', 'Zelda', 
    'Zero Suit Samus']
    FormClass = makeform(chars=c, numerito=18, hasextra=True,
                         color1="#0c3e48", color2="#42dbac")
    return hestia(request, "p+", FormClass, hasextra=True)

def pm(request) :
    c = ['Bowser', 'Captain Falcon', 'Charizard', 'Dedede', 'Diddy Kong', 'Donkey Kong', 
    'Falco', 'Fox', 'Ganondorf', 'Ice Climbers', 'Ike', 'Ivysaur', 'Jigglypuff', 'Kirby',
    'Link', 'Lucario', 'Lucas', 'Luigi', 'Mario', 'Marth', 'Meta Knight', 'Mewtwo', 
    'Mr. Game and Watch', 'Ness', 'Olimar', 'Peach', 'Pikachu', 'Pit', 'ROB', 'Roy', 'Samus', 
    'Sheik', 'Snake', 'Sonic', 'Squirtle', 'Toon Link', 'Wario', 'Wolf', 'Yoshi', 'Zelda', 
    'Zero Suit Samus']
    FormClass = makeform(chars=c, numerito=18, hasextra=True,
                         color1="#2f3775", color2="#ffffff")
    return hestia(request, "p+", FormClass, hasextra=True, default_bg="bg2")

def tfh(request) :
    c = ['Arizona', 'Oleander', 'Paprika', 'Pom', 'Shanty', 'Tianhuo', 'Velvet']
    FormClass = makeform(chars=c, numerito=1, hasextra=True,
                         color1="#9e003a", color2="#ffffff")
    return hestia(request, "tfh", FormClass, hasextra=True, icon_sizes=(72,50))

def wargroove(request) :
    c = ['Caesar', 'DarkMercia', 'Elodie', 'Emeric', 'Greenfinger', 'Koji', 'Mercia', 'Mercival', 
         'Nuru', 'Ragna', 'Ryota', 'Sedge', 'Sigrid', 'Tenri', 'Twins', 'Valder', 'Vesper', 'Wulfar']
    FormClass = makeform(chars=c, numerito=9, hasextra=True,
                         color1="#9e003a", color2="#ffffff")
    return hestia(request, "wargroove", FormClass, hasextra=True)

def bbtag(request) :
    c = ['Aegis', 'Akatsuki', 'Akihiko Sanada', 'Azrael', 'Blake Belladona', 'Blitztank', 
         'Carmine', 'Celica A. Mercury', 'Chie Sakonata', 'Elizabeth', 'Es', 'Gordeau', 
         'Hakumen', 'Hazama', 'Heart Aino', 'Hilda', 'Hyde', 'Iron Tager', 'Izayoi', 'Jin Kisaragi', 
         'Jubei', 'Kanji Tatsumi', 'Labrys', 'Linne', 'Mai Natsume', 'Makoto Nanaya', 'Merkava', 'Mika', 
         'Mitsuru Kirijo', 'Naoto Kurogane', 'Naoto Shirogane', 'Neo Politan', 'Nine the Phantom', 
         'Noel Vermillion', 'Nu-13', 'Orie', 'Platinum the Trinity', 'Rachel Alucard', 'Ragna the Bloodedge', 
         'Ruby Rose', 'Seth', "Susano'o", 'Teddie', 'Tohru Adachi', 'Vatista', 'Waldstein', 'Weiss Schnee', 
         'Yang Xiao Long', 'Yosuke Hanamura', 'Yu Narukami', 'Yukiko Amagi', 'Yumi', 'Yuzuriha']
    FormClass = makeform(chars=c, numerito=1, hasextra=True,
                         color1="#3250a1", color2="#f5f5be")
    return hestia(request, "bbtag", FormClass, hasextra=True, icon_sizes=(72,50))

def waku(request) :
    c = ['Arina', 'Bonus Kun', 'DandyJ', 'Fernandez', 'Mauru', 'PolitankZ', 'Rai', 'Slash', 'Tesse']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#e87ff5", color2="#eeb42e")
    return hestia(request, "waku", FormClass, hasextra=False)

def windjammers(request) :
    c = ['Hiromi Mita', 'Steve Miller', 'Jordi Costa', 'Loris Biaggi', 'Gary Scott', 'Klaus Wessel']
    FormClass = makeform(chars=c, numerito=1, hasextra=True,
                         color1="#0096ff", color2="#bdff07")
    return hestia(request, "windjammers", FormClass, hasextra=True)


def garou(request) :
    c = ['B.Jenet', 'Dong', 'Freeman', 'Gato', 'Grant', 'Griffon', 'Hokutomaru', 
         'Hotaru', 'Jae', 'Kain', 'Kevin', 'Marco', 'Rock', 'Terry']
    FormClass = makeform(chars=c, numerito=4, hasextra=False,
                         color1="#f00000", color2="#000000")
    return hestia(request, "garou", FormClass, hasextra=False)

def sfv(request) :
    c = ['Abigail', 'Akira', 'Akuma', 'Alex', 'Birdie', 'Blanka', 'Boxer', 'Cammy',
         'Chun-li', 'Claw', 'Cody', 'Dan', 'Dhalsim', 'Dictator', 'E.Honda', 'Ed', 
         'F.A.N.G', 'Falke', 'G', 'Gill', 'Guile', 'Ibuki', 'Juri', 'Kage', 'Karin', 
         'Ken', 'Kolin', 'Laura', 'Lucia', 'Luke', 'Menat', 'Nash', 'Necalli', 'Oro', 'Poison', 
         'R.Mika', 'Rashid', 'Rose', 'Ryu', 'Sagat', 'Sakura', 'Seth', 'Urien', 'Zangief', 'Zeku']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#ff4c00", color2="#ffaa00")
    return hestia(request, "sfv", FormClass, hasextra=False)

def aos2(request) :
    c = ['Alte', 'Hime', 'Iru', 'Kae', 'Kyoko', 'Mira', 'Nanako', 'Nath', 
         'Saki', 'Sham', 'Sora', 'Star Breaker', 'Suguri', 'Sumika', 'Tsih']
    FormClass = makeform(chars=c, numerito=4, hasextra=False,
                         color1="#005d98", color2="#bec8dc")
    return hestia(request, "aos2", FormClass, hasextra=False)

def gbvs(request) :
    c = ['Gran', 'Katalina', 'Charlotta', 'Lancelot', 'Percival', 'Ferry', 
         'Lowain', 'Ladiva', 'Metera', 'Zeta', 'Vaseraga', 'Beelzebub', 
         'Narmaya', 'Soriz', 'Djeeta', 'Zooey', 'Belial', 'Cagliostro', 
         'Yuel', 'Anre', 'Eustace', 'Seox', 'Vira']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#0a5a8c", color2="#a6d9ea")
    return hestia(request, "gbvs", FormClass, hasextra=False)

def amogus(request) :
    c = ['Crewmate']
    FormClass = makeform(chars=c, numerito=16, hasextra=False,
                         color1="#7a1515", color2="#FFFFFF")
    return hestia(request, "amogus", FormClass, hasextra=False)

def abk(request) :
    c = ['Adler', 'Akatsuki', 'Anonym', 'Blitztank', 'Elektrosoldat', 'Fritz', 
         'Kanae', 'Marilyn', 'Murakumo', 'Mycale', 'Perfecti', 'Sai', 'Wei']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#7a1515", color2="#FFFFFF")
    return hestia(request, "abk", FormClass, hasextra=False)

def mbtl(request) :
    c = ['Akiha Tohno', 'Aoko Aozaki', 'Arcueid Brunestud', 'Ciel', 'Dead Apostle Noel',
         'Hisui', 'Kohaku', 'Kouma Kishima', 'Maids',
         'Michael Roa Valjamjong', 'Mario Gallo Bestino', 'Mash Kyrielight',
         'Miyako Arima', 'Neco Arc', 'Noel', 'Powerd Ciel', 'Red Arcueid',
         'Saber', 'Shiki Tohno', 'Vlov Arkhangel']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#06142a", color2="#d3000b",
                         default_black_squares=False)
    return hestia(request, "mbtl", FormClass, hasextra=False)

def dankuga(request) :
    c = ['Azteca', 'Barts', 'Boggy', 'Gekkou', 'Gonzales', 'J McCoy', 
         'Kazuya', 'Lihua', 'Liza', 'Marco', 'Wulong']
    FormClass = makeform(chars=c, numerito=3, hasextra=True,
                         color1="#f60000", color2="#b7a97c")
    return hestia(request, "dankuga", FormClass, hasextra=True)

def ssv(request) :
    c = ['Amakusa', 'Basara', 'Charlotte', 'Enja', 'Gaira', 'Galford', 'Gaoh', 
         'Genjuro', 'Hanzo', 'Haohmaru', 'Jubei', 'Kazuki', 'Kusaregedo', 'Kyoshiro',
         'Mina', 'Mizuki', 'Nakoruru', 'Rasetsumaru', 'Rera', 'Rimururu', 'Shizumaru',
         'Sogetsu', 'Suija', 'Tam Tam', 'Ukyo', 'Yoshitora', 'Yunfei', 'Zankuro', 'Random']
    FormClass = makeform(chars=c, numerito=4, hasextra=True, numerito_extra=1,
                         color1="#0e0e2d", color2="#bebef0")
    return hestia(request, "ssv", FormClass, hasextra=True)

def bbcf(request) :
    c = ['Amane Nishiki', 'Arakune', 'Azrael', 'Bang Shishigami', 'Bullet', 'Carl Clover',
         'Celica A. Mercury', 'Es', 'Hakumen', 'Hazama', 'Hibiki Kohaku',
         'Iron Tager', 'Izanami', 'Izayoi', 'Jin Kisaragi', 'Jubei', 'Kagura Mutsuki', 
         'Kokonoe', 'Lambda-11', 'Litchi Faye Ling', 'Mai Natsume', 'Makoto Nanaya', 
         'Mu-12', 'Naoto Kurogane', 'Nine the Phantom', 'Noel Vermillion', 'Nu-13', 
         'Platinum the Trinity', 'Rachel Alucard', 'Ragna the Bloodedge', 'Relius Clover', 
         "Susano'o", 'Taokaka', 'Tsubaki Yayoi', 'Valkenhayn R. Hellsing', 'Yuuki Terumi']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#0055a5", color2="#aadcfa")
    return hestia(request, "bbcf", FormClass, hasextra=False)

def nasb(request) :
    c = ['Aang', "April O'Neil", 'CatDog', 'Danny Phantom', 'Helga Pataki', 'Korra', 'Leonardo',
         'Lincoln Loud', 'Lucy Loud', 'Michelangelo', 'Nigel Thornberry', 'Oblina', 'Patrick Star',
         'Powdered Toast Man', 'Ren & Stimpy', 'Reptar', 'Sandy Cheeks', 'SpongeBob SquarePants',
         'Toph Beifong', 'Zim']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#ff7b00", color2="#47b84d")
    return hestia(request, "nasb", FormClass, hasextra=False)

def vsav(request) :
    c = ['Anakaris', 'Aulbath (Rikuo)', 'Bishamon', 'Bulleta (BB Hood)', 'Demitri', 'Felicia',
         'Gallon (Jon Talbain)', 'Jedah', 'Lei-Lei (Hsien-Ko)', 'Lilith', 'Morrigan', 'Q-Bee',
         'Sasquatch', 'Victor', 'Zabel (Lord Raptor)']
    FormClass = makeform(chars=c, numerito=1, hasextra=False,
                         color1="#840c2c", color2="#000000")
    return hestia(request, "vsav", FormClass, hasextra=False)

def mvci(request) :
    c = ['Arthur', 'Black Panther', 'Black Widow', 'Captain America', 'Captain Marvel', 'Chris',
         'Chun Li', 'Dante', 'Doctor Strange', 'Dormammu', 'Firebrand', 'Frank West', 'Gamora',
         'Ghost Rider', 'Haggar', 'Hawkeye', 'Hulk', 'Iron-Man', 'Jedah', 'X', 'Monster Hunter',
         'Morrigan', 'Nemesis', 'Nova', 'Rocket Raccoon', 'Ryu', 'Sigma', 'Spencer', 'Spider-Man',
         'Strider Hiryu', 'Thanos', 'Thor', 'Ultron', 'Venom', 'Winter Soldier', 'Zero']
    ec = ['Power Stone', 'Space Stone', 'Time Stone', 'Reality Stone', 'Soul Stone', 'Mind Stone'] + c
    FormClass = makeform(chars=c, echars=ec,
                         numerito=1, numerito_extra=1,
                         color1="#ff2605", color2="#166bff")
    return hestia(request, "mvci", FormClass, hasextra=True)

def tekken7(request) :
    c = ['Akuma', 'Alisa', 'Anna', 'Armor King', 'Asuka', 'Bob', 'Bryan', 'Claudio', 'Devil Jin',
         'Dragunov', 'Eddy', 'Eliza', 'Fahkumram', 'Feng', 'Ganryu', 'Geese', 'Gigas', 'Heihachi',
         'Hwoarang', 'Jack-7', 'Jin', 'Josie', 'Julia', 'Katarina', 'Kazumi', 'Kazuya', 'King', 'Kuma',
         'Kunimitsu', 'Lars', 'Law', 'Lee', 'Lei', 'Leo', 'Leroy', 'Lidia', 'Lili', 'Lucky Chloe', 'Marduk',
         'Master Raven', 'Miguel', 'Negan', 'Nina', 'Noctis', 'Panda', 'Paul', 'Shaheen', 'Steve', 'Xiaoyu',
         'Yoshimitsu', 'Zafina']
    FormClass = makeform(chars=c, numerito=1,
                         color1="#021422", color2="#4592c6")
    return hestia(request, "tekken7", FormClass, hasextra=False)

def ssb64(request) :
    c = ['Bowser', 'C.Falcon', 'Conker', 'D.K', 'D.Samus', 'Dr.Mario', 'Falco', 'Fox', 'Ganondorf',
         'Jigglypuff', 'Kirby', 'Link', 'Lucas', 'Luigi', 'Mario', 'Marth', 'Mewtwo', 'Ness', 'Pikachu',
         'Samus', 'Wario', 'Wolf', 'Y.Link', 'Yoshi']
    FormClass = makeform(chars=c, numerito=6)
    return hestia(request, "ssb64", FormClass, hasextra=False)

def karnov(request) :
    c = ['Clown', 'Feilin', 'Jean', 'Karnov', 'Lee', 'Marstorius', 'Matlok',
         'Mizoguchi', 'Ray', 'Ryoko', 'Samchay', 'Yungmie', 'Zazie']
    FormClass = makeform(chars=c, echars=c, hasextra=True,
                         numerito=2, numerito_extra=1,
                         color1="#ff2605", color2="#166bff")
    return hestia(request, "karnov", FormClass, hasextra=True)

def tlb2(request) :
    c = ['Akari', 'Amano', 'Hibiki', 'Juzoh', 'Kaede', 'Kaede (Original)', 'Kagami', 'Kojiroh',
         'Lee', 'Moriya', 'Mukuro', 'Okina', 'Setsuna', 'Shigen', 'Washizuka', 'Yuki', 'Zantetsu']
    FormClass = makeform(chars=c, numerito=3, hasextra=False,
                         color1="#f79800", color2="#340e4f")
    return hestia(request, "tlb2", FormClass, hasextra=False)

def ssbc(request) :
    c = ['Agumon', 'Ashley', 'Black Mage', 'Bomberman', 'Bowser', 'Captain Falcon', 'Chun-Li', 'Crash', 
         'Donkey Kong', 'Dr Mario', 'Duck Hunt Dog', 'Evil Ryu', 'Falco', 'Fox', 'Ganondorf', 'Geno',
         'Goku', 'Gooey', 'Goomba', 'Heracross', 'Ice Climbers', 'Jigglypuff', 'Kirby', 'Klonoa', 'Knuckles', 
         'Krystal', 'Link (Hidden Skills)', 'Link (Items)', 'Little Mac (Crusade)', 'Little Mac (Wii U)', 
         'Lucario (Aura)', 'Lucario (Auraless)', 'Lucas', 'Luigi', 'Mach Rider', 'Mario', 'Marth (Centered)', 
         'Marth (Spread)', 'Marth (Tipper)', 'Mega Man', 'Meta Knight', 'Mewtwo', 'Mr Game & Watch (Melee)', 
         'Mr Game & Watch (Ultimate)', 'Nega Shantae', 'Ness', 'Olimar', 'Pac-Man', 'Peach', 'Petey Piranha', 
         'Phoenix Wright', 'Pichu', 'Pikachu', 'Porky', 'Rayman', 'Ridley', 'Ristar', 'ROB', 'Ryu', 'Saki', 
         'Samus', 'Shadow', 'Shantae', 'Snake', 'Snivy', 'Sonic', 'Sukapon', 'Tails', 'Tetromino', 'Tingle', 
         'Toad', 'Toon Link', 'Waluigi', 'Wario', 'Weegee', 'Yoshi', 'Zero Suit Samus']
    FormClass = makeform(chars=c, numerito=1, hasextra=True,
                         color1="#17659d", color2="#66d5fd")
    return hestia(request, "ssbc", FormClass, hasextra=True)

def minus(request) :
    c = ['Alloy Blue', 'Alloy Green', 'Alloy Red', 'Alloy Yellow', 'Bowser', 'Captain Falcon', 'Crazy Hand',
         'Diddy', 'Donkey Kong', 'Dr Mario', 'Falco', 'Fox', 'Ganondorf', 'Ice Climbers', 'Ike', 'Jigglypuff',
         'King Dedede', 'Kirby', 'Link', 'Lucario', 'Lucas', 'Luigi', 'Mario', 'Marth', 'Master hand', 'Mewtwo',
         'Meta Knight', 'Mewtwo', 'Mr Game & Watch', 'Ness', 'Olimar', 'Palutena', 'Pichu', 'Pika', 'Pit', 'Random',
         'Ridley', 'ROB', 'Roy', 'Samus', 'Sheik', 'Snake', 'Sonic', 'Squirtle', 'Toon Link', 'Waluigi', 'Wario', 'Wolf', 
         'Yoshi', 'Zelda', 'ZSS']
    FormClass = makeform(chars=c, numerito=1)
    return hestia(request, "ssbbminus", FormClass, hasextra=False)

def joymechfight(request) :
    c = ['Ashura', 'Blaze', 'Bokbok', 'Dachon', 'Eye', 'Flame', 'Gaean', 'Garborg', 'Gel', 'Geo', 'Ghoston',
         'Giant', 'Giganto', 'Grak', 'Hanzor', 'Houou', 'Hover', 'Jibber', 'John', 'Legend', 'Leo', 'Nay', 'Neo',
         'Old', 'Ra', 'Sasuku', 'Senju', 'Shenlong', 'Skapokon', 'Skapon', 'Skater', 'Star', 'Superzak', 'Tiger',
         'Wai', 'Zak']
    FormClass = makeform(chars=c, numerito=2, color1="#388888", color2="#388888")
    return hestia(request, "joymechfight", FormClass, hasextra=True)

def dbfz(request) :
    c = ['AdultGohan', 'Android16', 'Android17', 'Android18', 'Android21', 'Baby', 'Bardock', 'Beerus', 'BrolyDBS',
         'BrolyDBZ', 'CapitanGinyu', 'Cell', 'Cooler', 'Freezer', 'GogetaBlue', 'GogetaSSJ4', 'GokuBase', 'GokuBlack',
         'GokuBlue', 'GokuGT', 'GokuSSJ', 'GokuUI', 'Gotenks', 'Hit', 'Janemba', 'Jiren', 'Kefla', 'KidBu', 'Krillin',
         'Labdroid21', 'MajinBu', 'Nappa', 'Piccolo', 'Roshi', 'TeenGohan', 'Tien', 'Trunks', 'VegetaBase', 'VegetaBlue',
         'VegetaSSJ', 'VegettoBlue', 'Videl', 'Yamcha', 'Zamasu']
    FormClass = makeform(chars=c, numerito=1, color1="#943035", color2="#0f0000")
    return hestia(request, "dbfz", FormClass, hasextra=False)

def aigs(request) :
    c = ['B. Knight', 'Captain America', 'Crystal', 'Dr. Minerva', 'Korath', 'Shatterax', 'Supremor', 'Thunder Strike']
    FormClass = makeform(chars=c, numerito=1, color1="#e6dc38", color2="#a00b10")
    return hestia(request, "aigs", FormClass, hasextra=True)

def mvc2(request) :
    c = ['Blackheart', 'Cable', 'Captain America', 'Colossus', 'Cyclops', 'Doctor Doom', 'Gambit', 'Hulk', 'Iceman',
         'Iron Man', 'Juggernaut', 'Magneto', 'Marrow', 'Omega Red', 'Psylocke', 'Rogue', 'Sabretooth', 'Sentinel',
         'Shuma-Gorath', 'Silver Samurai', 'Spider-Man', 'Spiral', 'Storm', 'Thanos', 'Venom', 'War Machine',
         'Wolverine (Adamantium Claws)', 'Wolverine (Bone Claws)', 'Akuma', 'Amingo', 'Anakaris', 'B.B. Hood',
         'Cammy', 'Captain Commando', 'Charlie', 'Chun-Li', 'Dan', 'Dhalsim', 'Felicia', 'Guile', 'Hayato',
         'Jill Valentine', 'Jin', 'Ken', 'M. Bison', 'Mega Man', 'Morrigan', 'Roll', 'Ruby Heart', 'Ryu', 'Sakura',
         'Servbot', 'Sonson', 'Strider Hiryu', 'Tron Bonne', 'Zangief']
    FormClass = makeform(chars=c, numerito=6, numerito_extra=1, color1="#ffff00", color2="#ff00c8")
    return hestia(request, "mvc2", FormClass, hasextra=True)

def p4au(request) :
    hasextra = False
    c = ['Aigis', 'Akihiko Sanada', 'Chie Satonaka', 'Elizabeth', 'Junpei Iori', 'Kanji Tatsumi', 'Ken Amada', 'Labrys',
         'Margaret', 'Marie', 'Minazuki', 'Mitsuru Kirijo', 'Naoto Shirogane', 'Rise Kujikawa', 'Sho', 'Teddie',
         'Tohru Adachi', 'Yosuke Hanamura', 'Yu Narukami', 'Yukari Takeba', 'Yukiko Amagi']
    FormClass = makeform(chars=c, numerito=2, hasextra=hasextra,
                         color1="#FF0700", color2="#16b1e1")
    return hestia(request, "p4au", FormClass, hasextra=hasextra)

def kofxv(request) :
    hasextra = True
    c = c = ['Andy Bogard', 'Angel', 'Antonov', 'Ash Crimson', 'Athena Asamiya', 'B. Jenet', 'Benimaru Nikaido',
             'Blue Mary', 'Chizuru Kagura', 'Chris', 'Clark Still', 'Dolores', 'Elisabeth Blanctorche', 'Gato', 'Heidern',
             'Iori Yagami', 'Isla', 'Joe Higashi', "K'", 'King', 'King of Dinosaurs', 'Krohnen', 'Kukri', 'Kula Diamond',
             'Kyo Kusanagi', 'Leona Heidern', 'Luong', 'Mai Shiranui', 'Maxima', 'Meitenkun', 'Omega Rugal', 'Ralf Jones',
             'Ramón', 'Robert Garcia', 'Rock Howard', 'Ryo Sakazaki', 'Shermie', "Shun'ei", 'Terry Bogard', 'Vanessa', 'Whip',
             'Yashiro Nanakase', 'Yuri Sakazaki']
    FormClass = makeform(chars=c, numerito=1, hasextra=hasextra,
                         color1="#FF0700", color2="#16b1e1")
    return hestia(request, "kofxv", FormClass, hasextra=hasextra)

def tomandjerry(request) :
    hasextra = True
    c = ['Butch', 'Jerry', 'Nibbles', 'Quacker', 'Spike', 'Tom', 'Tyke']
    FormClass = makeform(chars=c, numerito=1, hasextra=hasextra,
                         color1="#c71a1a", color2="#f9521a")
    return hestia(request, "tyj", FormClass, hasextra=hasextra)

def kof2002um(request) :
    hasextra = True
    c = ['Andy', 'Angel', 'Athena', 'Bao', 'Benimaru', 'Billy', 'Chang', 'Chin',
         'Choi', 'Chris', 'Clark', 'Clone', 'Daimon', 'EX Kensou', 'EX Robert', 'EX Takuma',
         'Foxy', 'Geese', 'Goenitz', 'Heidern', 'Hinako', 'Igniz', 'Iori', 'Jhun', 'Joe', "K'",
         'Kasumi', 'Kensou', 'Kim', 'King', 'Krizalid', 'Kula', 'Kusanagi', 'Kyo', 'Kyo-1', 'Kyo-2',
         'Leona', 'Lin', 'Mai', 'Mary', 'Mature', 'Maxima', 'May', 'Nameless', 'Nightmare', 'Omega',
         'Orochi Chris', 'Orochi Shermie', 'Orochi Yashiro', 'Ralf', 'Ramon', 'Robert', 'Ryo', 'Seth',
         'Shermie', 'Shingo', 'Takuma', 'Terry', 'Vanessa', 'Vice', 'Whip', 'Xiangfei', 'Yamazaki', 
         'Yashiro', 'Yuri', 'Zero']
    FormClass = makeform(chars=c, numerito=1, hasextra=hasextra,
                         color1="#c71a1a", color2="#f9521a")
    return hestia(request, "kof2002um", FormClass, hasextra=hasextra)

def breakersrevenge(request) :
    hasextra = False
    c = ['Alsion', 'Condor', 'Dao-long', 'Maherl', 'Pielle', 'Rila', 'Saizo', 'Sho', 'Tia']
    FormClass = makeform(chars=c, numerito=4, hasextra=hasextra,
                         color1="#c71a1a", color2="#f9521a")
    return hestia(request, "breakersrevenge", FormClass, hasextra=hasextra)

def dnf(request) :
    return response_from_json(request, "dnf")

def pplusta(request) :
    return response_from_json(request, "p+ta")

def doa5(request) :
    return response_from_json(request, "doa5")

def doa6(request) :
    return response_from_json(request, "doa6")

def sfa3(request) :
    return response_from_json(request, "sfa3")

def vhun(request) :
    return response_from_json(request, "vhun")

def kyanta2(request) :
    return response_from_json(request, "kyanta2")

def multiversus(request) :
    return response_from_json(request, "multiversus")

def umvc3(request) :
    return response_from_json(request, "umvc3")

def elemensional(request) :
    return response_from_json(request, "elemensional")

def samsho2019(request) :
    return response_from_json(request, "samsho2019")

def moonatics(request) :
    return response_from_json(request, "moonatics")

def touhouantinomy(request) :
    return response_from_json(request, "touhouantinomy")