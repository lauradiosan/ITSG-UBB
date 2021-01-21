import {Component, ElementRef, NgZone, OnInit, Renderer2, ViewChild} from '@angular/core';
import {LoginService} from '../services/login.service';
import {CookieService} from '../services/cookie.service';
import {HttpService} from '../services/http.service';
import {DomSanitizer, SafeUrl} from '@angular/platform-browser';
import {Router} from "@angular/router";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {

  profilePictureUrl: SafeUrl;
  // tslint:disable-next-line:variable-name
  public videos = [
    { thumbnail: 'toy_car.png', video: 'toy_car.mp4' },
    { thumbnail: 'louie.png', video: 'louie.mp4' },
    { thumbnail: 'copii402.png', video: 'copii402.mp4' },
    { thumbnail: 'curaj.png', video: 'curaj.mp4' },
    { thumbnail: 'spies.png', video: 'spies.mp4' },
    { thumbnail: 'shaman.png', video: 'shaman.mp4' },
  ];

  @ViewChild('vid', {static: true})
  public videoElement: ElementRef;

  @ViewChild('vid2', {static: true})
  public vid2: ElementRef;

  canvas: HTMLCanvasElement = document.createElement('canvas');

  videoWidth = 0;
  videoHeight = 0;
  videoClass = 'neutral';

  interval: any;
  currentVideo = '';

  constructor(
    private httpService: HttpService,
    private renderer: Renderer2,
    private cookieService: CookieService,
    private router: Router,
    private zone: NgZone,
    private sanitizer: DomSanitizer) { }

  async ngOnInit() {
    this.startCamera();
    //
    // this.interval = setInterval(() => {
    //   this.detectEmotion();
    // }, 3000);

    this.httpService.getImage('profile')
      .subscribe(blob => {
        const profilePictureUnsafeUrl = URL.createObjectURL(blob);
        this.profilePictureUrl = this.sanitizer.bypassSecurityTrustUrl(profilePictureUnsafeUrl);
      });
    //
    // this.renderer.setProperty(this.vid2.nativeElement, 'src', 'https://youtu.be/UrMr4iZPFz8');
    // this.renderer.listen(this.vid2.nativeElement, 'play', () => {});

  }

  detectEmotion() {
    this.capture();
    this.canvas.toBlob((blob) => {
      this.httpService.postFile('emotion_luxand', blob)
        .subscribe( ans => this.zone.run(() => {
          console.log(ans[0].emotions);
          const emotions = ans[0].emotions;
          let maxEmotion = 'neutral';
          let maxConfidence = 0;

          Object.keys(emotions).forEach(emotion => {
            if (emotions[emotion] > maxConfidence ) {
              maxConfidence = emotions[emotion];
              maxEmotion = emotion;
            }
          });

          this.videoClass = maxEmotion;
        }));
    });
  }

  startCamera() {
    if (!!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia)) {
      navigator.mediaDevices.getUserMedia({video: true}).then(this.attachVideo.bind(this)).catch(this.handleError);
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

  changeVideo(video: { thumbnail: string; video: string }) {
    this.currentVideo = '../../assets/videos/' + video.video;
  }
}
