use session_latam;

CREATE TABLE Organizer (
    OrganizerId int AUTO_INCREMENT PRIMARY KEY,
    OrganizerName VARCHAR(1000),
    Login VARCHAR(50) UNIQUE,
    SecretKey VARCHAR(50)
);

CREATE TABLE Person (
    PersonId int AUTO_INCREMENT PRIMARY KEY,
    PersonName VARCHAR(1000) NULL,
    Cpf VARCHAR(50) NULL,
    Phone VARCHAR(50) NULL,
    BirthDate DATETIME NULL,
    Mail VARCHAR(100) NULL,
    RegisterDate TIMESTAMP NULL,
    HasAcceptedPromotion BINARY,
    HasAcceptedParticipation BINARY,
);

CREATE TABLE Room (
    RoomId int AUTO_INCREMENT PRIMARY KEY,
    RoomName VARCHAR(100) NOT NULL
);
INSERT INTO Room (RoomName)
VALUES
('Sala 1');

CREATE TABLE Chair (
    ChairId int AUTO_INCREMENT PRIMARY KEY,
    ChairName VARCHAR(100) NOT NULL
);
INSERT INTO Chair (ChairName)
VALUES
('Cadeira 1'),
('Cadeira 2');

CREATE TABLE Turn (
    TurnId int AUTO_INCREMENT PRIMARY KEY,
    TurnTime timestamp NOT NULL
);

CREATE TABLE Scheduling (
    SchedulingId int AUTO_INCREMENT PRIMARY KEY,
    PersonId int NULL,
    ConfirmationDate TIMESTAMP,
    SchedulingDate TIMESTAMP,
    OrganizerId int NULL,
	TurnId int NOT NULL,
    RoomId int NOT NULL,
    ChairId int NOT NULL,
    SchedulingStatus int NOT NULL,
    IsNotified BINARY,
    FOREIGN KEY (PersonId) REFERENCES Person(PersonId),
    FOREIGN KEY (OrganizerId) REFERENCES Organizer(OrganizerId),
    FOREIGN KEY (TurnId) REFERENCES Turn(TurnId),
    FOREIGN KEY (RoomId) REFERENCES Room(RoomId),
    FOREIGN KEY (ChairId) REFERENCES Chair(ChairId)
);


