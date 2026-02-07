คู่มือการใช้งานระบบ Compensation System
โครงการ: MVC2


 รันโปรแกรม:
   python main.py
 หากเปิด GUI ไม่ได้และขึ้นว่าไม่มี PySide6 ให้ติดตั้ง:
   pip install PySide6
 เวอร์ชันนี้จะล้างข้อมูลเก่าทุกครั้งที่เปิดโปรแกรมใหม่ แล้ว seed ข้อมูลเริ่มต้นอัตโนมัติ

========================================
2) ส่วนประกอบหน้าจอ
========================================
- Login
  - Role: CITIZEN / OFFICER
  - Username
  - Password
  - ปุ่ม Login / Logout
- Submit Claim (Citizen)
  - ช่อง Claim ID (8 หลัก)
  - ปุ่ม Submit + Calculate
  - ปุ่ม Go To Claim List
- Claim List
  - ปุ่ม Refresh Claims
  - ปุ่ม Go To Submit Form
  - ตาราง Claims (แสดงผลคำขอและเงินเยียวยา)

========================================
3) บัญชีทดสอบ
========================================
Citizen:
- citizen1 / 1234
- citizen2 / 1234
- citizen3 / 1234

Officer:
- officer / admin

========================================
4) วิธีใช้งานหลัก
========================================
Citizen:
1. เลือก Role = CITIZEN
2. กรอก Username/Password และกด Login
3. กรอก Claim ID เป็นตัวเลข 8 หลัก (หลักแรกห้ามเป็น 0)
4. กด Submit + Calculate
5. ระบบจะกลับไปหน้า Claim List อัตโนมัติ
6. ตรวจสอบข้อมูลในตาราง Claims

Officer:
1. เลือก Role = OFFICER
2. กรอก officer / admin และกด Login
3. กด Refresh Claims เพื่อดูรายการทั้งหมด

สิทธิ์การมองเห็นข้อมูล:
- OFFICER: เห็น Claims ทั้งหมด
- CITIZEN: เห็นเฉพาะ Claims ของตนเอง
- Logout: ตาราง Claims ต้องว่าง

========================================
5) Business Rules การคำนวณ
========================================
หมายเหตุ: สูตรคำนวณอยู่ใน Model เท่านั้น และเลือกสูตรจาก monthly_income

1. LOW: รายได้ < 6500
   - เงินเยียวยา = 6500

2. NORMAL: รายได้ตั้งแต่ 6500 ถึงน้อยกว่า 50000
   - เงินเยียวยา = รายได้ต่อเดือน แต่ไม่เกิน 20000

3. HIGH: รายได้ >= 50000
   - เงินเยียวยา = รายได้ต่อเดือน / 5 แต่ไม่เกิน 20000

หลังคำนวณ:
- บันทึกผลลงตาราง Compensations
- อัปเดตสถานะ Claim เป็น CALCULATED
- กลับมาหน้ารายการคำขอ (Claim List) อัตโนมัติ

========================================
6) ชุด Test Cases (ครบตามการใช้งานหลัก)
========================================
TC-01: เปิดโปรแกรม
- ขั้นตอน: รัน python main.py
- ผลที่คาดหวัง: หน้าต่าง GUI เปิดได้ ไม่มี crash

TC-02: Login Citizen สำเร็จ
- ข้อมูล: role=CITIZEN, username=citizen1, password=1234
- ผลที่คาดหวัง: ขึ้น Login successful, ใช้งาน Submit Claim ได้

TC-03: Login Officer สำเร็จ
- ข้อมูล: role=OFFICER, username=officer, password=admin
- ผลที่คาดหวัง: ขึ้น Login successful, ปุ่ม/ส่วน Submit ถูกปิดใช้งาน

TC-04: Login ผิดรหัสผ่าน
- ข้อมูล: username=citizen1, password=9999
- ผลที่คาดหวัง: ขึ้น Login failed

TC-05: Login ไม่กรอกข้อมูล
- ข้อมูล: username ว่าง หรือ password ว่าง
- ผลที่คาดหวัง: ขึ้น Please enter username and password

TC-06: Login ตัวพิมพ์เล็ก/ใหญ่
- ข้อมูล: username=Citizen1, password=1234
- ผลที่คาดหวัง: Login ได้ (ไม่สนตัวพิมพ์เล็กใหญ่)

TC-07: Logout
- ขั้นตอน: Login ก่อน แล้วกด Logout
- ผลที่คาดหวัง: กลับสถานะ Not logged in และ Submit ใช้งานไม่ได้

TC-08: Submit โดยยังไม่ login
- ขั้นตอน: ไม่ login แล้วกด Submit + Calculate
- ผลที่คาดหวัง: ขึ้น Citizen login is required to submit a claim

TC-09: Validate Claim ID (ตัวอักษร)
- ข้อมูล: claim_id=12AB5678
- ผลที่คาดหวัง: ขึ้น error format claim id

TC-10: Validate Claim ID (ไม่ครบ 8 หลัก)
- ข้อมูล: claim_id=1234567
- ผลที่คาดหวัง: ขึ้น error format claim id

TC-11: Validate Claim ID (ขึ้นต้น 0)
- ข้อมูล: claim_id=01234567
- ผลที่คาดหวัง: ขึ้น error format claim id

TC-12: คำนวณ LOW (<6500)
- เงื่อนไขข้อมูล: ใช้ user ที่ monthly_income < 6500 (เช่น citizen1=5000)
- ขั้นตอน: login citizen1 แล้ว submit claim ใหม่
- ผลที่คาดหวัง: เงินเยียวยา = 6500

TC-13: คำนวณ NORMAL (6500 <= income < 50000)
- เงื่อนไขข้อมูล: user รายได้ 12000 (citizen2)
- ขั้นตอน: login citizen2 แล้ว submit claim ใหม่
- ผลที่คาดหวัง: เงินเยียวยา = 12000

TC-14: คำนวณ HIGH (income >= 50000)
- เงื่อนไขข้อมูล: user รายได้ 80000 (citizen3)
- ขั้นตอน: login citizen3 แล้ว submit claim ใหม่
- ผลที่คาดหวัง: เงินเยียวยา = 16000 (80000/5)

TC-15: Cap ของ NORMAL ไม่เกิน 20000
- เงื่อนไขข้อมูล: ตั้งรายได้ user ให้อยู่ช่วง NORMAL และมากกว่า 20000
- ผลที่คาดหวัง: เงินเยียวยา = 20000

TC-16: Cap ของ HIGH ไม่เกิน 20000
- เงื่อนไขข้อมูล: รายได้สูงมาก เช่น 200000
- ผลที่คาดหวัง: เงินเยียวยา = 20000

TC-17: บันทึก Compensations หลังคำนวณ
- ขั้นตอน: submit claim สำเร็จ 1 รายการ
- ผลที่คาดหวัง: ตาราง Compensations มีแถวใหม่ของ claim_id นั้น

TC-18: อัปเดตสถานะ Claim
- ขั้นตอน: submit claim สำเร็จ
- ผลที่คาดหวัง: status ของ Claims เป็น CALCULATED

TC-19: Duplicate Claim ID
- ขั้นตอน: ใช้ claim_id เดิม submit ซ้ำ
- ผลที่คาดหวัง: ระบบแจ้ง error จากฐานข้อมูล (primary key ซ้ำ)

TC-20: Refresh Claims
- ขั้นตอน: กด Refresh Claims หลัง submit
- ผลที่คาดหวัง: ตารางอัปเดตรายการล่าสุดและแสดง compensation

TC-21: หน้ารายการหลังคำนวณ
- ขั้นตอน: submit claim สำเร็จ
- ผลที่คาดหวัง: ยังคงอยู่ที่หน้ารายการ (ตาราง claims) และเห็นข้อมูลที่เพิ่งเพิ่ม

TC-22: Officer ห้าม submit
- ขั้นตอน: login officer
- ผลที่คาดหวัง: ส่วน Submit ถูกปิดใช้งาน

========================================
7) SQL ตรวจผล (ใช้ตอนส่งงาน/ดีบัก)
========================================
ดูข้อมูลผู้ใช้:
SELECT username, role, claimant_id FROM Users;

ดูคำขอทั้งหมด:
SELECT claim_id, claimant_id, submitted_date, status FROM Claims ORDER BY submitted_date DESC;

ดูผลคำนวณ:
SELECT claim_id, amount, calculated_date FROM Compensations ORDER BY calculated_date DESC;

เช็ค claim ใด claim หนึ่ง:
SELECT c.claim_id, c.status, cp.amount
FROM Claims c
LEFT JOIN Compensations cp ON cp.claim_id = c.claim_id
WHERE c.claim_id = '12345678';

========================================
8) ปัญหาที่พบบ่อย
========================================
1. กด Login แล้วไม่เกิดอะไรขึ้น
- ตรวจว่าใช้ไฟล์ main.py ล่าสุด
- ปิดโปรแกรมแล้วรันใหม่ด้วย python main.py

2. Login ไม่ผ่าน
- ตรวจ username/password
- ลองบัญชีตัวอย่างตามหัวข้อ 3

3. เปิด GUI ไม่ขึ้น
- ติดตั้ง PySide6
- ตรวจ Python environment ที่ใช้งานอยู่
