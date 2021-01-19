class HistoryRecords:
    def __init__(self, recordID, userID, imageName, imageDate):
        self.recordID = recordID
        self.userID = userID
        self.imageName = imageName
        self.imageDate = imageDate

    def serialize(self):
        return {"recordID": self.recordID, "userID": self.userID, "imageName": self.imageName,
                "imageDate": self.imageDate}
