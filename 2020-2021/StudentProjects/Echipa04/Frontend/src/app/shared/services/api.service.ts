import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';
import { AnalyseInfo, AnalyseResult, HistoryResult, LoggedInUser, LoginInfo, LoginResponse } from '../models/shared.models';
import { LoginService } from './login.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  protected baseUrl: string;

  constructor(private http: HttpClient,
              private loginService: LoginService) {
    this.baseUrl = environment.baseURL;
  }

  analyseImage(base64Image: string, imageName: string): Observable<AnalyseResult> {
    let analyseInfo = new AnalyseInfo();
    analyseInfo.imageBytes = base64Image;

    let loggedInUser: LoggedInUser = this.loginService.getLoggedInUser();
    analyseInfo.userID = loggedInUser != null ? loggedInUser.userID : 'guest';

    analyseInfo.imageName = imageName;

    return this.http.post<AnalyseResult>(this.baseUrl + "analyse_image_server", analyseInfo);
  }

  login(loginInfo: LoginInfo): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.baseUrl + "login_server", loginInfo);
  }

  register(loginInfo: LoginInfo): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.baseUrl + "register_server", loginInfo);
  }

  getUserHistory(): Observable<HistoryResult> {
    let loggedInUser: LoggedInUser = this.loginService.getLoggedInUser();
    return this.http.post<HistoryResult>(this.baseUrl + "get_user_history_server", {"userID": loggedInUser.userID} );
  }

  getRecordImages(recordID: string): Observable<AnalyseResult> {
    let loggedInUser: LoggedInUser = this.loginService.getLoggedInUser();
    return this.http.post<AnalyseResult>(this.baseUrl + "get_record_images_server", {"recordID": recordID} );
  }
}