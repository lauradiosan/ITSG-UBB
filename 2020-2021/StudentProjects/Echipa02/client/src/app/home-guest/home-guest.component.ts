import { HttpService } from '../services/http.service';
import { Component, ElementRef, NgZone, OnInit, Renderer2, ViewChild } from '@angular/core';
import {CookieService} from "../services/cookie.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-home-guest',
  templateUrl: './home-guest.component.html',
  styleUrls: ['./home-guest.component.css']
})
export class HomeGuestComponent implements OnInit {
  @ViewChild('video', { static: true }) videoElement: ElementRef;

  canvas: HTMLCanvasElement = document.createElement('canvas');

  videoWidth = 0;
  videoHeight = 0;
  constraints = {
      video: {
          facingMode: "environment",
          width: { ideal: 4096 },
          height: { ideal: 2160 }
      }
  };

  constructor(
      private httpService: HttpService,
      private renderer: Renderer2,
      private cookieService: CookieService,
      private router: Router,
      private zone: NgZone
  ) { }

  ngOnInit() {
      this.startCamera();
  }

  upload() {
    this.capture();
    this.canvas.toBlob((blob) => {
      this.httpService.postFile('login', blob)
        .subscribe( ans => this.zone.run(() => {
          if (ans['user_name'] != undefined) {
            this.cookieService.saveUserCookie(ans['user_name']);
            this.router.navigate(['dashboard'])
          }
        }));
    });
  }

  startCamera() {
      if (!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
          navigator.mediaDevices.getUserMedia(this.constraints).then(this.attachVideo.bind(this)).catch(this.handleError);
      } else {
          alert('Sorry, camera not available.');
      }
  }

  attachVideo(stream) {
      this.renderer.setProperty(this.videoElement.nativeElement, 'srcObject', stream);
      this.renderer.listen(this.videoElement.nativeElement, 'play', (event) => {
          this.videoHeight = this.videoElement.nativeElement.videoHeight;
          this.videoWidth = this.videoElement.nativeElement.videoWidth;
      });
  }

  capture() {
      this.renderer.setProperty(this.canvas, 'width', this.videoWidth);
      this.renderer.setProperty(this.canvas, 'height', this.videoHeight);
      this.canvas.getContext('2d').drawImage(this.videoElement.nativeElement, 0, 0);
  }

  handleError(error) {
      console.log('Error: ', error);
  }
}
