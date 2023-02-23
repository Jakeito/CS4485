insert into Person (net_id, fname, mname, lname, hours_completed, usertype)
values ('abc180000', 'Alvin','Ben', 'Carter', 0, 'tutor'),
('def180000', 'Devin','Eules', 'Farhadi', 1, 'tutor'),
('ghi180000', 'Gerald','Henry', 'Immhurst', 2, 'tutor'),
('jkl180000', 'Jenna','Kim', 'Lam', 3, 'tutor'),
('mno180000', 'Mariah','Newman', 'Oppenheimer', 4, 'student'),
('pqr180000', 'Percy','Quinn', 'Reagan', 5, 'student'),
('stu180000', 'Steven','Titus', 'Underwood', 6, 'student'),
('vwx180000', 'Vy','Wan', 'Xander', 7, 'student'),
('yza180000', 'Yin','Zhuge', 'Anderdson', 999, 'student');
--done

insert into Login (net_id, hashed_pw)
--example values here will be simple passwords for testing, no actual passwords should be stored, only hashes
values ('abc180000', '1234'),
('def180000', 'apples'),
('ghi180000', '1234apples'),
('jkl180000', '1234Apples'),
('mno180000', '1234Apples!'),
('pqr180000', '4321Apples'),
('stu180000', 'pass'),
('vwx180000', 'word'),
('yza180000', 'password1234');
--done

insert into TutorApts (session_id, tutor_id, student_id, day, time, subject)
values (0, 'abc180000', 'mno180000', 'Monday', '9am-11am', 'Discrete Math'),
(1, 'abc180000', 'pqr180000', 'Tuesday', '5pm-6pm', 'Differential Calculus'),
(2, 'def180000', 'stu180000', 'Wednesday', '11am-1pm', 'Biology'),
(3, 'ghi180000', 'vwx180000', 'Thursday', '2pm-3pm', 'Statistics'),
(4, 'jkl180000', 'yza180000', 'Friday', '11am-1pm', 'Discrete Math 2');
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
('jkl180000', 'Integral Calculus');
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
('jkl180000', 'Friday', '11am-2:30pm');
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