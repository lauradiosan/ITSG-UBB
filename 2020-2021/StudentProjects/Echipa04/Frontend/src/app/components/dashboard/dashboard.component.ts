import { Component, OnInit } from '@angular/core';

import { LoginService } from 'src/app/shared/services/login.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  public showAnalysePage = false;
  public hideLandingPage = false;

  constructor(private loginService: LoginService) {}
  
  ngOnInit() {
    environment.hideLandingPage = this.loginService.getLoggedInUser() != null
    this.showAnalysePage = this.hideLandingPage = environment.hideLandingPage;
  }

  analyse() {
    this.showAnalysePage = true
  }
}
