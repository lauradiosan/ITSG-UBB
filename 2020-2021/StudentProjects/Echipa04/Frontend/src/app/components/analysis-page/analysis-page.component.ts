import { Component, OnInit } from '@angular/core';
import { SafeResourceUrl } from '@angular/platform-browser';

import { ApiService } from 'src/app/shared/services/api.service';
import { MedicalViewerService } from 'src/app/shared/services/medical-viewer.service';
import { LoginService } from 'src/app/shared/services/login.service';
import { AnalyseResult } from 'src/app/shared/models/shared.models';

import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'analysis-page',
  templateUrl: './analysis-page.component.html',
  styleUrls: ['./analysis-page.component.scss']
})
export class AnalysisPageComponent implements OnInit {
  uploadedImage: any;
  isLoading: boolean = false;
  resultedImageURL: SafeResourceUrl;
  isUserLoggedIn: boolean = false;
  imageFile: any;
  imageName: string;

  constructor(private apiService: ApiService,
              private medicalViewerService: MedicalViewerService,
              private toastr: ToastrService,
              private loginService: LoginService) { }

  ngOnInit() {
    this.isUserLoggedIn = this.loginService.getLoggedInUser() != null;
  }

  public uploadImage(event) { 
    this.uploadedImage = event.target.files[0];
    this.imageName = event.target.files[0].name;

    var reader = new FileReader();
    reader.readAsDataURL(this.uploadedImage); 
    reader.onload = (_event) => { 
      this.imageFile = reader.result;
    }      
  }

  removeImage() {
    this.uploadedImage = null;
  }

  analyseImage() {
    if(!this.uploadedImage) {
      this.errorToast("No image uploaded");
      return;
    }

    this.isLoading = true;

    this.apiService.analyseImage(this.imageFile, this.imageName).subscribe(
      (result: AnalyseResult) => {
        this.medicalViewerService.redirectToMedicalViewer(result.resultBytes, this.uploadedImage.name);
      },
      _ => {
        this.isLoading = false;
        this.removeImage();
        this.errorToast("An error has occured");
    });
  }

  errorToast(message) {
    this.toastr.error(message,'', {
      timeOut: 1500,
    });
  }
}