import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent{
  @Output() analyse: EventEmitter<string> = new EventEmitter();

  quickAnalyse() {
    this.analyse.emit('');
  }
}
