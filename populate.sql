insert into Person (net_id, fname, mname, lname, hours_completed, usertype)
values ('abc180000', 'Alvin','Ben', 'Carter', 0, 'tutor'),
('def180000', 'Devin','Eules', 'Farhadi', 1, 'tutor'),
('ghi180000', 'Gerald','Henry', 'Immhurst', 2, 'tutor'),
('jkl180000', 'Jenna','Kim', 'Lam', 3, 'tutor'),
('mno180000', 'Mariah','Newman', 'Oppenheimer', 4, 'student'),
('pqr180000', 'Percy','Quinn', 'Reagan', 5, 'student'),
('stu180000', 'Steven','Titus', 'Underwood', 6, 'student'),
('vwx180000', 'Vy','Wan', 'Xander', 7, 'student'),
('yza180000', 'Yin','Zhuge', 'Anderdson', 999, 'student'),
('jad180000', 'Jane','Adams', 'Doe', 20, 'tutor'),
('ctj180000', 'Chris','Taylor', 'Jpnes', 20, 'tutor'),
('ams180000', 'Ashley','Melissa', 'Smith', 20, 'tutor'),
('jjw180000', 'Josh','James', 'Williams', 20, 'tutor');
--done

insert into Person (net_id, fname, mname, lname, hours_completed, usertype)
values ('axc180000', 'Albert','', 'Carey', 0, 'tutor');

--example values here will be simple passwords for testing, no actual passwords should be stored, only hashes
insert into Login (net_id, hashed_pw)
values ('abc180000', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4'),
('def180000', 'f5903f51e341a783e69ffc2d9b335048716f5f040a782a2764cd4e728b0f74d9'),
('ghi180000', '1a6336daa9528a5bb8feff461d2b2c6c2da9a883aeb29028fa5c34369764911e'),
('jkl180000', '7aafe8112311ea6a507bf504076ace4e5ea59abf2b9704698f8ecabd14bb1498'),
('mno180000', '9c725ba62ccba25360a9b273f87cd877631df9f52e9633bb7610dffe8907889c'),
('pqr180000', '065788c2e7f9fb66edf448f813a7bd92302fa171df7296f9332d29b64381b8cc'),
('stu180000', 'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1'),
('vwx180000', '98c1eb4ee93476743763878fcb96a25fbc9a175074d64004779ecb5242f645e6'),
('yza180000', 'b9c950640e1b3740e98acb93e669c65766f6670dd1609ba91ff41052ba48c6f3'),
('axc180000', '0f6cdaa500c96e8b5f00b74ebbfb1e80a72f944c501ba89f55a71657c72c4f71'),
('jad180000', '0f6cdaa500c96e8b5f00b74ebbfb1e80a72f944c501ba89f55a71657c72c4f71'),
('ctj180000', '0f6cdaa500c96e8b5f00b74ebbfb1e80a72f944c501ba89f55a71657c72c4f71'),
('ams180000', '0f6cdaa500c96e8b5f00b74ebbfb1e80a72f944c501ba89f55a71657c72c4f71'),
('jjw180000', '0f6cdaa500c96e8b5f00b74ebbfb1e80a72f944c501ba89f55a71657c72c4f71');
--done
--Original password table below, they do not fit to our project's password requirements and are here mainly for testing the hash
/*
('abc180000', '1234'),
('def180000', 'apples'),
('ghi180000', '1234apples'),
('jkl180000', '1234Apples'),
('mno180000', '1234Apples!'),
('pqr180000', '4321Apples'),
('stu180000', 'pass'),
('vwx180000', 'word'),
('yza180000', 'password1234'),
('axc180000', 'Password123456!'),
('jad180000', 'Password123456!'),
('ctj180000', 'Password123456!'),
('ams180000', 'Password123456!'),
('jjw180000', 'Password123456!');
*/

--add date functionality to sql statements
insert into TutorApts (session_id, tutor_id, student_id, day, time, date)
values (0, 'abc180000', 'mno180000', 'Monday', '9am-11am','2023-04-26'),
(1, 'abc180000', 'pqr180000', 'Tuesday', '5pm-6pm','2023-07-26'),
(2, 'def180000', 'stu180000', 'Wednesday', '11am-1pm','2023-10-03'),
(3, 'ghi180000', 'vwx180000', 'Thursday', '2pm-3pm','2023-11-16'),
(4, 'jkl180000', 'yza180000', 'Friday', '11am-1pm','2023-11-21');
--done

insert into SubjectList (tutor_id, classname)
values ('abc180000', 'Discrete Math'),
('abc180000', 'Differential Calculus'),
('abc180000', 'Integral Calculus'),
('def180000', 'Biology'),
('def180000', 'Chemistry 1'),
('def180000', 'Chemistry 2'),
('ghi180000', 'College Algebra'),
('ghi180000', 'Trigonometry'),
('ghi180000', 'Statistics'),
('jkl180000', 'Biology 2'),
('jkl180000', 'Discrete Math 2'),
('jkl180000', 'Integral Calculus'),
('axc180000', 'CS 1200'),
('axc180000', 'MATH 2418'),
('jad180000', 'BIOL 2428'),
('ctj180000', 'ENG 2320'),
('ams180000', 'CS 4483'),
('jjw180000', 'MATH 2418');
--done

insert into TutorAvailability (tutor_id, day, time)
values ('abc180000', 'Monday', '9am-12pm'),
('abc180000', 'Monday', '5pm-7pm'),
('abc180000', 'Tuesday', '5pm-7pm'),
('abc180000', 'Thursday', '5pm-7pm'),
('abc180000', 'Friday', '5pm-7pm'),
('def180000', 'Monday', '9am-12pm'),
('def180000', 'Tuesday', '10am-1pm'),
('def180000', 'Wednesday', '11am-2pm'),
('def180000', 'Thursday', '12pm-3pm'),
('def180000', 'Friday', '1pm-4pm'),
('ghi180000', 'Monday', '9:30am-12:30pm'),
('ghi180000', 'Tuesday', '10:30am-1:30pm'),
('ghi180000', 'Wednesday', '11:30am-2:30pm'),
('ghi180000', 'Thursday', '12:30pm-3:30pm'),
('ghi180000', 'Friday', '1:30pm-4:30pm'),
('jkl180000', 'Monday', '9am-12:30pm'),
('jkl180000', 'Tueday', '9:30am-1pm'),
('jkl180000', 'Wednesday', '10am-1:30pm'),
('jkl180000', 'Thursday', '10:30am-2pm'),
('jkl180000', 'Friday', '11am-2:30pm'),
('axc180000', 'Monday', '5pm-7pm'),
('jad180000', 'Monday', '5pm-7pm'),
('ctj180000', 'Monday', '5pm-7pm'),
('ams180000', 'Monday', '5pm-7pm'),
('jjw180000', 'Monday', '5pm-7pm');
--done

insert into FavoriteTutors (student_id, tutor_id)
values ('mno180000', 'abc180000'),
('mno180000', 'def180000'),
('mno180000', 'ghi180000'),
('mno180000', 'jkl180000'),
('pqr180000', 'abc180000'),
('pqr180000', 'def180000'),
('pqr180000', 'ghi180000'),
('stu180000', 'abc180000'),
('stu180000', 'def180000'),
('vwx180000', 'jkl180000'),
('yza180000', 'abc180000');
--done

insert into aboutme (tutor_id, about_me)
values ('abc180000', 'I am alvin, nice to meet you!'),
('def180000', 'I''m devin or something'),
('ghi180000', 'Hi my name is Gerald, I will tutor you well!'),
('jkl180000', 'Jenna''s the name, tutoring''s my game!'),
('axc180000', 'I''m Albert, but you can call me Albie! I don''t have a middle name'),
('jad180000', 'Hi, I''m a tutor here at ETutor, and I primarily help in scientific topics. Here at UTD, I''m on the pre-med path and studying primarily Biology. I try to keep myself available after classes during the weekdays, so let me know if you need any tutoring for any pre-med related courses.'),
('ctj180000', 'Hello, my name is Chris Jones, and I am a tutor at ETutor. My main subjects are in english and communication related classes, so feel free to book an appointment with me if you are having trouble in those areas. I''m currently studying literature at UTD and I tend to have part time work after classes on the weekdays, so I will be mostly available on the weekends.'),
('ams180000', 'Hi, I''m Ashley, and I provide tutoring for computer science related topics at ETutor. I''m currently pursuing a Bachelor of Science in Computer Science. Outside of tutoring, I like to spend my time working on personal projects whether it''s something to do with Machine Learning or Artificial Intelligence. I am available for most of the week other than Fridays, where I meet up with a team of other students to work on a project. If you need any help with Computer Science related topics, I''m open to tutoring whenever I can.'),
('jjw180000', 'Hi, I''m Josh and I teach math topics here at ETutor. If you are having trouble with any mathemateical topics such as differential equations, calculus, statistics, or linear algebra, feel free to book an appointment with me. My availability tends to change based on when I conduct research, but my availability hours will be updated every week.');
--done;
