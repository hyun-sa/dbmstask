import pymysql
import numpy


connect_info = pymysql.connect(host='localhost', port=3306, user='hyunsa', password='qlalfqjsgh1!', db='taskDB', charset='utf8mb4')
cursor = connect_info.cursor()
idx = -1

def clear_screen():
    for _ in range(80):
        print()


def main_screen():
    global idx
    clear_screen()
    print("다음 항목을 선택하세요.")
    print("1. 학생 정보 일괄 추가")
    print("2. 과제 결과 추가")
    print("3. 유사도 검사 결과 추가")
    print("4. 데이터 조회")
    print("5. 데이터 초기화")
    print("0. 종료")
    idx =int(input("번호 입력 : "))


def add_student():
    clear_screen()
    chk = True
    while chk:
        fname = input("파일 이름 입력 (0 입력시 이전 화면 이동) : ")
        if fname == "0":
            return
        try:
            fp = open(fname + ".txt", "r")
        except FileNotFoundError:
            print("해당하는 파일이 없습니다. 다시 입력하세요.")
        else:
            chk = False
    chk = 0
    for line in fp.readlines():
        if "TA" in line and chk != 1:
            chk = 1
            continue
        if "STU" in line and chk != 2:
            chk = 2
            continue
        temp = line.split()
        snum = int(temp[0])
        sclass = int(temp[1])
        sname = temp[2]
        smail = temp[3]
        if chk == 1:
            cursor.execute(f"INSERT INTO class(class_no, TA_name) VALUES({sclass}, '{sname}');")
        cursor.execute(f"INSERT INTO student(stu_num, class_no, name, email) VALUES({snum}, {sclass}, '{sname}', '{smail}');")
    connect_info.commit()
    print("추가되었습니다. Enter(Return)키를 입력하여 메인화면으로 돌아가십시오.")
    input()


def add_task():
    clear_screen()
    chk = True
    while chk:
        fname = input("파일 이름 입력 (0 입력시 이전 화면 이동) : ")
        if fname == "0":
            return
        try:
            fp = open(fname + ".txt", "r")
        except FileNotFoundError:
            print("해당하는 파일이 없습니다. 다시 입력하세요.")
        else:
            chk = False
    chk = 0
    for line in fp.readlines():
        if "TA" in line and chk != 1:
            chk = 1
            continue
        if "TASK" in line and chk != 2:
            chk = 2
            continue
        temp = line.split()
        if chk == 1:
            tnum = int(temp[0])
            taname = temp[1]
            cursor.execute(f"INSERT INTO task_ta(task_num, TA_name) VALUES({tnum}, '{taname}');")
        elif chk == 2:
            snum = int(temp[0])
            stnum = int(temp[1])
            tsize = float(temp[2])
            score = int(temp[3])
            stime = float(temp[4])
            cursor.execute(f"INSERT INTO task(stu_num, task_num, size, score, submit_time) VALUES({snum}, {stnum}, {tsize}, {score}, {stime});")
    connect_info.commit()
    query = "SELECT class_no FROM class"
    cursor.execute(query)
    N = -1
    for cnum in cursor.fetchall():
        N = max(N, int(cnum[0]))
    query = "SELECT task_num, stu_num, class_no FROM task NATURAL JOIN student;"
    cursor.execute(query)
    for res in cursor.fetchall():
        K, stunum, M = map(int, res)
        cursor.execute(f"INSERT INTO result_task(result_No, stu_num, task_num) VALUES({(N+1)*(M-1)+K-1}, {stunum}, {M});")
    connect_info.commit()
    query = "SELECT task_num, class_no, score FROM task NATURAL JOIN student;"
    cursor.execute(query)
    result = [[] for _ in range(100)]
    for res in cursor.fetchall():
        K, M, score = map(int, res)
        result[(N+1)*(M-1)+K-1].append(score)
        result[(N+1)*M-1].append(score)
    for i in range(len(result)):
        if not result[i]:
            break;
        cursor.execute(f"INSERT INTO result(result_No, MAX, MIN, MEAN, STD) VALUES({i}, {max(result[i])}, {min(result[i])}, {numpy.mean(result[i])}, {numpy.std(result[i])});")
    connect_info.commit()
        
        
    print("추가되었습니다. Enter(Return)키를 입력하여 메인화면으로 돌아가십시오.")
    input()
    

def add_PLAG():
    clear_screen()
    chk = True
    while chk:
        fname = input("파일 이름 입력 (0 입력시 이전 화면 이동) : ")
        if fname == "0":
            return
        try:
            fp = open(fname + ".txt", "r")
        except FileNotFoundError:
            print("해당하는 파일이 없습니다. 다시 입력하세요.")
        else:
            chk = False
    chk = 0
    for line in fp.readlines():
        if "MOSS" in line and chk != 1:
            chk = 1
            continue
        if "JPLAG" in line and chk != 2:
            chk = 2
            continue
        temp = line.split()
        mainstu = int(temp[0])
        tasknum = int(temp[1])
        substu = int(temp[2])
        plag = float(temp[3])
        if chk == 1:
            cursor.execute(f"INSERT INTO MOSS_plag(main_stu, task_num, sub_stu, result) VALUES({mainstu}, {tasknum}, {substu}, {plag});")
        elif chk == 2:
            cursor.execute(f"INSERT INTO Jplag_plag(main_stu, task_num, sub_stu, result) VALUES({mainstu}, {tasknum}, {substu}, {plag});")
    connect_info.commit()
    print("추가되었습니다. Enter(Return)키를 입력하여 메인화면으로 돌아가십시오.")
    input()
    
    
def chk_screen():
    print("다음 항목을 선택하세요.")
    print("1. 단일 학생 정보 검색")
    print("2. 단일 분반 정보 검색")
    print("3. 통합 과제 정보 검색")
    print("4. 유사도 조회")
    print("0. 메인화면으로 돌아가기")
    return int(input("번호 입력 : "))
    
    
def chk_plag():
    print("다음 항목을 선택하세요.")
    print("1. 유사도 위험군 학생 조회")
    print("2. 유사도 경고군 학생 조회")
    print("3. 특정 학생 조회")
    print("0. 메인화면으로 돌아가기")
    return int(input("번호 입력 : "))
    

def check_data():
    clear_screen()
    chk_idx = chk_screen()
    if chk_idx == 1:
        snum = input("찾고자하는 학생의 학번 혹은 이름을 입력 : ")
        if snum.isdigit():
            cursor.execute(f"SELECT * FROM student NATURAL JOIN task WHERE stu_num={int(snum)}")
        else:
            cursor.execute(f"SELECT * FROM student NATURAL JOIN task WHERE name='{snum}'")
        i = True
        task = []
        
        for data in cursor.fetchall():
            temp = data
            if i:
                stnum = temp[0]
                stclass = temp[1]
                stname = temp[2]
                stmail = temp[3]
                i = False
            task.append([temp[4], temp[5], temp[6], temp[7]])
        
        print(f"==================================================")
        print(f"학생 이름 : {stname}, 학번 : {stnum}, 분반 : {stclass}, 메일 : {stmail}")
        print(f"==================================================")
        for i in task:
            print(f"과제 번호 : {i[0]}, 제출 용량 : {i[1]}, 점수 : {i[2]}, 실행 시간 : {i[3]}")
        print(f"==================================================")
    elif chk_idx == 2:
        clear_screen()
        sclass = int(input("찾고자하는 분반의 번호를 입력 : "))
        cursor.execute(f"SELECT * FROM student NATURAL JOIN task WHERE class_no={int(sclass)} ORDER BY stu_num")
        temp_stu = []
        task_num = []
        for data in cursor.fetchall():
            temp = data
            if temp[0] not in temp_stu:
                temp_stu.append(temp[0])
                stnum = temp[0]
                stclass = temp[1]
                stname = temp[2]
                stmail = temp[3]
                print(f"==================================================")
                print(f"학생 이름 : {stname}, 학번 : {stnum}, 분반 : {stclass}, 메일 : {stmail}")
                print(f"==================================================")
            if temp[4] not in task_num:
                task_num.append(temp[4])
            print(f"과제 번호 : {temp[4]}, 제출 용량 : {temp[5]}, 점수 : {temp[6]}, 실행 시간 : {temp[7]}")
        print(f"==================================================")
        chk_total = int(input("통합 결과를 보시겠습니까? (0 입력시 검색 종료) : "))
        task_num.sort()
        if chk_total:
            print(f"==================================================")
            cursor.execute(f"SELECT MAX(class_no) FROM class;")
            cnum = -1
            for val in cursor.fetchall():
                cnum = int(val[0])
            for i in task_num:
                cursor.execute(f"SELECT * FROM result WHERE result_No={(cnum-1)*(int(i))+sclass-1}")
                for data in cursor.fetchall():
                    temp = data
                    tmax = temp[1]
                    tmin = temp[2]
                    tmean = temp[3]
                    tstd = temp[4]
                    print(f"과제 번호 : {i}, 최대값 : {tmax}, 최소값 : {tmin}, 평균 : {tmean}, 표준편차 : {tstd}") 
            print(f"==================================================")
    elif chk_idx == 3:
        clear_screen()
        cursor.execute(f"SELECT MAX(class_no) FROM class;")
        cnum = -1
        for val in cursor.fetchall():
            cnum = int(val[0])
        cursor.execute(f"SELECT MAX(task_num) FROM task;")
        tnum = -1
        for val in cursor.fetchall():
            tnum = int(val[0])
        cursor.execute(f"SELECT * FROM result;")
        for i in range(tnum):
            print(f"=======과제 #{i+1}=======")
            for j in range(cnum):
                temp = cursor.fetchone()
                tmax = temp[1]
                tmin = temp[2]
                tmean = temp[3]
                tstd = temp[4]
                print(f"분반 : {j}, 최대값 : {tmax}, 최소값 : {tmin}, 평균 : {tmean}, 표준편차 : {tstd}")
            temp = cursor.fetchone()
            tmax = temp[1]
            tmin = temp[2]
            tmean = temp[3]
            tstd = temp[4]
            print(f"==================================================")
            print(f"통합 결과 = 최대값 : {tmax}, 최소값 : {tmin}, 평균 : {tmean}, 표준편차 : {tstd}")
            print(f"==================================================")
    elif chk_idx == 4:
        clear_screen()
        plag_chk = chk_plag()
        clear_screen()
        if plag_chk == 1:
            print(f"==================================================")
            print(f"=======MOSS Result=======")
            print(f"==================================================")
            cursor.execute(f"SELECT * FROM MOSS_plag WHERE result >= 40;")
            for data in cursor.fetchall():
                main_stu = data[0]
                tnum = data[1]
                sub_stu = data[2]
                pres = data[3]
                print(f"과제번호 : {tnum}, 주대상 : {main_stu}, 표절대상 : {sub_stu}, 표절율 : {pres}%")
            print(f"==================================================")
            print(f"=======JPLAG Result=======")
            print(f"==================================================")
            cursor.execute(f"SELECT * FROM Jplag_plag WHERE result >= 40;")
            for data in cursor.fetchall():
                main_stu = data[0]
                tnum = data[1]
                sub_stu = data[2]
                pres = data[3]
                print(f"과제번호 : {tnum}, 주대상 : {main_stu}, 표절대상 : {sub_stu}, 표절율 : {pres}%")
        elif plag_chk == 2:
            print(f"==================================================")
            print(f"=======MOSS Result=======")
            print(f"==================================================")
            cursor.execute(f"SELECT * FROM MOSS_plag WHERE result >= 20;")
            for data in cursor.fetchall():
                main_stu = data[0]
                tnum = data[1]
                sub_stu = data[2]
                pres = data[3]
                print(f"과제번호 : {tnum}, 주대상 : {main_stu}, 표절대상 : {sub_stu}, 표절율 : {pres}%")
            print(f"==================================================")
            print(f"=======JPLAG Result=======")
            print(f"==================================================")
            cursor.execute(f"SELECT * FROM Jplag_plag WHERE result >= 20;")
            for data in cursor.fetchall():
                main_stu = data[0]
                tnum = data[1]
                sub_stu = data[2]
                pres = data[3]
                print(f"과제번호 : {tnum}, 주대상 : {main_stu}, 표절대상 : {sub_stu}, 표절율 : {pres}%")
        elif plag_chk == 3:
            snum = input("찾고자하는 학생의 학번 혹은 이름을 입력 : ")
            if not snum.isdigit():
                cursor.execute(f"SELECT stu_num FROM student WHERE name = '{snum}'")
                snum = int(cursor.fetchone()[0])
            print(f"==================================================")
            print(f"=======MOSS Result=======")
            print(f"==================================================")
            cursor.execute(f"SELECT * FROM MOSS_plag WHERE main_stu = {snum};")
            for data in cursor.fetchall():
                main_stu = data[0]
                tnum = data[1]
                sub_stu = data[2]
                pres = data[3]
                print(f"과제번호 : {tnum}, 주대상 : {main_stu}, 표절대상 : {sub_stu}, 표절율 : {pres}%")
            print(f"==================================================")
            print(f"=======JPLAG Result=======")
            print(f"==================================================")
            cursor.execute(f"SELECT * FROM Jplag_plag WHERE main_stu = {snum};")
            for data in cursor.fetchall():
                main_stu = data[0]
                tnum = data[1]
                sub_stu = data[2]
                pres = data[3]
                print(f"과제번호 : {tnum}, 주대상 : {main_stu}, 표절대상 : {sub_stu}, 표절율 : {pres}%")
    else:
        return
    print("조회되었습니다. Enter(Return)키를 입력하여 메인화면으로 돌아가십시오.")
    input()
    

    

def clean_data():
    clear_screen()
    cursor.execute(f"SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute(f"TRUNCATE TABLE result;")
    cursor.execute(f"TRUNCATE TABLE result_task;")
    cursor.execute(f"TRUNCATE TABLE MOSS_plag;")
    cursor.execute(f"TRUNCATE TABLE Jplag_plag;")
    cursor.execute(f"TRUNCATE TABLE task;")
    cursor.execute(f"TRUNCATE TABLE task_ta;")
    cursor.execute(f"TRUNCATE TABLE student;")
    cursor.execute(f"TRUNCATE TABLE class;")
    cursor.execute(f"SET FOREIGN_KEY_CHECKS = 1;")
    connect_info.commit()
    print("초기화되었습니다. Enter(Return)키를 입력하여 메인화면으로 돌아가십시오.")
    input()


with connect_info:
    with connect_info.cursor() as cursor:
        while idx:
            main_screen()
            if idx ==1:
                add_student()
            elif idx ==2:
                add_task()
            elif idx ==3:
                add_PLAG()
            elif idx == 4:
                check_data()
            elif idx == 5:
                clean_data()
            elif not idx:
                clear_screen()