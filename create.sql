DROP VIEW IF EXISTS tutors;
DROP VIEW IF EXISTS students;
DROP TABLE IF EXISTS FavoriteTutors;
DROP TABLE IF EXISTS TutorAvailability;
DROP TABLE IF EXISTS SubjectList;
DROP TABLE IF EXISTS TutorApts;
DROP TABLE IF EXISTS Login;
DROP TABLE IF EXISTS Person;


CREATE TABLE Person (
    --value net_id should strictly follow the format of a UTD Net ID
    net_id varchar(9) not null,
    fname varchar(30) not null,
    --if a lone "x" is read in the mname value, then the person does not have a middle name registered
    mname varchar(30) null,
    lname varchar(30) not null,
    hours_completed int null DEFAULT 0,
    --usertype should contain the string "student" or "tutor"
    usertype varchar(7) not null,

    PRIMARY KEY(net_id)
);
    


CREATE TABLE Login (
    net_id varchar(9) not null,
    --hashed_pw length should be changed to match the output of the hashing algorithm used
    hashed_pw varchar(64) not null,

    PRIMARY KEY (net_id),
    FOREIGN KEY (net_id) REFERENCES Person (net_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE TutorApts (
    --session_id will be used as a nonce 
    session_id int not null,
    tutor_id varchar(9) not null,
    student_id varchar(9) not null,
    --day should be formatted as a full day of the week, max characters are 9 since Wednesday is the longest day of the week
    day varchar (9) not null,
    --time should be formatted as a span of hours, such as "9am-11am" and will be parsed in the backend
    --longest possible input is "xx:xxam-xx:xxpm", 
    time varchar(18) not null,
    subject varchar (30) not null,


    PRIMARY KEY (session_id),
    FOREIGN KEY (tutor_id) REFERENCES Person (net_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES Person (net_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE SubjectList (
    --only those with usertype "tutor" should be stored in this list, will add contstraint later
    tutor_id varchar(9) not null,
    classname varchar(30) not null,

    PRIMARY KEY(tutor_id, classname),
    FOREIGN KEY (tutor_id) REFERENCES Person (net_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE TutorAvailability(
    --This table will contain all available times that a tutor has, and does not take into account appointments
    tutor_id varchar(9) not null,
    --day should be formatted as a full day of the week, max characters are 9 since Wednesday is the longest day of the week
    day varchar (9) not null,
    --time should be formatted as a span of hours, such as "9am-11am" and will be parsed in the backend
    time varchar(18) not null,

    FOREIGN KEY (tutor_id) REFERENCES Person (net_id)
);

CREATE TABLE FavoriteTutors(
    student_id varchar(9) not null,
    tutor_id varchar(9) not null,

    PRIMARY KEY (student_id, tutor_id),
    FOREIGN KEY (student_id) REFERENCES Person (net_id),
    FOREIGN KEY (tutor_id) REFERENCES Person (net_id)
);

CREATE VIEW tutors AS SELECT * FROM Person WHERE usertype = 'tutor';
CREATE VIEW students AS SELECT * FROM Person WHERE usertype = 'student';
CREATE VIEW unique_subjects AS SELECT DISTINCT classname from subjectlist;