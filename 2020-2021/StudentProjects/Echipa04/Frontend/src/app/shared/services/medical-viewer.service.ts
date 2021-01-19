import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class MedicalViewerService {
  imageData: any;
  imageName: string;

  constructor(private router: Router) { }

  getImageData() {
    return this.imageData;
  }

  getImageName() {
    return this.imageName;
  }

  redirectToMedicalViewer(imageData, imageName) {
    this.imageData = imageData;
    this.imageName = imageName;
    this.router.navigate(['./medical-image-viewer']);
  }
}