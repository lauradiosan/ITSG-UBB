import { Component, OnInit } from '@angular/core';
import { SafeResourceUrl } from '@angular/platform-browser';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

import { MedicalViewerService } from 'src/app/shared/services/medical-viewer.service';

import { Options } from '@angular-slider/ngx-slider';
import * as JSZip from 'jszip';
import { saveAs } from 'file-saver';

@Component({
  selector: 'medical-image-viewer',
  templateUrl: './medical-image-viewer.component.html',
  styleUrls: ['./medical-image-viewer.component.scss']
})
export class MedicalImageViewerComponent implements OnInit {
  imageData = [];
  imageDataBlob = [];
  imageName: string = null;
  sliderInit: Boolean = false;
  resultedImageURL: SafeResourceUrl;
  value: number = 0;

  options: Options = {
    floor: 0,
    ceil: 0
  };

  constructor(private router: Router,
              private medicalViewerService: MedicalViewerService,
              private location: Location) { }

  ngOnInit(): void {
    this.imageData = this.medicalViewerService.getImageData();

    if(!this.imageData || this.imageData.length === 0) {
        this.returnToAnalysisPage();
        return;
    }

    this.imageName = this.medicalViewerService.getImageName();

    this.options.ceil = this.imageData.length - 1;
    this.sliderInit = true;

    this.convertBase64ToBlob();
  }

  returnToPreviousPage() {
    this.location.back();
  }

  private returnToAnalysisPage() {
    this.router.navigate(['']);
  }

  private base64ToBlob(base64) {
    var binary = this.fixBinary(atob(base64));
    var blob = new Blob([binary], {type: 'image/png'});
    return blob;
  }

  private fixBinary (bin) {
    var length = bin.length;
    var buf = new ArrayBuffer(length);
    var arr = new Uint8Array(buf);
    for (var i = 0; i < length; i++) {
      arr[i] = bin.charCodeAt(i);
    }
    return buf;
  }

  private convertBase64ToBlob() {
    this.imageData.forEach(image => {
      this.imageDataBlob.push(this.base64ToBlob(image))
    });
  }

  public saveAsZip() : void{
    var zip =  new JSZip();
    let imageName = this.imageName.split('.')[0];

    this.imageDataBlob.forEach((_, index) => {
      zip.file(imageName + "" + (index + 1) + ".png", this.imageDataBlob[index]);
    });
    zip.generateAsync({ type: "blob" })
       .then(blob => saveAs(blob, imageName + '.zip'));
  };
}