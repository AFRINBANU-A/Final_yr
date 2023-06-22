from flask import Flask, render_template, request
import pandas as pd
import random

city_dict={ "Ali" : 18 ,"Bar" : 2 ,"Ban" : 1 ,"Ch" :3,"Chid" :22,"Chit" :0,"Hyd" :6,"Kol":8,"Jai":15,"Moh":10,"Mum":11,"Man":7,"ND":13,
"Nag": 20,"Pal": 4,"Pali":12 ,"Pha":16 ,"Pu" :17 ,"Sa" :5 ,"Tiru":19 ,"Var":9 ,"Vel":21,"War":14 }

city_dict1={ "Ali" : "Aligarh" ,"Bar" : "Baroda" ,"Ban" : "Bangalore" ,"Ch" :"Chennai","Chid" :"Chidambaram","Chit":"Chitanukalan","Hyd":"Hydrabad","Kol":"Kolkata","Jai":"Jaipur","Moh":"Mohali","Mum":"Mumbai","Man":"Mangalore","ND":"New Delhi",
"Nag":"Nagpur","Pal": "Palani","Pali":"Pali" ,"Pha":"Phagwara" ,"Pu" :"Pune","Sa" :"Sawargaon" ,"Tiru":"Tiruchirappalli" ,"Var":"Varanasi","Vel":"Vellore","War":"Warangal" }
univ_dict={"AMU" : [1,85],
"ANU" : [2 ,60],
"AU" : [3,50],
"AnU" : [4,60],
"ARKA" : [5 , 55],
"AIHS" : [6 , 50],
"BS" :[7 , 70],
"BBAU" : [8 ,50],
"BV":[9,55],
"BU" :[10 , 60],
"BIHER" : [11 , 50],
"BIT" :[ 12,55],
"BITS" : [ 13 ,60 ],
"CUTM" :[14 , 60],
"CHU" : [15,45],
"CUC":[17,80 ],
"CU":[18, 60],
"CV":[19, 70],
"DAIICT":[20, 85],
"DEI":[21, 80],
"DTU":[22,70 ],
"DSU":[23, 50],
"DDU":[24, 80],
"MGR": [26, 55],
"EU": [27, 85],
"GU": [28, 60],
"GLA": [29, 45],
"GEU": [30, 50],
"GGSIU": [31, 55],
"GJU": [32, 40],
"GNDU": [33, 40],
"HITS": [34, 65],
"III": [35, 80],
"IIIT": [36, 75],
"JU": [37, 55],
"JH": [38, 60],
"JMI": [39, 65],
"JNTU": [40, 60],
"JII": [41, 80],
"JUI": [42, 65],
"JSS": [43, 85],
"KU": [44,40],
"KARE": [45, 60],
"KIIT": [46, 80],
"KLU": [47, 60],
"KAHE": [48, 60],
"KRU": [49, 50],
"KL": [50, 75],
"KLE": [51, 40],
"KLEF": [52, 55],
"LPU": [53, 50],
"MSUB": [54, 45],
"MRU": [55, 40],
"MU": [56, 50],
"MIU": [57, 45],
"NSUT": [58, 60],
"NIMS": [59, 65],
"NEHU": [60, 60],
"PES": [61, 75],
"RTU": [62, 80],
"RGU": [63, 85],
"RTMN": [64, 88],
"RK": [65, 60],
"SASTRA": [66, 50],
"SU": [67, 85],
"SCSVMV": [68, 90],
"SHU": [69, 50],
"SNU": [70, 60],
"SUS": [71, 50],
"SMVD": [72, 50],
"SOA": [73, 45],
"SRU": [74, 50],
"SPMV": [75, 65],
"SRM": [76, 50],
"TU": [77, 45],
"THU": [78, 80],
"UD": [79, 55],
"VSSUT": [80, 85],
"VTC": [81, 55],
"VIT": [82, 55],
"VUC": [83, 55],
"VFST": [84, 60],
"VTU": [85, 55],
"YMCA": [86, 75],}

headings=("University Name","State","District","College Link","Location Link","Entrance Percentage","Ranking","12th Percentage")
data=( ("Amity University" , "Rajasthan" , "Jaipur" , "https://www.amity.edu/" , "https://goo.gl/maps/E9nZojejiJKuwPDw8" , 85 , 46 , 43),
       ("Anna University" , "Tamil Nadu" , "Chennai" , "https://www.annauniv.edu/" , "https://g.co/kgs/AtzjCr" , 60 , 50 , 21),
       ("Annamalai University","Tamil Nadu","Chidambaram","https://annamalaiuniversity.ac.in/index.php","https://goo.gl/maps/NEjmf5ZQxppHT5hc6",60,152,55),
       ("Anurag University" , "Telangana" , "Hyderabad" , "https://anurag.edu.in/",	"https://goo.gl/maps/2cTzdBUCpv88JVCG9" , 60 , 103 , 50),
       ("ARKA Jain University" , "Jharkhand", "Jamshedpur", "https://arkajainuniversity.ac.in/" , "https://goo.gl/maps/o1dZkxMVxMPp1pry8" , 55 , 101, 50),
       ("Avinashilingam Institute for Home Science and Higher Education for Women" , "Tamil Nadu" ,	"Coimbatore" , "https://avinuty.ac.in/", "https://goo.gl/maps/kNKWXXc3PAT3HvQJ8" , 50 , 84 , 65),
       ("B.S Abdur Rahman Crescent Institute of Science and Technology" , "Tamil Nadu" , "Chennai" , "https://crescent.education/" , "https://goo.gl/maps/y627EpYGaU2n51cx6" , 65 , 104 , 50),
       ("Babasaheb Bhimrao Ambedkar University" , "Uttar Pradesh" , "Lucknow" , "https://www.bbau.ac.in/" , "https://g.co/kgs/QRWqPy" , 50 , 55 , 50),
       ("Banasthali Vidyapith" , "Rajasthan" , "Jaipur", "http://www.banasthali.org/" , "https://goo.gl/maps/HEMu2bzyks42d4pEA" , 55 , 49 , 50),
       ("Bangalore University" , "Karnataka" , "Bangalore" , "https://bangaloreuniversity.ac.in/" , "https://goo.gl/maps/cWzqfAHnmuoMGdbz6", 60 , 64 , 50),
       ("Bharath Institute of Higher Education and Research" , "Tamil Nadu" , "Chennai" , "https://www.bharathuniv.ac.in/" , "https://goo.gl/maps/Zf218hvCqYgAMDhU8" , 50 , 62 , 50),
       ("Bharatiya Engineering Science and Technology Innovation University" , "Andhra Pradesh" ," Anantapur" , "https://bestiu.edu.in/" , "https://goo.gl/maps/zSybbSK5TiuaFBhU7" , 65 , 107 , 55),
       ("Birla Institute of Technology" , "Jharkhand" , "Ranchi" , "https://www.bitmesra.ac.in/" , "https://goo.gl/maps/1CZfRWuJ6NG6x4pr6" , 55 , 99 , 75),
       ("Birla Institute of Technology and Science" , "Rajasthan" , "Pilani" , "https://www.bits-pilani.ac.in/" , "https://goo.gl/maps/oHKxsWrDZzUCkRmC8" , 60 , 18 , 75),
       ("Centurion University of Technology and Management" , "Odisha" , "Gajapati" , "https://cutm.ac.in/" , "https://goo.gl/maps/a95EzZns6PxWxLFF8" , 60 , 109 , 60),
       ("Chandigarh University" , "Punjab" , "Chandigarh" , "https://www.cuchd.in/" , "https://g.co/kgs/XwSLN1" , 35 , 29 , 50),
       ("Chitkara University Chandigarh" , "Punjab" , "Patiala" , "https://www.chitkara.edu.in/" , "https://goo.gl/maps/1pTzs5VdAkYqQ2MNA" , 80, 108 , 65),
       ("Christ University" , "Karnataka" , "Bangalore" , "https://christuniversity.in/" , "https://g.co/kgs/A5xA4w" , 60 , 71 , 50),
       ("CV Raman Global University" , "Odisha" , "Bhubaneswar" , "https://cgu-odisha.ac.in/" , "https://goo.gl/maps/a3gWu2RcwYNRQSH46" , 70 , 105, 60),
       ("DAIICT Gandhinagar" , "Gujarat" , "Gandhinagar" , "https://www.daiict.ac.in/" , "https://googl/maps/uusLMy5wJV8WsLzx7" , 85 , 123 , 60),
       ("Dayalbagh Educational Institute" , "Uttar Pradesh" , "Agra" , "https://www.dei.ac.in/dei/" , "https://g.co/kgs/TMQ8Gy " , 80 , 111 , 65),
       ("Delhi Technological University","New Delhi","New Delhi","http://www.dtu.ac.in/","https://goo.gl/maps/VHMGgd3YwdPJitHD8",60,36,60),
       ("Dhanalakshmi Srinivasan University" , "Tamil Nadu" , "Tiruchirappalli" , "https://www.dsuniversity.ac.in/" , "https://g.co/kgs/oGV2JC" ,50, 118 , 70),
       ("Dharmsinh Desai Univeersity" , "Gujarat" , "Nadidad" , "https://www.ddu.ac.in/" , "https://goo.gl/maps/NU4fHXsqxTXfzpTJ7" , 80 , 120 , 55),
       ("Dr MGR Educational and Research Institute","Tamil Nadu","Chennai","https://www.drmgrdu.ac.in/","https://goo.gl/maps/CuRyHK8xAfDaLjUGA",55,28,65),
       ("Eklavya University" , "Madhya Pradesh" , "Damoh" , "https://eklavyauniversity.ac.in/" , "https://goo.gl/maps/si3zEjKBCfEsEZLr6" , 85 , 125 , 55),
       ("Galgotias University" , "Uttar Pradesh" , "Greater Noida" , "https://www.galgotiasuniversity.edu.in/" , "https://goo.gl/maps/mtcwattX77h4pBVn7" , 60 , 133 ,65),
       ("GLA University" , "Uttar Pradesh" , "Mathura" , "https://www.gla.ac.in/" , "https://goo.gl/maps/f1XiTRCwJVZcih3t7" , 45 , 135 , 55),
       ("Graphic Era University" , "Uttarakhand" , "Dehradun" , "https://www.geu.ac.in/" , "https://goo.gl/maps/fhyrnp91KyUUyTXP8" , 85 , 43 , 60),
       ("Guru Gobind Singh Indraprastha University","New Delhi","New Delhi","http://www.ipu.ac.in/","https://goo.gl/maps/YknYxUsX6m2MAXRXA", 55 , 24 , 55),
       ("Guru Jambheshwar University of Science and Technology" , "Haryana" , "Hisar" , "https://www.gjust.ac.in/" , "https://goo.gl/maps/nApLB8Q7buGLwPmi9" , 40 , 29 , 75),
       ("Guru Nanak Dev University" , "Punjab" , "Amritsar" , "https://online.gndu.ac.in/" , "https://goo.gl/maps/w39WWYGEmSMBi99VA" , 40 , 15 , 50),
       ("Hindustan Institute of Technology and Science", "Tamil Nadu" , "Chennai" , "https://hindustanuniv.ac.in/" , "https://goo.gl/maps/EkDvsP6mXWsYxe5v6	50" , 65 , 40 , 50),
    #    ("Indian Institute of Science, Bangalore","Karnataka","Bangalore","https://iisc.ac.in/","https://goo.gl/maps/GK9gUja8pnfSpFYL7",70,94,50),
    #    ("Indian Institute of Technology,Bombay","Maharashtra","Mumbai","https://www.iitb.ac.in/","https://goo.gl/maps/kbKqj6Z9bfGnERS39",50,80,60),
    #    ("Indian Institute of Technology,Madras","Tamil Nadu","Chennai","https://www.iitm.ac.in/","https://goo.gl/maps/73bHL5Q8RQS8yt5v9",55,153,55),
    #    ("Indian Institute of Technology,Delhi","New Delhi","New Delhi","https://home.iitd.ac.in/","https://goo.gl/maps/3gPFUWx7fp2A99fP6",75,160,60),
    #    ("Indira Gandhi National Open University","New Delhi","New Delhi","http://ignou.ac.in/","https://goo.gl/maps/SfsYq66L9xvvDFsbA",55,71,55),
    #    ("Institute of Chemical Technology, Mumbai","Maharashtra","Mumbai","https://www.ictmumbai.edu.in/","https://goo.gl/maps/Y6rD7yit6Kc7dH189",66,14,55),
       ("Indraprastha Institute of Information Technology" , "Delhi" , "New Delhi" , "https://iiitd.ac.in/" , "https://goo.gl/maps/AC1U2YTsuoiQSq6eA" , 80 , 130 , 55),
       ("International Institute of Information Technology" , "Telangana" , "Hyderabad" , "https://www.iiitb.ac.in/" , "https://g.co/kgs/M43ZHu" , 75 , 129 , 75),
       ("Jadavpur University","West Bengal","Kolkata","http://www.jaduniv.edu.in/","https://goo.gl/maps/dLSJoT2jB61XXBUZA",60,4,45),
       ("Jamia Hamdard","New Delhi","New Delhi","http://jamiahamdard.edu/","https://goo.gl/maps/z6S684pksuWb4vFs5",50,46,50),
       ("Jamia Millia Islamia","New Delhi","New Delhi","https://www.jmi.ac.in/","https://goo.gl/maps/NCaytJGjbrEMc3WU8",50,3,50),
       ("Jawaharlal Nehru University","Tamil Nadu","Pali","https://www.jnu.ac.in/","https://goo.gl/maps/s6VEFh8SNQ391jLs9",55,10,55),
       ("JSS Science and Technology University" , "Karnataka" , "Mysuru" , "https://jssstuniv.in/" , "https://goo.gl/maps/s6mJqsHfZyHpsfSy8" , 85 , 124 , 45),
       ("Kakatiya University" , "Telangana" , "Hanamkonda" , "https://www.kakatiya.ac.in/" , "https://goo.gl/maps/RAZPaEx9rbjM8m1k8" , 40 , 113 , 50),
       ("Kalasalingam Academy of Research and Education" , "Tamil Nadu" , "Krishnan Kovil" , "https://kalasalingam.ac.in/" , "https://goo.gl/maps/coPeEF664DULfUkm8"	 , 60 , 35 , 55),
       ("Kalinga Institute of Industrial Technology" , "Odisha" , "Bhubaneshwar" , "https://kiit.ac.in/" , "https://g.co/kgs/D5dpGt" , 80 , 20 , 60),
       ("Kalinga University" , "Chhattisgarh" , "Naya Raipur" , "https://kalingauniversity.ac.in/" , "https://goo.gl/maps/3qa7GEsLPxY9cQ1u7" , 60 , 114 ,55),
       ("Karpagam Academy of Higher Education" , "Tamil Nadu" , "Coimbatore" , "https://kahedu.edu.in/" , "https://goo.gl/maps/B5EgnmjdCTaM2q7V8" , 60 , 128 , 50),
       ("Karunya University" , "Tamil Nadu" , "Coimbatore" , "https://www.karunya.edu/" , "https://goo.gl/maps/k7zhnjoSxAWhxCqR9" , 50 , 117 , 50),
       ("KL University Guntur" , "Andhra Pradesh" , "Guntur" , "https://www.kluniversity.in/" , "https://maps.google.com/maps/contrib/109107625783380127325" , 75 , 27 , 60),
       ("KLE Technological University" , "Karnataka" , "Hubli" , "https://www.kletech.ac.in/" , "https://goo.gl/maps/xcJWavLkgsjJQ9zG6" , 40 , 127 , 60),
       ("Koneru Lakshmaiah Education Foundation" , "Andhra Pradesh" , "Guntur" , "https://www.kluniversity.in/" , "https://goo.gl/maps/RXVE74BBjgRQ7HNx7" , 55 , 27 , 85),
       ("Lovely Professional University","Punjab","Phagwara","https://www.lpu.in/","https://g.page/LPUUniversity?share",55,47,60),
       ("Maharaja Sayajirao University of Baroda","Gujarat","Baroda","https://www.msubaroda.ac.in/","https://g.page/TheMSUB?share",50,90,40),
       ("Malla Reddy University" , "Telangana" , "Hyderabad" , "https://www.mallareddyuniversity.ac.in/" , "https://goo.gl/maps/JEwXa4DoectvuYYy8" , 40 , 123 , 45),
       ("Manipal University","Rajasthan","Jaipur","https://manipal.edu/mu.html","https://goo.gl/maps/JsuTibUDEocMwkxt9",50,103,50),
       ("Mizoram University" , "Mizoram" , "Aizawl" , "https://mzu.edu.in/" , "https://goo.gl/maps/kVbpGM44zbXJSWkj8" , 45 , 78 , 50), 
    #    ("National Institute of Technology Karnataka","Karnataka","Mangalore","https://www.nitk.ac.in/","https://goo.gl/maps/eRFnpagJi5i4z5yS9",75,64,60),
    #    ("National Institute of Technology Tiruchirappalli","Tamil Nadu","Tiruchirappalli","https://www.nitt.edu/","https://goo.gl/maps/jCdSeTTq88JgF1HJ8",65,47,75),
    #    ("National Institute of Technology, Warangal","Telangana","Warangal","https://www.nitw.ac.in/","https://goo.gl/maps/nE1XMKvb5eRTfo6f8",75,45,75),
       ("Netaji Subhas University of Technology" , "Delhi" , "New Delhi" , "http://nsut.ac.in/en/home" , "https://goo.gl/maps/BVvPAmUc2qUzH9xY9" , 60 , 107 , 60),
       ("NIMS University","Rajasthan","Chitanukalan","https://www.nimsuniversity.org/","https://g.page/MyNIMS?share",65,101,50),
       ("North Eastern Hill University" , "Meghalaya" , "Shilong" , "https://nehu.ac.in/" , "https://g.co/kgs/iZjDcE" , 60 , 90, 65),
       ("PES University","Karnataka","Bangalore","https://pes.edu/","https://goo.gl/maps/6C2mn7kWp4JDaVz17",60,83,50),
       ("Rabindranath Tagore University" , "Madhya Pradesh" , "Raisen" , "https://rntu.ac.in/" , "https://g.co/kgs/zYCSzT", 65 , 125, 45),
       ("Radha Govind University" , "Jharkhand" , "Ramgarh" , "https://www.rguniversity.org/" , "https://goo.gl/maps/ZfpzqcEvwcxUVJcH6" , 85 , 122 ,50),
       ("Rashtrasant Tukadoji Maharaj Nagpur University" , "Maharashtra" , "Nagpur" , "https://nagpuruniversity.ac.in/" , "https://goo.gl/maps/xDDg92pi5CEiVJuTA" , 88 , 134 ,50),
       ("RK University" , "Gujarat" , "Rajkot" , "https://rku.ac.in/", "https://goo.gl/maps/7R9gStvvMLfsaqGP6" , 60 , 131 , 60),
       ("SASTRA University Thanjavur" , "Tamil Nadu" , "Thanjavur" , "https://www.sastra.edu/" , "https://goo.gl/maps/7z3WWVvmPvrBpwQ39" , 50 , 24 , 60),
       ("Sathyabama University" , "Tamil Nadu" , "Chennai" , "https://www.sathyabama.ac.in/" , "https://g.co/kgs/UzmEBP" , 85 , 43 , 60),
       ("SCSVMV University" , "Tamil Nadu" , "Kanchipuram" , "https://kanchiuniv.ac.in/" , "https://goo.gl/maps/5PGa4fFoEy26u5rDA" , 90 , 122 , 80),
       ("Sharda University" , "Uttar Pradesh" , "Greater Noida" , "https://www.sharda.ac.in/" , "https://goo.gl/maps/GswuyntYd6Sch2fH7" , 50 , 117, 60),
       ("Shiv Nadar University" , "Uttar Pradesh" , "Greater Noida" , "https://snu.edu.in/" , "https://goo.gl/maps/3iZFj2nXgeshknPYA" , 60 , 61 ,60),
       ("Shoolini University Solan" , "Himachal Pradesh" , "Solan" , "https://shooliniuniversity.com/" , "https://goo.gl/maps/wQ3EyVPwMzRmWG957" , 	50 , 96 , 60),
       ("Shri Mata Vaishno Devi University" , "Jammu and Kashmir" , "Katra" , "https://www.smvdu.ac.in/" , "https://goo.gl/maps/7Qsi5nUdp6yKRf2FA" , 50 , 119 , 50),
       ("Siksha 'O' Anusandhan" , "Odisha" , "Bhubaneshwar" , "https://www.soa.ac.in/" , "https://goo.gl/maps/dDxLYvgf6mi8x9sa8" , 45 , 16 , 50),
       ("SR University" , "Telangana" , "Warangal" , "https://sru.edu.in/" , "https://goo.gl/maps/iDLH9x7GruZgJCrc7" , 50 , 80 , 70),
       ("Sri Padmavati Mahila Visvavidyalayam" , "Andhra Pradesh" , "Tirupati" , "https://www.spmvv.ac.in/" , "https://g.co/kgs/rnRUc9" , 65 , 120 , 60),
       ("SRM Institute of Science and Technology","Tamil Nadu","Chennai","https://www.srmist.edu.in/","https://goo.gl/maps/z7BsZBg1coy96UdJ8",60,19,50),
       ("Tezpur University" , "Assam" , "Tezpur" , "http://www.tezu.ernet.in/" , "https://goo.gl/maps/qqTycTUax6ahqjAb6" , 45 , 59 , 50),
       ("Thapar University" , "Punjab" , "Patiala" , "https://www.thapar.edu/" , "https://goo.gl/maps/sqxs6iKnrHRgVfDW7" , 80 , 31 ,70),
       ("University of Delhi","New Delhi","New Delhi","http://www.du.ac.in/","https://goo.gl/maps/FRukDt7VQXdQfUJcA",45,13,50),
       ("Veer Surendra Sai University of Technology" , "Odisha" , "Burla" , "https://www.vssut.ac.in/" , "https://goo.gl/maps/DeatBv4ft6mzhrRu7" , 85 , 140 , 75),
       ("Vel Tech Chennai" , "Tamil Nadu" , "Chennai" , "https://www.veltech.edu.in/", "https://g.co/kgs/3hHLJ5" , 55 , 93 , 60),
       ("Vellore Institute of Technology","Tamil Nadu","Vellore","https://vit.ac.in/","https://goo.gl/maps/hgQD3vdarwFDZP1eA",55,9,55),
       ("Vels University Chennai" , "Tamil Nadu" , "Chennai " , "https://vistas.ac.in/" , "https://goo.gl/maps/wwe6WVMxi5PxRD5z6" , 55 , 121 , 60),
       ("Vignan's Foundation for Science Technology and Research" , "Andhra Pradesh" , "Guntur" , "https://www.vignan.ac.in/" , "https://goo.gl/maps/MfLaKp6fnnG1pedf7" , 60 , 95 , 60),
       ("Visvesvaraya National Institute of Technology","Maharashtra","Nagpur","https://vnit.ac.in/","https://goo.gl/maps/VNnyPyWo7jZp5xCX7",65,54,75),
       ("YMCA Faridabad" , "Haryana" , "Faridabad" , "https://jcboseust.ac.in/" , "https://goo.gl/maps/chhtxGuP6dwU8QS97", 75 , 100 , 50),
)

responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you": ["I'm doing well, thanks for asking.", "I'm fine, how about you?"],
    "can you explain about cs department":["Yeah!! sure dude. CS department is one of the growing department in IT industries. Do you need more information just work on the cs deparment site"],
    "cs department is worth to choose":["Yes,its worth to take","ofcourse buddy"],
    "more information need to know about cs department":["just work on our site you will get more exciting information"],
    "what's up?": ["Nothing much, you?", "Just chatting with you.", "Not much, how about you?"],
    "bye": ["Goodbye!", "Bye-bye!", "See you later!"],
    "job opportunity of cs department":["left side of this page can see the Job vacancy and Latest News!! by clicking the links you are redirect and see the information"],
    "I'm a slow learner can i choose cs department":["Yeah!!, Don't lose your hope just try you can and you will"],
    "I'm not eligible for cs department what can i do":["Don't lose hope try other departments you will get it"],
    "cs department have future" :["yeah!! it have more future","yes!!","definitely it have bright future"]

}

def generate_response(message):
    message = message.lower()
    if message in responses:
        return random.choice(responses[message])
    else:
        return "Can you reach out us through mail id : vidyapeethinfo@gmail.com (or) Linkedin : www.linkedin.com/in/vidhyapeeth (or) Twitter : https://twitter.com/Vidhyapeethinfo"

app = Flask(__name__)

import pickle
model = pickle.load(open(r"C:\Users\A.Afrinbanu\OneDrive\Desktop\Implementation\pickle.pkl",'rb'))


@app.route('/',methods=['GET'])
def home():
    return render_template("Home.html")

@app.route('/faqece')
def faqece():
    return render_template("Faqece.html")

@app.route('/faqeee')
def faqeee():
    return render_template("Faqeee.html")

@app.route('/faqmech')
def faqmech():
    return render_template("Faqmech.html")

@app.route('/faqcivil')
def faqcivil():
    return render_template("Faqcivil.html")

@app.route('/faqit')
def faqit():
    return render_template("Faqit.html")

@app.route('/about')
def about():
    return render_template("About.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/faqcs')
def faqcs():
    return render_template("Faqcs.html")

@app.route('/get')
def get_bot_response():
    user_input = request.args.get('msg')
    response = generate_response(user_input)
    return str(response)

@app.route('/choose_dept', methods=['POST'])
def departments():
    dep = request.form["depts"]
    if(dep == "civil"):
        return render_template("civil.html")
    if(dep == "cse"):
        return render_template("cse.html")
    if(dep == "ece"):
        return render_template("ece.html")
    if(dep == "eee"):
        return render_template("eee.html")
    if(dep == "mech"):
        return render_template("mech.html")
    if(dep == "it"):
        return render_template("it.html")

    return '0'

@app.route('/civil',methods=['POST'])
def civil():
    d1_civil=[]
    d2_civil=[]
    u=0
    e=0
    c=0
    percent= request.form.get('twelC',type=float)
    cities=request.form["citiesC"]
    univ = request.form["uniC"]
    for key in city_dict1:
        if key == cities:
            c=city_dict1[key]
    for key1 in univ_dict:
        if key1 == univ:
            x=univ_dict[key1]
            u = x[0]
            e = x[1]
    pred = [[u,int(percent),e,0]]  
    output = model.predict(pred)
    i=0
    for ds in data:
            if(float(ds[7]) >= percent or c==ds[2]) and i<10:
                d1_civil.insert(i,ds)
                i+=1
    
    d2_civil = list(set(j for j in d1_civil))
    if(output == 1):
        return render_template("output.html",prediction="Congrats you are Eligible", headings=headings,d2=d2_civil)
    else:
        return render_template("output.html",prediction="You are not eligible. Let's hope for the best",headings=headings,d2=d2_civil)
    

@app.route('/cse',methods=['POST'])
def cse():
    d1_cse=[]
    d2_cse=[]
    d=1
    c1=0
    percent1= request.form.get('twel',type=float)
    cities=request.form["cities"]
    univ = request.form["uni"]
    for key in city_dict1:
        if key == cities:
            c1=city_dict1[key]
    for key1 in univ_dict:
        if key1 == univ:
            univ=key1
            x=univ_dict[key1]
            u1 = x[0]
            e1 = x[1]
    pred = [[u1,int(percent1),e1,d]]  
    output = model.predict(pred)
    i1 = 0
    for ds in data:
        if(float(ds[7]) >= percent1 or c1==ds[2]) and i1 < 10:
            d1_cse.insert(i1,ds)
            i1 += 1
    
    d2_cse = list(set(j for j in d1_cse))
    if(output == 1):
        return render_template("output.html",prediction="Congrats you are Eligible", headings=headings,d2=d2_cse)
    else:
        return render_template("output.html",prediction="You are not eligible. Let's hope for the best",headings=headings,d2=d2_cse)
    
@app.route('/ece',methods=['POST'])
def ece():
    d1_ece=[]
    d2_ece=[]
    d=3
    percent2= request.form.get('twelEC',type=float)
    cities=request.form["citiesEC"]
    univ = request.form["uniEC"]
    for key in city_dict1:
        if key == cities:
            c2=city_dict1[key]
    for key1 in univ_dict:
        if key1 == univ:
            x=univ_dict[key1]
            u2 = x[0]
            e2 = x[1]
    pred = [[u2,int(percent2),e2,d]]  
    output = model.predict(pred)
    i2 = 0
    for ds in data:
            if(float(ds[7]) >= percent2 or c2==ds[2]) and i2 < 10:
                d1_ece.insert(i2,ds)
                i2 += 1
    
    d2_ece = list(set(j for j in d1_ece))
    if(output == 1):
        return render_template("output.html",prediction="Congrats you are Eligible", headings=headings,d2=d2_ece)
    else:
        return render_template("output.html",prediction="You are not eligible. Let's hope for the best",headings=headings,d2=d2_ece)
    
    
@app.route('/eee',methods=['POST'])
def eee():
    d1_eee=[]
    d2_eee=[]
    d=2
    percent3= request.form.get('twelE',type=float)
    cities=request.form["citiesE"]
    univ = request.form["uniE"]
    for key in city_dict1:
        if key == cities:
            c3=city_dict1[key]
    for key1 in univ_dict:
        if key1 == univ:
            x=univ_dict[key1]
            u3 = x[0]
            e3 = x[1]
    pred = [[u3,int(percent3),e3,d]]  
    output = model.predict(pred)
    i3=0
    for ds in data:
        if(float(ds[7]) >= percent3 or c3==ds[2]) and i3 < 10:
            d1_eee.insert(i3,ds)
            i3 += 1
    
    d2_eee = list(set(j for j in d1_eee))
    if(output == 1):
        return render_template("output.html",prediction="Congrats you are Eligible", headings=headings,d2=d2_eee)
    else:
        return render_template("output.html",prediction="You are not eligible. Let's hope for the best",headings=headings,d2=d2_eee)
    
@app.route('/mech',methods=['POST'])
def mech():
    d1_mech=[]
    d2_mech=[]
    d=4
    percent4= request.form.get('twelM',type=float)
    cities=request.form["citiesM"]
    univ4 = request.form["uniM"]
    for key in city_dict1:
        if key == cities:
            c4=city_dict1[key]
    for key1 in univ_dict:
        if key1 == univ4:
            x=univ_dict[key1]
            u = x[0]
            e = x[1]
    pred = [[u,int(percent4),e,d]]  
    output = model.predict(pred)
    i4=0
    for ds in data:
            if(float(ds[7]) >= percent4 or c4==ds[2]) and i4 < 10:
                d1_mech.insert(i4,ds)
                i4 += 1
    
    d2_mech = list(set(j for j in d1_mech))
    if(output == 1):
        return render_template("output.html",prediction="Congrats you are Eligible", headings=headings,d2=d2_mech)
    else:
        return render_template("output.html",prediction="You are not eligible. Let's hope for the best",headings=headings,d2=d2_mech)
    

@app.route('/it',methods=['POST'])
def it():
    d1_it=[]
    d2_it=[]
    d=5
    percent5= request.form.get('tweli',type=float)
    cities=request.form["citiesi"]
    univ5 = request.form["unii"]
    for key in city_dict1:
        if key == cities:
            c5=city_dict1[key]
    for key1 in univ_dict:
        if key1 == univ5:
            x=univ_dict[key1]
            u2 = x[0]
            e2 = x[1]
    pred = [[u2,int(percent5),e2,d]]  
    output = model.predict(pred)
    i5 = 0
    for ds in data:
            if(float(ds[7]) >= percent5 or c5==ds[2]) and i5 < 10:
                d1_it.insert(i5,ds)
                i5 += 1
    
    d2_it = list(set(j for j in d1_it))
    if(output == 1):
        return render_template("output.html",prediction="Congrats you are Eligible", headings=headings,d2=d2_it)
    else:
        return render_template("output.html",prediction="You are not eligible. Let's hope for the best",headings=headings,d2=d2_it)

if __name__ == '__main__':
    app.run(debug=True)
