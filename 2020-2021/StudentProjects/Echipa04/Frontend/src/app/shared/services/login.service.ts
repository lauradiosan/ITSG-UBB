import { Injectable } from '@angular/core';
import { LoggedInUser } from '../models/shared.models';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  loggedInUser: LoggedInUser = null;

  constructor() { }

  getLoggedInUser() {
    if(this.loggedInUser)
      return this.loggedInUser;
    
    return this.getUserFromStorage();
  }

  saveLoggedInUser(userID, email) {
    localStorage.setItem('loggedInUserID', userID);
    localStorage.setItem('loggedInEmail', email);

    let loggedInUser = new LoggedInUser();
    loggedInUser.userID = userID;
    loggedInUser.email = email;

    this.loggedInUser = loggedInUser;
  }

  removeLoggedInUser() {
    localStorage.removeItem("loggedInUserID");
    localStorage.removeItem("loggedInEmail");
    this.loggedInUser = null;
    environment.hideLandingPage = false;
  }

  private getUserFromStorage() {
    let userID = localStorage.getItem('loggedInUserID');
    let email = localStorage.getItem('loggedInEmail');

    if(userID && email) {
      this.saveLoggedInUser(userID, email);
      return this.loggedInUser;
    } else {
      return null;
    }
  }
}
