import { Component, Input, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { LoggedInUser } from 'src/app/shared/models/shared.models';
import { LoginService } from 'src/app/shared/services/login.service';

@Component({
  selector: 'nav-bar',
  templateUrl: './nav-bar.component.html',
  styleUrls: ['./nav-bar.component.scss']
})
export class NavBarComponent implements OnInit{
  @Input() hideHistoryBtn: Boolean = false;
  
  loggedInUser: LoggedInUser;

  constructor(private router: Router,
              private loginService: LoginService) { }

  ngOnInit() {
    this.loggedInUser = this.loginService.getLoggedInUser();
  }

  redirectToLogin() { 
    this.router.navigate(["login"]);
  }

  redirectToHistory() {
    this.router.navigate(["history"]);
  }

  signOut() {
    this.loginService.removeLoggedInUser();
    console.log(this.router.url);
    if(this.router.url === '/')
      location.reload();
    else
      this.router.navigate([""]);
  }
}