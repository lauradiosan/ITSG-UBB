export class LoginInfo {
    Email: string;
    Password: string;
}

export class LoggedInUser {
    userID: string;
    email: string;
}

export class LoginResponse {
    userID: string;
    code: string;
    error: string;
}

export class AnalyseInfo {
    userID: string;
    imageBytes: string;
    imageName: string;
}

export class AnalyseResult {
    code: string;
    error: Blob;
    resultBytes: [];
}

export class HistoryResult {
    history: HistoryRecord[];
}

export class HistoryRecord {
    recordID: string; 
    userID: string;
    imageName: string;
    imageDate: string;
}