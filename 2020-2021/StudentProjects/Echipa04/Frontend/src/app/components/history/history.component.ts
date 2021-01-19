import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';
import { AnalyseResult, HistoryRecord, HistoryResult, LoggedInUser } from 'src/app/shared/models/shared.models';
import { LoginService } from 'src/app/shared/services/login.service';
import { ApiService } from 'src/app/shared/services/api.service';
import { MedicalViewerService } from 'src/app/shared/services/medical-viewer.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  loggedInUser: LoggedInUser = null;
  historyRecords: HistoryRecord[];
  displayedColumns: string[] = ['index', 'imageDate', 'imageName', 'viewResultBtn'];
  isLoading: Boolean = false;
  isError: Boolean = false;

  constructor(private router: Router,
              private location: Location,
              private loginService: LoginService,
              private apiService: ApiService,
              private medicalViewerService: MedicalViewerService,
              private toastr: ToastrService,) { }

  ngOnInit(): void {
    this.isLoading = true;
    
    this.loggedInUser = this.loginService.getLoggedInUser();

    if(this.loggedInUser == null)
      this.returnToAnalysisPage();
    else
      this.getHistory();
  }

  returnToPreviousPage() {
    this.location.back();
  }

  getHistory() {
    this.apiService.getUserHistory().subscribe(
      (result: HistoryResult) => {
        this.historyRecords = result.history;
        this.isLoading = false;
      },
      _ => {
        this.isLoading = false;
        this.isError = true;
        this.errorToast("An error has occured");
    });
  }

  viewResult(recordID: string, imageName: string) {
    this.isLoading = true;

    this.apiService.getRecordImages(recordID).subscribe(
      (result: AnalyseResult) => {
        this.medicalViewerService.redirectToMedicalViewer(result.resultBytes, imageName);
      },
      _ => {
        this.isLoading = false;
        this.errorToast("An error has occured");
    });
  }

  private returnToAnalysisPage() {
    this.router.navigate(['']);
  }

  errorToast(message) {
    this.toastr.error(message,'', {
      timeOut: 1500,
    });
  }
}
