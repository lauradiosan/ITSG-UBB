CREATE TABLE [Users] (
	UserID uniqueidentifier NOT NULL UNIQUE,
	Email varchar(100) NOT NULL UNIQUE,
	Password varchar(100) NOT NULL,
  CONSTRAINT [PK_USERS] PRIMARY KEY CLUSTERED
  (
  [UserID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO

CREATE TABLE [HistoryRecords] (
	RecordID uniqueidentifier NOT NULL,
	UserID uniqueidentifier NOT NULL,
	ImageName varchar(100) NOT NULL,
	ImageDate varchar(100) NOT NULL
  CONSTRAINT [PK_HISTORYRECORDS] PRIMARY KEY CLUSTERED
  (
  [RecordID] ASC
  ) WITH (IGNORE_DUP_KEY = OFF)

)
GO

ALTER TABLE [HistoryRecords] WITH CHECK ADD CONSTRAINT [HistoryRecords_fk0] FOREIGN KEY ([UserID]) REFERENCES [Users]([UserID])
ON UPDATE CASCADE
GO
ALTER TABLE [HistoryRecords] CHECK CONSTRAINT [HistoryRecords_fk0]
GO

